"""
app/main.py
-----------
OnboardAI — Entry Point

Loads client data from data/sample_input.json, initializes all agents,
and runs the agentic PLAN → ACTION → RESULT → DECISION loop for each client.

Run from the repo root:
    python submission_BinaryAgents/app/main.py
"""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

# ── Path bootstrap ─────────────────────────────────────────────────────────────
# Add submission_BinaryAgents/ to sys.path so that `from agents.X`, `from core.X`
# etc. resolve to submission_BinaryAgents/app/agents, submission_BinaryAgents/app/core …
APP_DIR = Path(__file__).resolve().parent          # submission_BinaryAgents/app/
SUBMISSION_ROOT = APP_DIR.parent                    # submission_BinaryAgents/
sys.path.insert(0, str(APP_DIR))                   # lets us do: from agents.X import …

# ── Load .env from submission root ─────────────────────────────────────────────
load_dotenv(dotenv_path=SUBMISSION_ROOT / ".env")
load_dotenv(dotenv_path=SUBMISSION_ROOT / ".env.example")  # fallback

# ── Imports ────────────────────────────────────────────────────────────────────
from core.state_manager import StateManager
from core.agent_loop import AgentLoop
from agents.planner_agent import PlannerAgent
from agents.executor_agent import ExecutorAgent
from agents.validator_agent import ValidatorAgent
from utils.logger import OnboardLogger


def main():
    """
    OnboardAI Entry Point.
    Orchestrates per-client onboarding runs using the multi-agent loop.
    """
    print("\n╔═════════════════════════════════════════════════╗")
    print("║      🤖  OnboardAI — Agentic Onboarding System    ║")
    print("╚══════════════════════════════════════════════════╝\n")

    # 1. Validate API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        OnboardLogger.error(
            "GOOGLE_API_KEY not set. Add it to submission_BinaryAgents/.env"
        )
        sys.exit(1)

    # 2. Resolve data file path (always relative to SUBMISSION_ROOT)
    data_file = SUBMISSION_ROOT / "data" / "sample_input.json"
    try:
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        clients = data.get("clients", [])
    except FileNotFoundError:
        OnboardLogger.error(f"Data file not found: {data_file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        OnboardLogger.error(f"Malformed JSON in sample_input.json: {e}")
        sys.exit(1)

    if not clients:
        OnboardLogger.error("No clients found in sample_input.json")
        sys.exit(1)

    # 3. Run the agentic loop for each client
    for idx, client in enumerate(clients, start=1):
        name = client.get("client_name", "Unknown")
        print(f"\n{'─'*55}")
        print(f"  CLIENT {idx}/{len(clients)}: {name}")
        print(f"{'─'*55}")

        state_manager = StateManager(client, project_root=str(SUBMISSION_ROOT))
        planner   = PlannerAgent(api_key=api_key)
        executor  = ExecutorAgent()
        validator = ValidatorAgent()

        loop = AgentLoop(planner, executor, validator, state_manager)

        try:
            loop.start()
        except KeyboardInterrupt:
            OnboardLogger.error("Run interrupted by user.")
            sys.exit(0)
        except Exception as exc:
            OnboardLogger.error(f"Unexpected crash for client '{name}': {exc}")

    print("\n╔══════════════════════════════════════════════════╗")
    print("║        🏁  All Clients Processed — Done!          ║")
    print("╚══════════════════════════════════════════════════╝\n")


if __name__ == "__main__":
    main()
