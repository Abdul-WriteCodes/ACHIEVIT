# evaluation/decide_winner.py

import json
from collections import defaultdict
import os

OUTPUT_FOLDER = "evaluation/output"
JUDGE_FILE = os.path.join(OUTPUT_FOLDER, "judged_results.json")

def decide(judge_results):
    """
    Aggregates scores for prompt versions and selects the winner.

    judge_results: list of dicts with structure:
      {
        "goal": str,
        "output_v1": str,
        "output_v2": str,
        "judged": {
            "winner": "A" or "B",
            "scores": {"A": {...}, "B": {...}},
            "reason": str
        }
      }
    """
    totals = defaultdict(lambda: {"relevance": 0, "consistency": 0, "hallucination_risk": 0})

    for result in judge_results:
        scores = result["judged"]["scores"]
        # Map scores to prompt versions
        version_map = {"A": "v1", "B": "v2"}
        for v_key, metrics in scores.items():
            version = version_map[v_key]
            for metric, value in metrics.items():
                totals[version][metric] += value

    # Display aggregated scores
    print("=== AGGREGATED SCORES ===")
    for version, metrics in totals.items():
        print(version, metrics)

    # Decide winner by sum of metrics
    winner = max(
        totals.keys(),
        key=lambda v: sum(totals[v].values())
    )

    print(f"\n🏆 PROMOTED PROMPT VERSION: {winner}")
    return winner


if __name__ == "__main__":
    if not os.path.exists(JUDGE_FILE):
        print(f"❌ Judge results not found at {JUDGE_FILE}")
        exit(1)

    with open(JUDGE_FILE, "r") as f:
        judge_results = json.load(f)

    decide(judge_results)
