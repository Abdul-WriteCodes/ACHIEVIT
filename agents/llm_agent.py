# agents/llm_agent.py

import streamlit as st
from google import genai

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=GEMINI_API_KEY)

def generate_detailed_plan(goal, milestones, constraints, progress=None):
    """
    Generate an adaptive, milestone-based academic plan.
    progress: dict mapping milestone -> completion percentage (0–100)
    """

    if progress is None:
        progress = {m: 0 for m in milestones}

    prompt = f"""
You are a seasoned academic planning assistant.

The student has ONE academic goal and EXACTLY FOUR high-level milestones.
Milestones are fixed phases and must NOT be broken into new milestones.

Goal:
{goal}

Constraints:
- Hours per day: {constraints.get("hours_per_day")}
- Skill level: {constraints.get("skill_level")}
- Deadline: {constraints.get("deadline")}

Milestones (fixed structure):
{milestones}

Current progress per milestone (0–100%):
{progress}

Your task:
1. For each milestone, give in-depth explanation what it is all about and how important it is to success . Then suggest concrete next actions appropriate to its progress level.
2. Do NOT repeat completed work; focus on what moves progress forward.
3. Adjust workload based on limited time and skill level.
4. Recommend resources only where useful.
5. Ensure the plan remains realistic for the deadline.
6. If a milestone is 100% complete, acknowledge it briefly and move on.
7. If progress is low and the deadline is near, warn the student and suggest prioritization.


Return the response structured clearly by milestone.
Avoid generic advice.



"""

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    return response.text

