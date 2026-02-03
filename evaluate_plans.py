# evaluate_plans.py

from opik import Opik
from opik.evaluation import evaluate
from opik.evaluation.metrics import Hallucination, AnswerRelevance, Moderation
from agents.llm_agent import generate_detailed_plan

# ------------------------------
# 1. Initialize OPIK client and load dataset
# ------------------------------
client = Opik()

dataset = client.get_dataset(name="achievit_user_input_v1")  # your dataset name

# ------------------------------
# 2. Robust evaluation task
# ------------------------------
def evaluation_task(dataset_item):
    """
    Generates a detailed plan using the LLM for a single dataset row.
    Safe defaults ensure no crashes if a field is missing.
    """

    # Safely extract dataset fields
    goal_description = dataset_item.get("goal_description", "No goal description provided")
    goal_type = dataset_item.get("goal_type", "Unknown")
    hours_per_day = dataset_item.get("hours_per_day", "Not specified")
    skill_level = dataset_item.get("skill_level", "Not specified")
    deadline = dataset_item.get("deadline", "No deadline specified")

    # Build context for the LLM
    context = (
        f"Goal type: {goal_type}, "
        f"Hours per day: {hours_per_day}, "
        f"Skill level: {skill_level}, "
        f"Deadline: {deadline}"
    )

    # Call the LLM with all required arguments
    plan = generate_detailed_plan(
        goal=goal_description,
        milestones=context,     # milestones include context
        constraints=context,    # constraints include context
        progress="",            # placeholder; can be enhanced later
        subtasks="",            # placeholder; can be enhanced later
        prompt_version="v1.0"
    )

    # Return in OPIK-compatible format
    return {
        "input": goal_description,
        "output": plan
    }

# ------------------------------
# 3. Metrics to evaluate (LLM-as-a-judge)
# ------------------------------
metrics = [
    AnswerRelevance(),
    Hallucination(),
    Moderation()
]

# ------------------------------
# 4. Run evaluation
# ------------------------------
results = evaluate(
    experiment_name="achievit_plan_quality_v1",
    dataset=dataset,
    task=evaluation_task,
    scoring_metrics=metrics
)

print("✅ Evaluation completed successfully")
