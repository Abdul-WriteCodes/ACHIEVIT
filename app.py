import streamlit as st
from datetime import date, datetime

from agents.heuristic import generate_plan
from agents.llm_agent import generate_detailed_plan
from utils.validation import validate_goal_input
from utils import progress_manager
from utils.exporters import plan_to_docx

# ------------------------------
# Initialize session state
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
    "adapted": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ------------------------------
# Page Setup
# ------------------------------
st.set_page_config(page_title="ACHIEVIT", layout="centered")

st.markdown(
    "<div style='text-align: center;'>"
    "<h1>🎭 ACHIEVIT</h1>"
    "<p style='font-size: 16px; color: cyan;'>Powered by Large Language Model</p>"
    "</div>",
    unsafe_allow_html=True
)

# ------------------------------
# Sidebar Inputs
# ------------------------------
st.sidebar.header("Goal Control Panel")

goal_type = st.sidebar.selectbox(
    "Select Goal Type",
    ["Exam", "Assignment", "Dissertation / Thesis"]
)

goal_input = st.sidebar.text_area(
    f"Clearly explain your {goal_type} goal, give context and important details:",
    height=160
)

st.sidebar.markdown("---")
st.sidebar.caption("Consider these constraints and indicate how they fit into your plan")

with st.sidebar.expander("Constraints", expanded=True):
    hours_per_day = st.number_input(
        "Hours per day you can dedicate to this",
        min_value=1,
        max_value=24,
        value=2
    )
    skill_level = st.selectbox(
        "Skill level",
        ["Novice", "Intermediate", "Expert"]
    )
    deadline = st.date_input(
        "What is your deadline or time frame for this",
        min_value=date.today()
    )

# ------------------------------
# Main Panel
# ------------------------------
st.markdown("### Welcome to ACHIEVIT 👋")
st.markdown(
    "I’m your AI-powered goal planning companion. "
    "Enter your goal and constraints in the sidebar to get started."
)

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
            "deadline": str(deadline)
        }

        st.session_state.start_date = datetime.today().date()

        st.session_state.milestones = generate_plan(
            goal_input, st.session_state.constraints
        )

        st.session_state.progress = {
            m: 0 for m in st.session_state.milestones
        }

        with st.spinner("Thinking through your goal and constraints..."):
            plan_text = generate_detailed_plan(
                goal=st.session_state.goal,
                milestones=st.session_state.milestones,
                constraints=st.session_state.constraints,
                progress=st.session_state.progress
            )

        st.session_state.detailed_plan_original = plan_text
        st.session_state.detailed_plan = plan_text

# ------------------------------
# Display Original Plan
# ------------------------------
if st.session_state.plan_generated:
    st.markdown("---")
    st.subheader("📘 Your Original Plan")
    st.write(st.session_state.detailed_plan_original)

    # ------------------------------
    # Download Original Plan
    # ------------------------------
    st.markdown("---")
    st.subheader("💾 Download Original Plan")

    original_docx = plan_to_docx(
        title="ACHIEVIT – Original Plan",
        goal=st.session_state.goal,
        constraints=st.session_state.constraints,
        plan_text=st.session_state.detailed_plan_original
    )

    st.download_button(
        "⬇️ Download Original Plan (DOCX)",
        data=original_docx,
        file_name=f"{st.session_state.goal_id}_original_plan.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

    # ------------------------------
    # Execution Layer
    # ------------------------------
    st.markdown("---")
    st.subheader("✅ Execute Your Plan")
    st.caption("Adjust the slider to indicate your progress (0–100%).")

    updated_progress = {}
    for milestone in st.session_state.milestones:
        updated_progress[milestone] = st.slider(
            milestone,
            0,
            100,
            st.session_state.progress.get(milestone, 0),
            key=f"milestone_{milestone}"
        )

    if updated_progress != st.session_state.progress:
        st.session_state.progress = updated_progress
        progress_manager.save_progress(
            st.session_state.goal_id, updated_progress
        )
        st.success("Progress updated successfully.")

    # ------------------------------
    # Deadline Risk Check
    # ------------------------------
    total_progress = sum(updated_progress.values()) / len(updated_progress)
    today = datetime.today().date()

    if deadline > st.session_state.start_date:
        days_total = (deadline - st.session_state.start_date).days
        days_elapsed = (today - st.session_state.start_date).days
        expected_progress = (
            (days_elapsed / days_total) * 100 if days_total > 0 else 100
        )

        if total_progress < expected_progress:
            st.warning(
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
            progress=st.session_state.progress
        )

    st.session_state.detailed_plan = adapted_plan
    st.session_state.adapted = True

    st.success("Plan adapted successfully.")
    st.subheader("🔁 Updated Adaptive Plan")
    st.write(st.session_state.detailed_plan)

# ------------------------------
# Download Adaptive Plan (ONLY AFTER ADAPTATION)
# ------------------------------
if st.session_state.adapted:
    st.markdown("---")
    st.subheader("💾 Download Adaptive Plan")

    adaptive_docx = plan_to_docx(
        title="ACHIEVIT – Adaptive Plan",
        goal=st.session_state.goal,
        constraints=st.session_state.constraints,
        plan_text=st.session_state.detailed_plan
    )

    st.download_button(
        "⬇️ Download Adaptive Plan (DOCX)",
        data=adaptive_docx,
        file_name=f"{st.session_state.goal_id}_adaptive_plan.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )




# ------------------------------
# Progress Overview# ------------------------------
if st.session_state.plan_generated:
    st.markdown("---")
    st.subheader("📊 Progress Overview")
    st.table(st.session_state.progress)
    
 # ------------------------------
# Start New Goal (FINAL ACTION)
# ------------------------------
if st.session_state.plan_generated:
    st.markdown("---")
    if st.button("🆕 Start New Goal"):
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
    unsafe_allow_html=True
)
