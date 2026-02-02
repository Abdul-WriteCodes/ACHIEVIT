# evaluation/judge.py

import os
import json
import ast
from opik import track
from google import genai
import streamlit as st

# ------------------------------
# Gemini Client
# ------------------------------
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# ------------------------------
# Paths
# ------------------------------
OUTPUT_FOLDER = "evaluation/output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
JUDGE_FILE = os.path.join(OUTPUT_FOLDER, "judged_results.json")

# ------------------------------
# LLM-as-Judge Function
# ------------------------------
@track
def judge_outputs(goal: str, output_v1: str, output_v2: str):
    judge_prompt = f"""
You are an impartial evaluator of AI-generated academic plans.

GOAL:
{goal}

You must compare OUTPUT A and OUTPUT B.

====================
EVALUATION CRITERIA
====================

1. Relevance (0–10)
- Does the plan strictly align with the goal, milestones, and constraints?

2. Consistency (0–10)
- Does it respect fixed milestones and subtasks?
- Does it avoid contradictions?

3. Hallucination Risk (0–10)
- Does it invent milestones, subtasks, or irrelevant advice?
- Lower hallucination risk = higher score.

====================
OUTPUT A
====================
{output_v1}

====================
OUTPUT B
====================
{output_v2}

====================
YOUR TASK
====================
Return a JSON object strictly in this format:

{{
  "winner": "A" or "B",
  "scores": {{
    "A": {{
      "relevance": int,
      "consistency": int,
      "hallucination_risk": int
    }},
    "B": {{
      "relevance": int,
      "consistency": int,
      "hallucination_risk": int
    }}
  }},
  "reason": "Concise explanation"
}}
"""
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=judge_prompt,
    )

    return response.text

# ------------------------------
# Run Judge on Dataset
# ------------------------------
def run_judge(dataset):
    """
    dataset: list of dicts with keys:
      - goal
      - output_v1
      - output_v2
    """
    results = []

    for entry in dataset:
        goal = entry["goal"]
        output_v1 = entry["output_v1"]
        output_v2 = entry["output_v2"]

        try:
            judge_text = judge_outputs(goal, output_v1, output_v2)
            judged = ast.literal_eval(judge_text)  # safe parse
        except Exception:
            judged = {
                "winner": "A",
                "scores": {"A": {}, "B": {}},
                "reason": "Failed to parse LLM JSON"
            }

        results.append({
            "goal": goal,
            "output_v1": output_v1,
            "output_v2": output_v2,
            "judged": judged
        })

    # Save to output
    with open(JUDGE_FILE, "w") as f:
        json.dump(results, f, indent=2)

    print(f"✅ Judge results saved at {JUDGE_FILE}")
    return results


# ------------------------------
# Example Usage
# ------------------------------
if __name__ == "__main__":
    # Example: Load dataset.json (list of goal outputs for v1 and v2)
    DATASET_FILE = "evaluation/output/dataset.json"
    if not os.path.exists(DATASET_FILE):
        print(f"❌ Dataset not found at {DATASET_FILE}")
        exit(1)

    with open(DATASET_FILE, "r") as f:
        dataset = json.load(f)

    run_judge(dataset)
