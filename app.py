import streamlit as st
from datetime import date
from agents.heuristic import generate_plan
from agents.llm_agent import generate_detailed_plan
from utils.validation import validate_goal_input
from utils import progress_manager

# Page Setup
st.set_page_config(page_title="ACHIEVIT", layout="centered")
st.markdown(
    """
    <div style='text-align: center;'>
        <h1>🎭 ACHIEVIT</h1>
        <p style='font-size: 16px; color: cyan;'>
            Powered by Large Language Model
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.header("Goal Control Panel")

goal_type = st.sidebar.selectbox(
    "Select Goal Type: Exam, Assignment, Research",
    ["Exam", "Assignment", "Dissertation / Thesis"]
)



goal = st.sidebar.text_area(
    f"Clearly explain your {goal_type} goal, give context and important details (e.g topic or focus area):",
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







# --- Main Panel ---
st.markdown("### Welcome to ACHIEVIT! 👋")
st.markdown(
    "Your AI-powered goal planning companion for students and researchers. "
    "To get started, head to the sidebar and enter your goal, describe it and state the constraints."
)


submit = st.button("🚀 Generate Plan", type="primary")

if submit:
    errors = validate_goal_input(goal, hours_per_day, deadline)

    if errors:
        for e in errors:
            st.error(e)

    else:
        constraints = {
            "hours_per_day": hours_per_day,
            "skill_level": skill_level,
            "deadline": str(deadline)
        }

        # --- Internal structure (NOT shown yet) ---
        milestones = generate_plan(goal, constraints)

        goal_id = goal.lower().replace(" ", "_")
        progress = progress_manager.load_progress(goal_id) or {
            m: 0 for m in milestones
        }

        # --- LLM FIRST ---
        with st.spinner("Thinking through your goal and constraints..."):
            detailed_plan = generate_detailed_plan(
                goal=goal,
                milestones=milestones,
                constraints=constraints,
                progress=progress
            )
            
        st.markdown("---")

        st.subheader("Your Adaptive Study Plan")
        st.write(detailed_plan)

        # --- (Optional) Save progress silently ---
        progress_manager.save_progress(goal_id, progress)



# Footer
st.markdown("---")
st.markdown("""
   <div style="text-align: center; font-size: 0.85em; color: gray; line-height: 1.6em;">
    <strong>ACHIEVIT</strong>: Designed and Developed in <strong>2026 Encode Commit To Change Hackathon</strong><br>
    🔬Learn more about Developer: <a href="https://abdul-writecodes.github.io/portfolio/" target="_blank">Abdul</a><br>
    We appreciate voluntary support for this project via 
    <a href="https://www.buymeacoffee.com/abdul_writecodes" target="_blank" style="color: #ff5f1f; font-weight: bold;">☕BuyMeACoffee</a> 
    </a><br>
    <strong>Disclaimer:</strong> This system does not collect or store personal data and information. 
    The feedback that is voluntarily given by users and collected by us is only used to improve the system.<br> 
    © 2025 Abdul Write & Codes. All rights reserved.
</div>
""", unsafe_allow_html=True) 