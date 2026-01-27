# agents/llm_agent.py

from google import genai
from google.genai import errors
import streamlit as st

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=GEMINI_API_KEY)


class LLMServiceUnavailable(Exception):
    """Raised when the LLM service cannot generate a response."""
    pass


def generate_detailed_plan(
    goal: str,
    milestones: list[str],
    constraints: dict,
    progress: dict,
    subtasks: dict,
) -> str:
    """
    Generate an adaptive, milestone-based academic plan.

    This function is ATOMIC:
    - Returns a valid plan string on success
    - Raises an exception on ANY failure
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

1. Explain what this milestone is and why it matters for achieving the goal.
2. Acknowledge completed subtasks briefly.
3. Focus on pending subtasks:
   - What should be done next
   - Why these actions matter now
4. Adjust workload based on time available, skill level, and deadline proximity.
5. If progress is low and deadline is near, issue a warning and suggest prioritisation.
6. Recommend learning resources ONLY when they directly help pending subtasks.

====================
RESPONSE FORMAT
====================
- Use clear headings for each milestone
- Be concrete and execution-focused
- Avoid generic study advice
- Do NOT restate subtasks verbatim unless explaining actions

The plan must remain realistic, adaptive, and grounded in the execution data provided.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
        )

        if not response or not getattr(response, "text", None):
            raise LLMServiceUnavailable("Empty response from LLM")

        return response.text

    except (errors.ServerError, errors.APIError) as e:
        # Propagate failure to app layer
        raise LLMServiceUnavailable(str(e)) from e

    except Exception as e:
        # Catch-all: still fail hard
        raise LLMServiceUnavailable("Unexpected LLM failure") from e
