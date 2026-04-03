# OnboardAI Architecture

This document describes the multi-agent architecture of OnboardAI.

## 🏗️ The Three-Agent System

| Agent | Name | Role | Responsibility |
| --- | --- | --- | --- |
| **Planner** | Oogway | Decision Maker | Analyze state + client info to choose the next tool. Uses Gemini. |
| **Executor** | Po | Action Taker | Maps planned actions to tool internal functions and manages calls. |
| **Validator** | Viper | Quality Guard | Inspects results, checks for edge cases (missing data), and directs the loop. |

## 🔄 Agentic Loop Logic

The system is designed for **autonomy** and **reasoning**. It is *not* a static pipeline.

1.  **PLAN (Planner)**: "Based on the client data for 'TechGlobal' and the fact that we've already sent an email, the next best step is creating a Google Drive folder."
2.  **ACTION (Executor)**: "I will call `create_drive_folder` with the name 'TechGlobal'."
3.  **RESULT (Tools)**: "Folder successfully created with ID: DRV_9821."
4.  **DECISION (Validator)**: "Result verified. No edge cases found. Continue loop."
5.  **REPEAT**: Continue until Planner returns 'DONE'.

## 🛠️ Components

- **StateManager**: A source of truth for the session.
- **OnboardLogger**: Standardized console reporting.
- **ReportGenerator**: Summarizes the entire run into a persistent Markdown file.
