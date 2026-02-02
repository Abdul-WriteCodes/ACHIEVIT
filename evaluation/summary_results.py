# evaluation/summary_results.py

import json
import os

# ---------- Config ----------
OUTPUT_FOLDER = "evaluation/output"   # Where your run_prompt_versions and judge outputs are saved
JUDGE_FILE = os.path.join(OUTPUT_FOLDER, "judged_results.json")  # LLM-as-judge results
WINNER_FILE = os.path.join(OUTPUT_FOLDER, "winner.json")         # Optional winner output

# ---------- Load judged results ----------
if not os.path.exists(JUDGE_FILE):
    print(f"❌ Judge results not found at {JUDGE_FILE}")
    exit(1)

with open(JUDGE_FILE, "r") as f:
    judged_data = json.load(f)

# ---------- Compute averages per prompt ----------
scores = {}
for entry in judged_data:
    for version in ["v1.0", "v1.1"]:
        if version not in scores:
            scores[version] = {"relevance": 0, "consistency": 0, "hallucination_risk": 0, "count": 0}
        s = entry.get(version, {})
        if s:
            scores[version]["relevance"] += s.get("relevance", 0)
            scores[version]["consistency"] += s.get("consistency", 0)
            scores[version]["hallucination_risk"] += s.get("hallucination_risk", 0)
            scores[version]["count"] += 1

# Average scores
for version, s in scores.items():
    count = s.pop("count")
    if count > 0:
        for k in s:
            s[k] /= count

# ---------- Determine winner ----------
# Simple scoring: higher relevance + consistency, lower hallucination risk
ranking = {}
for version, s in scores.items():
    ranking[version] = s["relevance"] + s["consistency"] - s["hallucination_risk"]

winner = max(ranking, key=ranking.get)

# ---------- Print summary ----------
print("\n===== Prompt Version Evaluation Summary =====\n")
for version, s in scores.items():
    print(f"Version: {version}")
    print(f"  Relevance          : {s['relevance']:.3f}")
    print(f"  Consistency        : {s['consistency']:.3f}")
    print(f"  Hallucination Risk : {s['hallucination_risk']:.3f}")
    print(f"  Score (R+C-H)     : {ranking[version]:.3f}\n")

print(f"🏆 Winner: {winner} (Highest overall score)\n")

# Optional: save winner
with open(WINNER_FILE, "w") as f:
    json.dump({"best_version": winner, "scores": scores}, f, indent=2)

print(f"✅ Winner info saved to {WINNER_FILE}")
