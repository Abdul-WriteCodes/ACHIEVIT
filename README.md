# ACHIEVIT  
**An LLM-Powered System for Planning, Executing, Tracking,  and Achieving Goal Resolution**

---

## Description

**ACHIEVIT** is an AI-driven, adaptive planning system designed to help **students and researchers structure, execute, and complete academic goals**.

It supports tasks such as preparing for exams, completing assignments, and writing dissertations or theses, while explicitly accounting for **real-world constraints** such as:

- Available study time  
- Skill level  
- Fixed deadlines  

By combining **deterministic heuristic planning** with **LLM-based reasoning**, ACHIEVIT produces **structured, realistic, and adaptive plans** that evolve as users make progress. Goals are broken into stable milestones and executable subtasks, progress is tracked transparently, and plans are dynamically adapted to maximize the likelihood of completion.

<p align="center">
  <img src="assets/Achievit.jpg" alt="Achievit Logo" width="800"/>
</p>

---

## Architecture & Key Features

### Hybrid Intelligence Architecture

ACHIEVIT follows a **layered, human-in-the-loop architecture** that combines rule-based structure with LLM intelligence.

<p align="center">
  <img src="assets/Achievitecture.png" alt="Achievitecture Diagram" width="800"/>
</p>



### 1. Heuristic Logic Layer
- Detects goal type (Exam, Assignment, Dissertation / Thesis)
- Generates **deterministic and auditable milestones**
- Produces structured, milestone-specific subtasks
- Incorporates constraints:
  - Daily hours available
  - Skill level (Novice / Intermediate / Expert)
  - Deadline proximity

### 2. LLM Reasoning Layer (Gemini)
- Interprets execution data and progress signals
- Produces **context-aware, adaptive guidance**
- Re-prioritizes effort as deadlines approach
- Issues warnings when progress lags behind schedule
- Suggests targeted learning resources only when relevant

This hybrid approach ensures plans remain **stable, feasible, and intelligent**, avoiding hallucinated structure while still benefiting from LLM reasoning.

---

## Key Features & How It Works

### 🎯 Goal-Oriented Planning

ACHIEVIT supports multiple academic goal types:

- **Exams**
- **Assignments**
- **Dissertations / Theses**

For each goal, the system:

- Accepts a high-level user goal
- Generates **four fixed milestones**
- Assigns **five executable subtasks per milestone**
- Factors in:
  - Daily time commitment
  - User skill level
  - Fixed deadlines
- Produces **realistic, milestone-based execution plans**
- Tracks completion at the **subtask level**
- Dynamically adapts plans based on actual user progress
- Analyses deadline risk and alerts users when they fall behind
- Recommends strategies and academic resources aligned with pending work

---

### 🧑‍🤝‍🧑 Human-in-the-Loop Interface

- Built with **Streamlit** for fast, interactive iteration
- Sidebar-driven goal and constraint input
- Single column execution layout:
  - Milestone and subtask execution (checkbox matrix)
  - Plan overview, progress, and downloads of plans as docx
- Users remain in full control of:
  - Goal definition
  - Progress updates
  - Plan adaptation decisions
---
## 🔗 Live System

👉 **[Try the Live Demo Here](https://achievit.streamlit.app/)**


## Target Users

- Undergraduate and postgraduate students  
- Graduate researchers and PhD candidates  
- Self-directed learners with academic goals  

---
## OPIK Observability and evaluation

## Observability
- Total number of Trace logged: 
- Total Errors:
	- 52 due to API free tier exhaustion
	- 23 due to system logic issues
	- $0.351 as total token cost
	- p50 duration: 16.2s

## Evaluation Result: LLM-as-a-Judge
- Evaluated Model: Google Gemini-3-Flash
- Judge: OpenAI GPT-4
- Metrics: AnswerRelevance, Hallucination, Moderation
- Size of Dataset: 15
- Basis of Evaluation: Prompt version 1 vs Prompt version 2







---
## Local Installation & Setup

Follow the steps below to clone and run ACHIEVIT locally on your machine.
- Clone the Repository
	- git clone https://github.com/abdul-writecodes/ACHIEVIT.git
	- cd achievit
- Create and Activate a Virtual Environment (Recommended)
- Windows
	- python -m venv venv
	- venv\Scripts\activate
- macOS / Linux
	- python3 -m venv venv
	- source venv/bin/activate
-	Install Dependencies
	- pip install -r requirements.txt
	- Configure Environment Variables
- Create a .streamlit/secrets.toml file in the project root:
	- GEMINI_API_KEY = "input_your_gemini_api_key_here"
	- OPIK_API_KEY = "input_your_opik_api_key_here"  # optional

Gemini API key can be obtained from Google AI Studio.
OPIK is optional but recommended for tracing, evaluation, and observability.

- Run the Application
	- streamlit run app.py
- Open your browser at:
	- http://localhost:8501

---
## Troubleshooting

Gemini API free tier limit exceeded or server overloaded
The free-tier Gemini model has request limits and reduced reasoning capacity. If the limit is exceeded or the server is overloaded, the app will prompt you to try again later or switch to a billed model.

- Missing dependencies
	- Re-run pip install -r requirements.txt
- Secrets not found
	- Ensure .streamlit/secrets.toml exists and is correctly formatted

---

## Disclaimer

ACHIEVIT does not collect or store personal data.  
All planning and progress tracking occur within the application session.

---

© 2026
