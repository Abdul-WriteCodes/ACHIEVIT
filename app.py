import streamlit as st
from datetime import date, datetime

from agents.heuristic import generate_plan, initialize_progress
from agents.llm_agent import generate_advisory_plan, generate_adaptive_plan
from utils.validation import validate_goal_input
from utils import progress_manager
from utils.exporters import plan_to_docx

# ------------------------------
# Helper Functions
# ------------------------------
def compute_progress(progress_matrix):
    return {
        milestone: int(sum(subtasks.values()) / len(subtasks) * 100)
        for milestone, subtasks in progress_matrix.items()
    }

def summarize_subtasks(progress_matrix):
    return {
        milestone: {
            "completed": [s for s, done in subtasks.items() if done],
            "pending": [s for s, done in subtasks.items() if not done]
        }
        for milestone, subtasks in progress_matrix.items()
    }

# ------------------------------
# Session State
# ------------------------------
defaults = {
    "plan_generated": False,
    "goal": "",
    "constraints": {},
    "milestones": [],
    "progress": {},
    "detailed_plan_original": "",
    "detailed_plan": "",
    "start_date": None,
    "goal_id": "",
    "adapted": False,
    "advisory_text": "",
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ------------------------------
# Page Setup
# ------------------------------
st.set_page_config(page_title="ACHIEVIT", layout="centered")
st.markdown("<h1 style='text-align:center;'>A C H I E V I T</h1>", unsafe_allow_html=True)
st.markdown("---")

# ------------------------------
# Sidebar Inputs
# ------------------------------
st.sidebar.header("Goal Control Panel")
goal_type = st.sidebar.selectbox("Goal Type", ["Exam", "Assignment", "Dissertation / Thesis"])
goal_input = st.sidebar.text_area(f"Describe your {goal_type} goal:", height=160)

st.sidebar.markdown("---")
st.sidebar.caption("Constraints")
with st.sidebar.expander("Set Constraints", expanded=True):
    hours_per_day = st.number_input("Hours/day", 1, 24, 2)
    skill_level = st.selectbox("Skill Level", ["Novice", "Intermediate", "Expert"])
    deadline = st.date_input("Deadline", min_value=date.today())

# ------------------------------
# Generate Plan
# ------------------------------
if st.button("🚀 Generate Plan"):
    errors = validate_goal_input(goal_input, hours_per_day, deadline)
    if errors:
        for e in errors:
            st.error(e)
    else:
        temp_constraints = {
            "hours_per_day": hours_per_day,
            "skill_level": skill_level,
            "deadline": str(deadline)
        }

        # ---------------- First LLM call: advisory plan ----------------
        with st.spinner("Generating advisory plan..."):
            advisory_text = generate_advisory_plan(goal_input, temp_constraints)
            st.session_state.advisory_text = advisory_text
            st.subheader("📝 Advisory Guidance")
            st.write(advisory_text)

        # ---------------- Heuristic Milestones ----------------
        temp_milestones = generate_plan(goal_input, temp_constraints)
        temp_progress = initialize_progress(temp_milestones, goal_input)

        # ---------------- Second LLM call: adaptive plan ----------------
        with st.spinner("Generating adaptive plan..."):
            plan_text = generate_adaptive_plan(
                goal=goal_input,
                milestones=temp_milestones,
                constraints=temp_constraints,
                progress=compute_progress(temp_progress),
                subtasks=summarize_subtasks(temp_progress)
            )

        # ---------------- Commit Phase ----------------
        st.session_state.goal = goal_input
        st.session_state.goal_id = goal_input.lower().replace(" ", "_")
        st.session_state.constraints = temp_constraints
        st.session_state.start_date = datetime.today().date()
        st.session_state.milestones = temp_milestones
        st.session_state.progress = temp_progress
        st.session_state.detailed_plan_original = plan_text
        st.session_state.detailed_plan = plan_text
        st.session_state.plan_generated = True
        st.session_state.adapted = False

# ------------------------------
# Display Plan & Execution
# ------------------------------
if st.session_state.plan_generated:
    st.markdown("---")
    st.subheader("📘 Adaptive Plan")
    st.write(st.session_state.detailed_plan_original)

    st.markdown("---")
    st.subheader("✅ Execute Your Plan")
    updated_progress = {}
    for milestone, subtasks in st.session_state.progress.items():
        st.markdown(f"### {milestone}")
        updated_progress[milestone] = {}
        for subtask, done in subtasks.items():
            updated_progress[milestone][subtask] = st.checkbox(subtask, value=done, key=f"{milestone}_{subtask}")

    if updated_progress != st.session_state.progress:
        st.session_state.progress = updated_progress
        progress_manager.save_progress(
            st.session_state.goal_id,
            execution_matrix=updated_progress,
            computed_progress=compute_progress(updated_progress)
        )
        st.success("Progress updated!")

# ------------------------------
# Adapt Plan Button
# ------------------------------
if st.session_state.plan_generated and st.button("🔄 Adapt Plan"):
    with st.spinner("Re-adapting plan..."):
        adapted_text = generate_adaptive_plan(
            goal=st.session_state.goal,
            milestones=st.session_state.milestones,
            constraints=st.session_state.constraints,
            progress=compute_progress(st.session_state.progress),
            subtasks=summarize_subtasks(st.session_state.progress)
        )
    st.session_state.detailed_plan = adapted_text
    st.session_state.adapted = True
    st.success("Adaptive plan updated.")
    st.subheader("🔁 Updated Plan")
    st.write(adapted_text)

# ------------------------------
# Download Plan
# ------------------------------
if st.session_state.plan_generated:
    st.markdown("---")
    st.subheader("💾 Download Plan")
    docx = plan_to_docx(
        title="ACHIEVIT – Adaptive Plan",
        goal=st.session_state.goal,
        constraints=st.session_state.constraints,
        plan_text=st.session_state.detailed_plan
    )
    st.download_button(
        "⬇️ Download Plan (DOCX)",
        data=docx,
        file_name=f"{st.session_state.goal_id}_adaptive_plan.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

# ------------------------------
# Start New Goal
# ------------------------------
if st.session_state.plan_generated and st.button("🆕 Start New Goal"):
    for k, v in defaults.items():
        st.session_state[k] = v
    st.rerun()
