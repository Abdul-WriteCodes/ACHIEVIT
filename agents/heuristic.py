# agents/heuristic.py

def generate_plan(goal, constraints):
    goal_lower = goal.lower()

    if "exam" in goal_lower or "test" in goal_lower:
        milestones = [
            "Understand exam syllabus and requirements",
            "Study core topics and concepts",
            "Practice past questions and mock exams",
            "Final revision and exam readiness"
        ]

    elif "assignment" in goal_lower or "homework" in goal_lower:
        milestones = [
            "Understand assignment requirements",
            "Research and gather relevant materials",
            "Draft and refine the assignment",
            "Final review and submission"
        ]

    elif (
        "dissertation" in goal_lower
        or "thesis" in goal_lower
        or "research paper" in goal_lower
    ):
        milestones = [
            "Draft Proposal and Chapter One: Define research scope, and Purpose",
            "Draft Chapter Two: Conduct literature review and methodology planning",
            "Draft Chapter Three: Plan Methodology, Execute research and write core chapters",
            "Draft Chapter Four and Five: Write core chapters, analyse result, review, edit, and submit"
        ]

    else:
        milestones = [
            "Clarify and scope the goal",
            "Plan and execute core tasks",
            "Review progress and refine work",
            "Finalize and complete the goal"
        ]

    return milestones
