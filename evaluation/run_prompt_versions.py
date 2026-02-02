from agents.llm_agent import generate_detailed_plan
from evaluation.eval_dataset import EVAL_DATASET

PROMPT_VERSIONS = ["v1.0", "v2.0"]

def run_all():
    results = []

    for case in EVAL_DATASET:
        for version in PROMPT_VERSIONS:
            output = generate_detailed_plan(
                goal=case["goal"],
                milestones=case["milestones"],
                constraints=case["constraints"],
                progress=case["progress"],
                subtasks=case["subtasks"],
                prompt_version=version,  # ✅ now working
            )

            results.append({
                "case_id": case["id"],
                "prompt_version": version,
                "output": output,
            })

    return results

if __name__ == "__main__":
    run_all()
