# agents/llm_agent.py
import streamlit as st
from google import genai
from google.genai import errors

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=GEMINI_API_KEY)

# ------------------------------
# Advisory Plan — first LLM call
# ------------------------------
def generate_advisory_plan(goal: str, constraints: dict):
    """
    Generate human-readable advice on achieving the goal.
    Does NOT commit milestones or subtasks.
    """
    prompt = f"""
You are an academic planning assistant.

GOAL:
{goal}

CONSTRAINTS:
- Hours/day: {constraints.get("hours_per_day")}
- Skill level: {constraints.get("skill_level")}
- Deadline: {constraints.get("deadline")}

TASK:
Provide detailed guidance on how to achieve this goal.
Focus on strategy, key milestones, and general execution advice.
Do NOT generate new milestones/subtasks.
"""
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
        )
        return response.text

    except errors.ServerError:
        st.warning("⚠️ AI service temporarily unavailable. Try again later.")
        return "⚠️ Unable to generate advisory plan."

    except errors.APIError:
        st.error("❌ Unexpected error while contacting AI service.")
        return "❌ Advisory plan generation failed."


# ------------------------------
# Adaptive Plan — second LLM call
# ------------------------------
def generate_adaptive_plan(goal: str, milestones: list[str], constraints: dict, progress: dict, subtasks: dict):
    """
    Generate adaptive plan based on current progress.
    - Inputs: milestones, subtasks, progress percentages
    - Outputs: structured adaptive plan with risk warnings
    """
    prompt = f"""
You are an academic planning assistant.

GOAL:
{goal}

CONSTRAINTS:
- Hours/day: {constraints.get("hours_per_day")}
- Skill level: {constraints.get("skill_level")}
- Deadline: {constraints.get("deadline")}

MILESTONES:
{milestones}

PROGRESS:
{progress}

SUBTASKS:
{subtasks}

TASK:
For EACH milestone:
1. Acknowledge completed subtasks.
2. Focus on pending subtasks: next actions, why they matter.
3. Adjust workload based on hours/day, skill, deadline.
4. Signal risks clearly if deadline is near or progress is low.

FORMAT:
- Show milestones with subtasks.
- Mark completed ✅ and pending ⬜
- Include warnings if needed.
- Keep output structured for execution tracking.
"""
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
        )
        return response.text

    except errors.ServerError:
        st.warning("⚠️ AI service temporarily unavailable. Try again later.")
        return "⚠️ Unable to generate adaptive plan now."

    except errors.APIError:
        st.error("❌ Unexpected error while contacting AI service.")
        return "❌ Adaptive plan generation failed."
