"""
agents/planner_agent.py
------------------------
Oogway — The Planner Agent

Uses the Gemini LLM to analyze the current onboarding state and decide the
next best action. THIS is the source of true agentic behavior — the system
does NOT follow a fixed sequence; every step is reasoned by the LLM.

Decision format (JSON):
    {
        "action":    "SEND_EMAIL" | "CREATE_DRIVE_FOLDER" |
                     "CREATE_NOTION_PAGE" | "CREATE_AIRTABLE_RECORD" | "DONE",
        "reasoning": "One-sentence justification for this choice."
    }
"""

import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()


AVAILABLE_ACTIONS = [
    "SEND_EMAIL",
    "CREATE_DRIVE_FOLDER",
    "CREATE_NOTION_PAGE",
    "CREATE_AIRTABLE_RECORD",
    "DONE",
]

SYSTEM_PROMPT = """
You are 'Oogway', the Planner Agent for an autonomous Client Onboarding AI system.

Your job is to decide the NEXT SINGLE ACTION to take based on the current system state.

AVAILABLE ACTIONS:
- SEND_EMAIL           → Send a welcome email to the client
- CREATE_DRIVE_FOLDER  → Create a Google Drive folder for assets
- CREATE_NOTION_PAGE   → Set up a Notion onboarding dashboard
- CREATE_AIRTABLE_RECORD → Log the client in the CRM (Airtable)
- DONE                 → All tasks are complete; stop the loop

RULES:
1. Return ONLY a JSON object — no markdown, no explanation outside JSON.
2. JSON must have exactly two keys: "action" and "reasoning".
3. "action" must be one of the AVAILABLE ACTIONS listed above.
4. "reasoning" is a single sentence justifying your choice.
5. If contact_email is missing or marked MISSING, do NOT choose SEND_EMAIL — choose DONE or skip to the next step.
6. If all steps appear in the Completed list, return DONE.
7. Never repeat a step already listed in Completed.
""".strip()


class PlannerAgent:
    """
    Oogway — LLM-powered planning agent.
    On each call to decide(), it sends the full state context to Gemini
    and parses the structured JSON response.
    """

    def __init__(self, api_key: str = None):
        self.api_key  = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY is not set.")
        self.client   = genai.Client(api_key=self.api_key)
        self.model_id = "gemini-2.5-flash"

    def decide(self, current_state: str, client_data: dict) -> dict:
        """
        Ask the LLM which action to take next.

        Returns:
            dict with keys 'action' and 'reasoning'.
            Falls back to heuristic if LLM call fails.
        """
        user_prompt = (
            f"CURRENT STATE:\n{current_state}\n\n"
            f"CLIENT DATA:\n{json.dumps(client_data, indent=2)}\n\n"
            f"Respond with ONLY a JSON object."
        )

        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    response_mime_type="application/json",
                    temperature=0.2,   # low temp = deterministic reasoning
                ),
            )
            raw = response.text.strip()
            decision = json.loads(raw)

            # Sanitize action field
            action = decision.get("action", "").strip().upper()
            if action not in AVAILABLE_ACTIONS:
                raise ValueError(f"LLM returned unknown action: '{action}'")

            decision["action"] = action
            return decision

        except Exception as exc:
            print(f"[Planner] LLM call failed: {exc} — falling back to heuristic.")
            return {
                "action":    self._heuristic_fallback(current_state),
                "reasoning": "Heuristic fallback: LLM unavailable.",
            }

    # ── Heuristic fallback ────────────────────────────────────────────────────

    def _heuristic_fallback(self, state: str) -> str:
        """
        Simple rule-based fallback so the system stays functional even
        if the Gemini API is unreachable (e.g. no internet at hackathon).
        """
        email_missing = "MISSING" in state or "skip SEND_EMAIL" in state
        for step in AVAILABLE_ACTIONS[:-1]:   # all except DONE
            if step in state:
                continue
            if step == "SEND_EMAIL" and email_missing:
                continue
            return step
        return "DONE"
