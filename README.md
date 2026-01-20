# ACHIEVIT
**An LLM-Powered Academic Companion for Goal Achievement**

---

## Description
**ACHIEVIT** is an AI-driven, adaptive academic planning system designed to help **students and researchers structure, track, and achieve their goals**.  
It supports academic tasks such as studying for exams, completing assignments, or writing dissertations while taking into account **real-world constraints** like time availability, skill level, and deadlines.  

By combining **heuristic milestone logic** with **LLM reasoning**, ACHIEVIT provides **adaptive, context-aware guidance** that evolves as users make progress on their goals. The system breaks goals into actionable milestones, tracks completion, and dynamically adjusts plans to maximize success.

<p align="center">
  <img src="assets/Achievit.jpg" alt="Achievit Logo" style="width:100%; max-width:800px;" />
</p>

---

## Architecture & Key Features

### Hybrid Intelligence Architecture
ACHIEVIT uses a layered, human-in-the-loop architecture:

<p align="center">
  <img src="assets/Achievitecture.png" alt="Achievitecture" style="width:100%; max-width:800px;" />
</p>

- **Heuristic Logic Layer**  
  - Generates deterministic milestones from high-level goals  
  - Handles constraints such as time, skill level, and deadlines  

- **LLM Reasoning Layer (Gemini)**  
  - Produces adaptive and context-aware plans  
  - Optimizes schedules based on progress  
  - Suggests strategies and relevant academic resources  

> This hybrid layering ensures plans are **structured, feasible, and intelligent**.

---

### Key Features

#### 🎯 Goal-Oriented Planning
- Supports multiple academic goal types:  
  - **Exams**  
  - **Assignments**  
  - **Dissertations / Theses**  
- Converts high-level goals into **clear, actionable milestones**  
- Plans account for user constraints to ensure feasibility  

#### ⏱️ Constraint-Aware Planning
- Explicitly accounts for:  
  - Daily hours available  
  - Skill level (Novice / Intermediate / Expert)  
  - Fixed deadlines  
- Produces **realistic and achievable plans**  

#### 🔁 Progress-Aware Adaptation
- Track progress through interactive sliders:  
  - *Not started* → 0%  
  - *In progress* → 1–99%  
  - *Completed* → 100%  
- LLM dynamically:  
  - Updates remaining steps  
  - Adjusts schedules  
  - Recommends optimization strategies  
  - Suggests relevant resources  

#### 🧑‍🤝‍🧑 Human-in-the-Loop UI
- Built with **Streamlit** for interactive planning  
- Sidebar for goal input and constraints  
- Users remain in control of:  
  - Goal definition  
  - Progress updates  
  - Plan adaptation  

---

## Target Users
- Undergraduate and postgraduate students  
- Graduate researchers and PhD candidates  
- Self-directed learners with academic goals  
- Developers exploring **LLM agent systems with observability**

---

## Why ACHIEVIT?
- Combines **LLM reasoning + heuristic logic** for smarter planning  
- Supports **adaptive, milestone-driven execution**  
- Handles **real-world constraints** for feasible plans  
- Offers **downloadable plans (DOCX)** for offline use  
- Provides **progress tracking and adaptive updates** for ongoing goal achievement  

---

## Getting Started

1. Clone the repository:  
```bash
git clone https://github.com/<your-username>/achievit.git
