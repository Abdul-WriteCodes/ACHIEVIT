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



# Helper Functions
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



# Initialize Session State
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
    "show_execution": False,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value



# Page Setup

st.set_page_config(page_title="🖥️ACHIEVIT", layout="centered")

# ---------------- HEADER ----------------
st.markdown(
    """
    <div style='text-align:center;'>
        <h1>🖥️ A C H I E V I T </h1>
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


# Sidebar Inputs
st.sidebar.header("Goal Control Panel⚙️")

goal_type = st.sidebar.selectbox(
    "Select Goal Type 🎯",
    ["Exam", "Assignment", "Dissertation / Thesis"],
)

goal_input = st.sidebar.text_area(
    f"Clearly describe your {goal_type} goal, give context and important details📝:",
    height=160,
)

st.sidebar.markdown("---")
st.sidebar.caption("Consider these constraints and indicate how they fit into your goal⛔")

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



# Main Panel

st.markdown("### Hello 👋!")
st.markdown(
    """
    <p style='font-size:14px; color:#2ECC71; line-height:1.5;'>
    Achievit is an AI-powered intelligent system that will accompany you in planning, executing and finishing whatever goal you start.<br><br>
    Use the Sidebar to get started:<br>
    🎯 <strong>Select a goal type</strong><br>
    📝 <strong>Describe your goal</strong><br>
    ⏱️ <strong>State your constraints</strong><br>
    👇 Click <strong>'Get Roadmap'</strong><br>
    🕹️ <strong>Take control from there!<strong>
    </p>
    """,
    unsafe_allow_html=True
)



# Generate Plan
_= '''
System operation starts here based on validated inputs: Goal type, goal description and constraints

'''
if st.button("🚀 Get Roadmap", type="primary"):
    errors = validate_goal_input(goal_input, hours_per_day, deadline)

    if errors:
        for e in errors:
            st.error(e)
        st.stop()

    with st.spinner("🧠Thinking through your goal and constraints..."):
        try:
            temp_goal = goal_input
            temp_goal_id = goal_input.lower().replace(" ", "_")

            temp_constraints = {
                "hours_per_day": hours_per_day,
                "skill_level": skill_level,
                "deadline": str(deadline),
            }

            temp_start_date = datetime.today().date()

            temp_milestones = generate_plan(temp_goal, temp_constraints)
            temp_progress = initialize_progress(temp_milestones, temp_goal)

            if len(temp_milestones) != 4 or any(len(v) != 5 for v in temp_progress.values()):
                st.error("❌ Internal planning error. Please try again.")
                st.stop()

            plan_text = generate_detailed_plan(
                goal=temp_goal,
                milestones=temp_milestones,
                constraints=temp_constraints,
                progress=compute_progress(temp_progress),
                subtasks=summarize_subtasks(temp_progress),
            )

        except Exception:
            st.error("❌ AI service unavailable. Please try again.")
            st.stop()

    st.session_state.update({
        "plan_generated": True,
        "adapted": False,
        "goal": temp_goal,
        "goal_id": temp_goal_id,
        "constraints": temp_constraints,
        "start_date": temp_start_date,
        "milestones": temp_milestones,
        "progress": temp_progress,
        "detailed_plan_original": plan_text,
        "detailed_plan": plan_text,
        "show_execution": False,
    })

    st.success(f"✅ Analysis of your {goal_type} and constaint completed")


# Display  Road Map Plan
_= """
LLM agent presents clean and downloadable structured roadmap plan that users have to follow to ensure that the goal is achieved
"""

if st.session_state.plan_generated:
    st.markdown("---")
    st.subheader(f"📄 Here is the Road Map towards  Achieving your {goal_type} goal targets ")
    st.write(st.session_state.detailed_plan_original)

    st.markdown("---")
    st.subheader("💾 Download Roadmap Plan")

    original_docx = plan_to_docx(
        title="ACHIEVIT – Roadmap Plan",
        goal=st.session_state.goal,
        constraints=st.session_state.constraints,
        plan_text=st.session_state.detailed_plan_original,
    )

    st.download_button(
        "⬇️ Download Roadmap Plan",
        data=original_docx,
        file_name=f"{st.session_state.goal_id}_original_plan.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        type="primary",
    )


# Reveal Execution Subtasks Button
_= """
Reveal the planned milestones and subtasks activities that users must execute.
Four milestones are generated for users.
Five substasks are generated per milestone.
Users have to mark any of the subtasks to have competed.
"""
if st.session_state.plan_generated and not st.session_state.show_execution:
    st.markdown("---")
    st.subheader(f"🧠 Ready to Execute Plan and Achieve your {goal_type} ?")
    st.caption("Click to Reveal actionable subtasks and begin execution.")

    if st.button("▶️ Generate Planned Tasks and Activities"):
        st.session_state.show_execution = True
        st.rerun()


# Plan Execution Layer
_= """
Active execution of each of the five subtasks per milestones. 
Execution is in no particular order but progress is saved for the LLM agent (Gemini-3-flash) to work on them.

"""
if st.session_state.plan_generated and st.session_state.show_execution:
    st.markdown("---")
    st.subheader(f"✅  Start Execution: Here are the tasks you need to do to achieve your  {goal_type} Target")

    updated_progress = {}

    for milestone, subtasks in st.session_state.progress.items():
        st.markdown(f"### 🎯 {milestone}")
        updated_progress[milestone] = {}

        for subtask, completed in subtasks.items():
            updated_progress[milestone][subtask] = st.checkbox(
                subtask,
                value=completed,
                key=f"{milestone}_{subtask}",
            )

    if updated_progress != st.session_state.progress:
        st.session_state.progress = updated_progress
        progress_manager.save_progress(
            st.session_state.goal_id,
            execution_matrix=updated_progress,
            computed_progress=compute_progress(updated_progress),
        )
        st.success("Progress updated.")


# Deadline Risk Check 
_= """
Check and validate how user progress on milestone subtasks marked as completed takes them far away from achieving the goal against the deadline period
"""

if st.session_state.plan_generated and st.session_state.show_execution:
    computed_progress = compute_progress(st.session_state.progress)
    total_progress = sum(computed_progress.values()) / len(computed_progress)

    today = datetime.today().date()
    days_total = (deadline - st.session_state.start_date).days
    days_elapsed = (today - st.session_state.start_date).days

    expected_progress = (days_elapsed / days_total) * 100 if days_total > 0 else 100

    if total_progress < expected_progress:
        st.warning(
            f"⚠️ Behind schedule — "
            f"{total_progress:.1f}% done vs {expected_progress:.1f}% expected"
        )


# Road Map Plan Adaptation
_= """
Agent considers the progress level that users have made based on the sub-tasks that are completed.
It provides users with an progress-state adapted roadmap on how to adjust and optimise tasks to ensure that the goal
is achieved within the stated deadline"

"""
st.markdown("---")
if st.session_state.plan_generated and st.button("🔄 Adapt Plan and Get Advice on My Progress"):
    with st.spinner("🧠Re-evaluating your progress against your planned goal and constraints..."):
        adapted_plan = generate_detailed_plan(
            goal=st.session_state.goal,
            milestones=st.session_state.milestones,
            constraints=st.session_state.constraints,
            progress=compute_progress(st.session_state.progress),
            subtasks=summarize_subtasks(st.session_state.progress),
        )

    st.session_state.detailed_plan = adapted_plan
    st.session_state.adapted = True

    st.success("✅ Evaluation successful.")
    st.subheader("🔁 Here is what your progress means....")
    st.write(st.session_state.detailed_plan)



# Progress Overview
_= """
User progress is computed, displayed and updated for every subtask marked as completed

"""
if st.session_state.plan_generated and st.session_state.show_execution:
    st.markdown("---")
    st.subheader("📊 Milestone Progress Overview")
    st.table(compute_progress(st.session_state.progress))

# ------------------------------
# Start New Goal

_= """
System reset logic for users to enter a fresh goal
"""
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
        🖥️ <a href="https://www.comet.com/opik/abdul-writecodes/projects/019c0e9e-6412-759b-ab54-a5238ff89bf7/traces?time_range=past30days&size=100&height=small&traces_filters=%5B%5D&trace=&span=&trace_panel_filters=%5B%5D&traceTab=feedback_scores&thread=&view=dashboards&dashboardId=template%3Aproject-performance" target="_blank">OPIK Observability: View Dashboard</a><br>
        <strong>Disclaimer:</strong> No personal data collected.<br>
        © 2026 Abdul Write & Codes.
    </div>
    """,
    unsafe_allow_html=True,
)
