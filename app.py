import streamlit as st
from datetime import date, datetime
from agents.heuristic import generate_plan
from agents.llm_agent import generate_detailed_plan
from utils.validation import validate_goal_input
from utils import progress_manager

# ------------------------------
# Initialize session state
# ------------------------------
if "plan_generated" not in st.session_state:
    st.session_state.plan_generated = False
if "goal" not in st.session_state:
    st.session_state.goal = ""
if "constraints" not in st.session_state:
    st.session_state.constraints = {}
if "milestones" not in st.session_state:
    st.session_state.milestones = []
if "progress" not in st.session_state:
    st.session_state.progress = {}
if "detailed_plan" not in st.session_state:
    st.session_state.detailed_plan = ""
if "start_date" not in st.session_state:
    st.session_state.start_date = None

# ------------------------------
# Page Setup
# ------------------------------
st.set_page_config(page_title="ACHIEVIT", layout="centered")
st.markdown(
    "<div style='text-align: center;'><h1>🎭 ACHIEVIT</h1>"
    "<p style='font-size: 16px; color: cyan;'>Powered by Large Language Model</p></div>",
    unsafe_allow_html=True
)

# ------------------------------
# Sidebar Inputs
# ------------------------------
st.sidebar.header("Goal Control Panel")

goal_type = st.sidebar.selectbox(
    "Select Goal Type: Exam, Assignment, Research",
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
        "Hours per day you can dedicate to this", min_value=1, max_value=24, value=2
    )
    skill_level = st.selectbox(
        "Skill level", ["Novice", "Intermediate", "Expert"]
    )
    deadline = st.date_input(
        "What is your deadline or time frame for this", min_value=date.today()
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
# Generate Plan Button
# ------------------------------
if st.button("🚀 Generate Plan", type="primary"):
    errors = validate_goal_input(goal_input, hours_per_day, deadline)
    if errors:
        for e in errors:
            st.error(e)
    else:
        st.session_state.plan_generated = True
        st.session_state.goal = goal_input
        st.session_state.constraints = {
            "hours_per_day": hours_per_day,
            "skill_level": skill_level,
            "deadline": str(deadline)
        }
        st.session_state.start_date = datetime.today().date()
        st.session_state.milestones = generate_plan(goal_input, st.session_state.constraints)

        # <<< FIX: reset progress to 0% for new plan >>>
        st.session_state.progress = {m: 0 for m in st.session_state.milestones}

        goal_id = goal_input.lower().replace(" ", "_")
        # progress_manager.load_progress can still be used if you want to load saved plans

        with st.spinner("Thinking through your goal and constraints..."):
            st.session_state.detailed_plan = generate_detailed_plan(
                goal=st.session_state.goal,
                milestones=st.session_state.milestones,
                constraints=st.session_state.constraints,
                progress=st.session_state.progress
            )

# ------------------------------
# Display Plan if Generated
# ------------------------------
if st.session_state.plan_generated:
    st.markdown("---")
    st.subheader("Your Adaptive Study Plan")
    st.write(st.session_state.detailed_plan)

    # ------------------------------
    # Execution Layer: Milestone Sliders
    # ------------------------------
    st.markdown("---")
    st.subheader("✅ Execute Your Plan")
    st.caption(
        "Adjust the slider to indicate your progress (0–100%) for each milestone."
    )

    updated_progress = {}
    goal_id = st.session_state.goal.lower().replace(" ", "_")

    for milestone in st.session_state.milestones:
        updated_progress[milestone] = st.slider(
            milestone,
            min_value=0,
            max_value=100,
            value=st.session_state.progress.get(milestone, 0),
            key=f"milestone_{milestone}"
        )

    if updated_progress != st.session_state.progress:
        st.session_state.progress = updated_progress
        progress_manager.save_progress(goal_id, updated_progress)
        st.success("Progress updated successfully.")

    # ------------------------------
    # Deadline Risk Check
    # ------------------------------
    total_progress = sum(st.session_state.progress.values()) / len(st.session_state.progress)
    today = datetime.today().date()
    if st.session_state.start_date and deadline > st.session_state.start_date:
        days_total = (deadline - st.session_state.start_date).days
        days_elapsed = (today - st.session_state.start_date).days
        expected_progress = (days_elapsed / days_total) * 100 if days_total > 0 else 100
        if total_progress < expected_progress:
            st.warning(f"⚠️ You are behind schedule! Current progress: {total_progress:.1f}% "
                       f"Expected by now: {expected_progress:.1f}%")

    # ------------------------------
    # Adapt Plan Button
    # ------------------------------
    st.markdown("---")
    if st.button("🔄 Adapt Plan Based on My Progress"):
        with st.spinner("Re-evaluating your plan..."):
            st.session_state.detailed_plan = generate_detailed_plan(
                goal=st.session_state.goal,
                milestones=st.session_state.milestones,
                constraints=st.session_state.constraints,
                progress=st.session_state.progress
            )
        st.success("Plan adapted successfully.")
        st.subheader("🔁 Updated Adaptive Plan")
        st.write(st.session_state.detailed_plan)

    # ------------------------------
    # Start New Goal Button (after adaptation)
    # ------------------------------
    st.markdown("---")
    if st.button("🆕 Start New Goal"):
        st.session_state.plan_generated = False
        st.session_state.goal = ""
        st.session_state.constraints = {}
        st.session_state.milestones = []
        st.session_state.progress = {}
        st.session_state.detailed_plan = ""
        st.session_state.start_date = None
        st.experimental_rerun()

    # ------------------------------
    # Progress Overview Table
    # ------------------------------
    st.markdown("---")
    st.subheader("📊 Progress Overview")
    st.table(st.session_state.progress)
    
    
    
# ------------------------------
# Footer
# ------------------------------
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; font-size: 0.85em; color: gray; line-height: 1.6em;">
        <strong>ACHIEVIT</strong>: 2026 Encode Commit To Change Hackathon<br>
        🔬 <a href="https://abdul-writecodes.github.io/portfolio/" target="_blank">Developer Portfolio</a><br>
        ☕ <a href="https://www.buymeacoffee.com/abdul_writecodes" target="_blank">Support</a><br>
        <strong>Disclaimer:</strong> No personal data collected.<br>
        © 2025 Abdul Write & Codes.
    </div>
    """,
    unsafe_allow_html=True
)
