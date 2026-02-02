EVAL_DATASET = [
    {
        "id": "tight_deadline_case",
        "goal": "Prepare for final year exams",
        "milestones": [
            "Understand exam syllabus",
            "Core concept revision",
            "Practice exam questions",
            "Final consolidation"
        ],
        "constraints": {
            "hours_per_day": 2,
            "skill_level": "intermediate",
            "deadline": "6 days"
        },
        "progress": {
            "Understand exam syllabus": 100,
            "Core concept revision": 40,
            "Practice exam questions": 20,
            "Final consolidation": 0
        },
        "subtasks": {
            "Understand exam syllabus": {
                "completed": [
                    "Read syllabus",
                    "Identify topics",
                    "Check exam format"
                ],
                "pending": [
                    "Note topic weightings",
                    "Clarify assessment rules"
                ]
            },
            "Core concept revision": {
                "completed": [
                    "Lecture notes review",
                    "Watch revision videos"
                ],
                "pending": [
                    "Summarise key concepts",
                    "Create flashcards",
                    "Solve examples"
                ]
            },
            "Practice exam questions": {
                "completed": [
                    "Attempt section A"
                ],
                "pending": [
                    "Attempt section B",
                    "Attempt section C",
                    "Review answers",
                    "Identify weak areas"
                ]
            },
            "Final consolidation": {
                "completed": [],
                "pending": [
                    "Quick revision notes",
                    "Formula memorisation",
                    "Time management strategy",
                    "Rest and recovery",
                    "Final review"
                ]
            }
        }
    }
]
