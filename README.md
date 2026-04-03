<div align="center">

# 🤖 OnboardAI

### Autonomous Client Onboarding — Powered by Agentic AI

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![Gemini](https://img.shields.io/badge/LLM-Gemini_2.0_Flash-orange?logo=google)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Hackathon](https://img.shields.io/badge/Hackathon-Agentic_AI_2026-purple)](.)

*Built for the Agentic AI Hackathon 2026 · Team BinaryAgents*

</div>

---

## 🧠 What is OnboardAI?

OnboardAI is a **fully autonomous, multi-agent system** that replaces manual client onboarding with intelligent, LLM-driven workflow execution.

> Traditional onboarding is manual, slow, and error-prone.  
> OnboardAI replaces this with an LLM that **thinks**, **decides**, and **acts** — without human intervention.

---

## ⚡ Core Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     OnboardAI System                      │
│                                                           │
│   Input (client data)                                     │
│       │                                                   │
│       ▼                                                   │
│  ┌─────────────┐   PLAN    ┌─────────────┐               │
│  │  🧠 Oogway  │ ────────► │  ⚡ Po      │               │
│  │  (Planner)  │           │  (Executor) │               │
│  │  Gemini LLM │ ◄──────── │  Tool Layer │               │
│  └─────────────┘  RESULT   └─────────────┘               │
│         │                        │                        │
│         │          DECISION      ▼                        │
│         └───────────────► ┌─────────────┐                │
│                            │  🛡️ Viper   │                │
│                            │  (Validator)│                │
│                            └─────────────┘                │
│                                  │                        │
│                    Continue / Retry / Abort               │
│                                  │                        │
│                                  ▼                        │
│                         outputs/report.md                 │
└─────────────────────────────────────────────────────────┘
```

---

## 🔁 The Agentic Loop

```
PLAN → ACTION → RESULT → DECISION → LOOP
```

Unlike a fixed pipeline, every step is **decided dynamically by the LLM** based on current state.  
Remove the LLM and the system loses all intelligence — that's what makes it truly agentic.

---

## 👥 Agent Roles

| Agent | Character | Role | Technology |
|---|---|---|---|
| **Planner** | 🧠 Oogway | Decides the next action | Gemini 2.0 Flash |
| **Executor** | ⚡ Po | Runs the tool for that action | Python functions |
| **Validator** | 🛡️ Viper | Checks output, handles edge cases | Rule-based logic |

---

## 🛠️ Simulated Tools

| Tool | Simulates |
|---|---|
| `send_email` | Welcome email dispatch |
| `create_drive_folder` | Google Drive folder creation |
| `create_notion_page` | Notion onboarding dashboard |
| `create_airtable_record` | Airtable CRM record |

---

## ⚠️ Edge Case Handling

| Scenario | System Response |
|---|---|
| **Missing email** | Validator issues `ABORT` — onboarding halts safely |
| **Duplicate client** | Validator issues `WARN` — logged, loop continues |
| **Tool failure** | Validator issues `RETRY` — up to 2 retries per step |
| **Invalid input** | Tool returns error, Validator escalates |

---

## 📊 Structured Logging

Every step is fully transparent:

```
[PLAN]     LLM Reasoning: Email not yet sent and client has valid address.
[PLAN]     Next action selected: SEND_EMAIL
[ACTION]   Executor dispatching tool: SEND_EMAIL
[RESULT]   ✉️ Welcome email dispatched to TechGlobal <hello@techglobal.io>
[DECISION] Validator approved. → Step 'SEND_EMAIL' validated successfully.
```

---

## 📁 Project Structure

```
submission_BinaryAgents/
├── app/
│   ├── main.py                  # Entry point
│   ├── agents/
│   │   ├── planner_agent.py     # Oogway — Gemini LLM decisions
│   │   ├── executor_agent.py    # Po — tool dispatch
│   │   └── validator_agent.py   # Viper — result validation
│   ├── tools/
│   │   ├── email_tool.py
│   │   ├── drive_tool.py
│   │   ├── notion_tool.py
│   │   └── airtable_tool.py
│   ├── core/
│   │   ├── agent_loop.py        # PLAN → ACTION → RESULT → DECISION
│   │   └── state_manager.py     # Session state & history
│   └── utils/
│       ├── logger.py            # Color-coded structured logs
│       └── report_generator.py  # Markdown report writer
├── data/
│   └── sample_input.json        # Test client data (incl. edge cases)
├── docs/
│   ├── architecture.md
│   └── agent_flow.md
├── outputs/                     # Generated reports land here
├── requirements.txt
└── .env.example
```

---

## 🚀 Setup & Run

### 1. Clone and install

```bash
git clone <your-repo-url>
cd <repo-name>
pip install -r submission_BinaryAgents/requirements.txt
```

### 2. Configure API key

```bash
cp submission_BinaryAgents/.env.example submission_BinaryAgents/.env
# Edit .env and set your GOOGLE_API_KEY
```

### 3. Run

```bash
python submission_BinaryAgents/app/main.py
```

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| LLM | Google Gemini 2.0 Flash (`google-genai`) |
| Config | `python-dotenv` |
| Output | Markdown (`outputs/`) |
| Architecture | Custom multi-agent loop |

---

## 🏆 Evaluation Criteria Alignment

| Criterion | How OnboardAI Addresses It |
|---|---|
| **Autonomy (30%)** | LLM decides every step — no hardcoded sequence |
| **Reasoning (25%)** | Planner returns explicit reasoning per decision |
| **Reliability (25%)** | Retry, Warn, Abort tiers + heuristic fallback |
| **Efficiency (20%)** | No sleep delays, minimal footprint, clean loop |

---

## 👥 Team

**Team BinaryAgents** — Agentic AI Hackathon 2026 🚀
