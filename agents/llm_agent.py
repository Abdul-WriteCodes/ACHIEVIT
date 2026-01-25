# agents/llm_agent.py

import streamlit as st
from google import genai
from google.genai import errors

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=GEMINI_API_KEY)


def generate_detailed_plan(
    goal: str,
    milestones: list[str],
    constraints: dict,
    progress: dict,
    subtasks: dict,
):
    """
    Generate an adaptive, milestone-based academic plan.

    progress: dict mapping milestone -> completion percentage (0–100)
    subtasks: dict mapping milestone -> {
        "completed": [subtasks],
        "pending": [subtasks]
    }
    """

    prompt = f"""
You are a seasoned academic planning assistant.

This system uses a FIXED heuristic structure.
You MUST respect the given milestones and subtasks.
Do NOT invent new milestones or new subtasks.

====================
GOAL
====================
{goal}

====================
CONSTRAINTS
====================
- Hours per day: {constraints.get("hours_per_day")}
- Skill level: {constraints.get("skill_level")}
- Deadline: {constraints.get("deadline")}

====================
MILESTONES (FIXED)
====================
{milestones}

====================
EXECUTION STATUS
====================
Progress percentages per milestone:
{progress}

Completed and pending subtasks per milestone:
{subtasks}

====================
YOUR TASK
====================
For EACH milestone:

1. Comprehensively explain what this milestone is, why it relates to the GOAL and matters for achieving the goal.
2. Acknowledge completed subtasks succinctly.
3. Focus primarily on pending subtasks and explain:
   - What should be done next
   - Why these actions matter now
4. Adjust workload based on:
   - Time available per day
   - Skill level
   - Proximity to the deadline
5. If a milestone is complete (100%), acknowledge it briefly and move on.
6. If progress is low and the deadline is near, issue a clear warning and suggest prioritisation.
7. Recommend learning resources ONLY when they directly help pending subtasks.

====================
RESPONSE FORMAT
====================
- Use clear headings for each milestone
- Be concrete and execution-focused
- Avoid generic study advice
- Do NOT restate subtasks verbatim unless explaining next actions

The plan must remain realistic, adaptive, and grounded in the execution data provided.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
        )

        return response.text

    except errors.ServerError:
        # Free-tier quota exceeded OR model/server overloaded
        st.warning(
            "⚠️ Gemini API free-tier limit may be exceeded or the server is overloaded.\n\n"
            "Please wait a few minutes and try again."
        )
        return (
            "⚠️ Unable to generate a plan right now due to temporary AI service limits. "
            "Please try again later."
        )

    except errors.APIError:
        st.error(
            "❌ An unexpected error occurred while contacting the AI service."
        )
        return (
            "❌ An unexpected error occurred while generating your plan. "
            "Please try again."
        )
