import streamlit as st
from datetime import date, datetime

from agents.heuristic import (
    generate_plan,
    initialize_progress,
)
from agents.llm_agent import generate_detailed_plan
from utils.validation import validate_goal_input
from utils import progress_manager
from utils.exporters import plan_to_docx


# ------------------------------
# Helper Functions
# ------------------------------
def compute_progress(progress_matrix):
    computed = {}
    for milestone, subtasks in progress_matrix.items():
        total = len(subtasks)
        done = sum(subtasks.values())
        computed[milestone] = int((done / total) * 100)
    return computed


def summarize_subtasks(progress_matrix):
    summary = {}
    for milestone, subtasks in progress_matrix.items():
        summary[milestone] = {
            "completed": [s for s, done in subtasks.items() if done],
            "pending": [s for s, done in subtasks.items() if not done],
        }
    return summary


# ------------------------------
# Initialize Session State
# ------------------------------
defaults = {
    "plan_generated": False,
    "goal": "",
    "constraints": {},
    "milestones": [],
    "progress": {},
    "detailed_plan": "",
    "detailed_plan_original": "",
    "start_date": None,
    "goal_id": "",
    "adapted": False,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ------------------------------
# Page Setup
# ------------------------------
st.set_page_config(page_title="ACHIEVIT", layout="centered")

# ---------------- HEADER ----------------
st.markdown(
    """
    <div style='text-align:center;'>
        <h1>A C H I E V I T</h1>
        <p style='font-size:16px; color:gray; font-weight:600'>
            A hybrid intelligent agent system for students and researchers in achieving their goals/resolutions
        </p>
        <p style='font-size:14px; color:#2ECC71; text-align:center; font-weight:600'>
            🎯 Set Goals • 📝 Create Plans • 🔄 Execute & Adapt • ✅ Complete
        </p>
    </div>
    """,
    unsafe_allow_html=True
) 
st.markdown("---")

# ------------------------------
# Sidebar Inputs
# ------------------------------
st.sidebar.header("Goal Control Panel")

goal_type = st.sidebar.selectbox(
    "Select Goal Type",
    ["Exam", "Assignment", "Dissertation / Thesis"],
)

goal_input = st.sidebar.text_area(
    f"Clearly explain your {goal_type} goal, give context and important details:",
    height=160,
)

st.sidebar.markdown("---")
st.sidebar.caption("Consider these constraints and indicate how they fit into your plan")

with st.sidebar.expander("Constraints", expanded=True):
    hours_per_day = st.number_input(
        "Hours per day you can dedicate to this",
        min_value=1,
        max_value=24,
        value=2,
    )
    skill_level = st.selectbox(
        "Skill level",
        ["Novice", "Intermediate", "Expert"],
    )
    deadline = st.date_input(
        "What is your deadline or time frame for this",
        min_value=date.today(),
    )

# ------------------------------
# Main Panel
# ------------------------------
st.markdown("### Hello 👋!")
st.markdown("""
<p style='font-size:14px; color:#2ECC71;'>
I’m your AI-powered academic planning companion, here to help you finish whatever goal you start<br>
To get started, follow the steps in the sidebar
</p>
""", unsafe_allow_html=True)

# ------------------------------
# Generate Plan
# ------------------------------
if st.button("🚀 Generate Plan", type="primary"):
    errors = validate_goal_input(goal_input, hours_per_day, deadline)

    if errors:
        for e in errors:
            st.error(e)
    else:
        st.session_state.plan_generated = True
        st.session_state.adapted = False
        st.session_state.goal = goal_input
        st.session_state.goal_id = goal_input.lower().replace(" ", "_")

        st.session_state.constraints = {
            "hours_per_day": hours_per_day,
            "skill_level": skill_level,
            "deadline": str(deadline),
        }

        st.session_state.start_date = datetime.today().date()

        st.session_state.milestones = generate_plan(
            goal_input, st.session_state.constraints
        )

        st.session_state.progress = initialize_progress(
            st.session_state.milestones,
            st.session_state.goal,
        )

        with st.spinner("Thinking through your goal and constraints..."):
            plan_text = generate_detailed_plan(
                goal=st.session_state.goal,
                milestones=st.session_state.milestones,
                constraints=st.session_state.constraints,
                progress=compute_progress(st.session_state.progress),
                subtasks=summarize_subtasks(st.session_state.progress),
            )

        st.session_state.detailed_plan_original = plan_text
        st.session_state.detailed_plan = plan_text

# ------------------------------
# Two-column layout
# ------------------------------
col1, col2 = st.columns([2, 1])  # left wider for milestone checkboxes

# ------------------------------
# Left Column: Milestones & Subtasks (Checkbox Matrix)
# ------------------------------
if st.session_state.plan_generated:
    col1.markdown("### ✅ Execute Your Plan")
    col1.caption("Mark completed subtasks. Progress updates automatically.")

    updated_progress = {}

    for milestone, subtasks in st.session_state.progress.items():
        with col1.expander(f"🎯 {milestone}", expanded=True):
            updated_progress[milestone] = {}
            for s_idx, (subtask, completed) in enumerate(subtasks.items()):
                checkbox_key = f"{milestone}_{s_idx}"  # unique key
                updated_progress[milestone][subtask] = col1.checkbox(
                    subtask,
                    value=completed,
                    key=checkbox_key
                )

    if updated_progress != st.session_state.progress:
        st.session_state.progress = updated_progress
        progress_manager.save_progress(
            st.session_state.goal_id,
            execution_matrix=updated_progress,
            computed_progress=compute_progress(updated_progress),
        )
        col1.success("Progress updated from completed subtasks.")

# ------------------------------
# Right Column: Plan, Downloads, Progress Overview
# ------------------------------
if st.session_state.plan_generated:
    # Original Plan
    col2.markdown("### 📘 Your Original Plan")
    col2.write(st.session_state.detailed_plan_original)

    original_docx = plan_to_docx(
        title="ACHIEVIT – Original Plan",
        goal=st.session_state.goal,
        constraints=st.session_state.constraints,
        plan_text=st.session_state.detailed_plan_original,
    )

    col2.download_button(
        "⬇️ Download Original Plan (DOCX)",
        data=original_docx,
        file_name=f"{st.session_state.goal_id}_original_plan.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )

    # Adaptive Plan
    if st.session_state.adapted:
        col2.markdown("### 🔁 Updated Adaptive Plan")
        col2.write(st.session_state.detailed_plan)

        adaptive_docx = plan_to_docx(
            title="ACHIEVIT – Adaptive Plan",
            goal=st.session_state.goal,
            constraints=st.session_state.constraints,
            plan_text=st.session_state.detailed_plan,
        )

        col2.download_button(
            "⬇️ Download Adaptive Plan (DOCX)",
            data=adaptive_docx,
            file_name=f"{st.session_state.goal_id}_adaptive_plan.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

    # Progress Overview
    col2.markdown("### 📊 Progress Overview")
    col2.table(compute_progress(st.session_state.progress))

# ------------------------------
# Deadline Risk Check
# ------------------------------
if st.session_state.plan_generated:
    computed_progress = compute_progress(st.session_state.progress)
    total_progress = sum(computed_progress.values()) / len(computed_progress)

    today = datetime.today().date()

    if deadline > st.session_state.start_date:
        days_total = (deadline - st.session_state.start_date).days
        days_elapsed = (today - st.session_state.start_date).days

        expected_progress = (
            (days_elapsed / days_total) * 100 if days_total > 0 else 100
        )

        if total_progress < expected_progress:
            col2.warning(
                f"⚠️ You are behind schedule! "
                f"Current: {total_progress:.1f}% | "
                f"Expected: {expected_progress:.1f}%"
            )

# ------------------------------
# Adapt Plan
# ------------------------------
st.markdown("---")
if st.session_state.plan_generated and st.button("🔄 Adapt Plan Based on My Progress"):
    with st.spinner("Re-evaluating your plan..."):
        adapted_plan = generate_detailed_plan(
            goal=st.session_state.goal,
            milestones=st.session_state.milestones,
            constraints=st.session_state.constraints,
            progress=compute_progress(st.session_state.progress),
            subtasks=summarize_subtasks(st.session_state.progress),
        )

    st.session_state.detailed_plan = adapted_plan
    st.session_state.adapted = True

    st.success("Plan adapted successfully.")

# ------------------------------
# Start New Goal
# ------------------------------
if st.session_state.plan_generated:
    st.markdown("---")
    if st.button("🆕 Start New Goal", type="primary"):
        for key, value in defaults.items():
            st.session_state[key] = value
        st.rerun()

# ------------------------------
# Footer
# ------------------------------
st.markdown(
    """
    <div style="text-align: center; font-size: 0.85em; color: gray;">
        <strong>ACHIEVIT</strong> — 2026 Encode Commit To Change Hackathon<br>
        🔬 <a href="https://abdul-writecodes.github.io/portfolio/" target="_blank">Developer Portfolio</a><br>
        ☕ <a href="https://www.buymeacoffee.com/abdul_writecodes" target="_blank">Support</a><br>
        <strong>Disclaimer:</strong> No personal data collected.<br>
        © 2025 Abdul Write & Codes.
    </div>
    """,
    unsafe_allow_html=True,
)
