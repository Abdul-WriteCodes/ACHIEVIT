
"""
Heuristic planning layer for ACHIEVIT.

Responsibilities:
- Detect goal type
- Generate stable, deterministic milestones
- Generate milestone-aware subtasks
"""


# Goal Type Detection
def detect_goal_type(goal: str) -> str:
    goal = goal.lower()

    if "exam" in goal or "test" in goal:
        return "exam"
    if "assignment" in goal or "homework" in goal:
        return "assignment"
    if "dissertation" in goal or "thesis" in goal or "research paper" in goal:
        return "dissertation"

    return "generic"


# Milestone Generator
def generate_plan(goal: str, constraints: dict) -> list[str]:
    goal_type = detect_goal_type(goal)

    if goal_type == "exam":
        return [
            "Understand exam syllabus and requirements",
            "Study core topics and concepts",
            "Practice past questions and mock exams",
            "Final revision and exam readiness",
        ]

    if goal_type == "assignment":
        return [
            "Understand assignment requirements",
            "Research and gather relevant materials",
            "Draft and refine the assignment",
            "Final review and submission",
        ]

    if goal_type == "dissertation":
        return [
            "Draft Proposal and Chapter One: Define research scope and purpose",
            "Draft Chapter Two: Literature review and methodology planning",
            "Draft Chapter Three: Execute research and write core chapters",
            "Draft Chapter Four and Five: Analyse, edit, and submit",
        ]

    return [
        "Clarify and scope the goal",
        "Plan and execute core tasks",
        "Review progress and refine work",
        "Finalize and complete the goal",
    ]



# Milestone-Aware Subtask Generator
def generate_subtasks(milestone: str, goal_type: str) -> list[str]:
    m = milestone.lower()

    if goal_type == "exam":
        if "syllabus" in m or "requirements" in m:
            return [
                "Identify all examinable topics and weightings",
                "Review official syllabus and exam format",
                "Map topics to available study materials",
                "Highlight unfamiliar or high-risk areas",
                "Confirm full understanding of exam scope",
            ]

        if "study" in m or "core" in m:
            return [
                "Study key concepts and theories",
                "Create concise notes or summaries",
                "Work through guided examples",
                "Identify weak topics and revise",
                "Validate understanding before proceeding",
            ]

        if "practice" in m or "mock" in m:
            return [
                "Attempt past exam questions",
                "Simulate exam conditions with timing",
                "Review answers using marking schemes",
                "Focus revision on weak areas",
                "Track improvement across attempts",
            ]

        if "revision" in m or "final" in m:
            return [
                "Review condensed notes and formulas",
                "Revise weak areas intensively",
                "Practice rapid recall exercises",
                "Plan exam-day strategy",
                "Confirm readiness for the exam",
            ]

    if goal_type == "assignment":
        if "requirements" in m:
            return [
                "Analyse task instructions and grading rubric",
                "Identify required sections and word limits",
                "Clarify expectations and assessment criteria",
                "List key deliverables",
                "Confirm understanding of the task",
            ]

        if "research" in m:
            return [
                "Search for relevant academic sources",
                "Evaluate credibility and relevance of sources",
                "Extract key arguments and evidence",
                "Organise references thematically",
                "Prepare annotated notes",
            ]

        if "draft" in m:
            return [
                "Outline the structure of the assignment",
                "Write the initial draft for each section",
                "Ensure arguments align with the question",
                "Integrate references correctly",
                "Review draft for coherence",
            ]

        if "final" in m or "submission" in m:
            return [
                "Edit for clarity and academic tone",
                "Check formatting and referencing style",
                "Proofread for grammar and errors",
                "Verify submission requirements",
                "Submit the assignment",
            ]

    if goal_type == "dissertation":
        if "proposal" in m or "chapter one" in m:
            return [
                "Define research problem and objectives",
                "Justify research significance",
                "Formulate research questions",
                "Draft proposal or Chapter One",
                "Prepare for supervisor feedback",
            ]

        if "chapter two" in m or "literature" in m:
            return [
                "Search and collect relevant literature",
                "Critically review key sources",
                "Identify gaps in existing research",
                "Organise literature into themes",
                "Draft literature review chapter",
            ]

        if "chapter three" in m or "research" in m:
            return [
                "Select appropriate research methods",
                "Collect or generate research data",
                "Analyse data systematically",
                "Draft core research chapters",
                "Review findings for accuracy",
            ]

        if "chapter four" in m or "chapter five" in m or "analyse" in m:
            return [
                "Interpret research findings",
                "Link results to research questions",
                "Edit and refine full dissertation",
                "Prepare final submission documents",
                "Submit dissertation",
            ]

    # Generic fallback
    return [
        "Clarify scope of this milestone",
        "Prepare required resources and tools",
        "Execute core task",
        "Review quality and completeness",
        "Finalize and mark milestone as complete",
    ]


# Progress Initializer
def initialize_progress(milestones: list[str], goal: str) -> dict:
    goal_type = detect_goal_type(goal)

    return {
        milestone: {
            subtask: False
            for subtask in generate_subtasks(milestone, goal_type)
        }
        for milestone in milestones
    }
