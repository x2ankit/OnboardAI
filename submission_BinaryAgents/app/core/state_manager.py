"""
core/state_manager.py
----------------------
Single source of truth for a client's onboarding session.

Shared by all three agents across the PLAN → ACTION → RESULT → DECISION loop.
Tracks: client data, step history, completed/pending tasks, retries, and status.
"""

from datetime import datetime
from pathlib import Path


# Canonical ordering of all onboarding steps
ALL_ONBOARDING_STEPS = [
    "SEND_EMAIL",
    "CREATE_DRIVE_FOLDER",
    "CREATE_NOTION_PAGE",
    "CREATE_AIRTABLE_RECORD",
]


class StateManager:
    """
    Maintains mutable session state across the agentic loop.
    """

    def __init__(self, client_data: dict, project_root: str = None):
        self.client_data    = client_data
        self.project_root   = project_root or str(Path(__file__).resolve().parents[2])
        self.history: list  = []
        self.completed_tasks: list = []
        self.pending_tasks: list   = list(ALL_ONBOARDING_STEPS)
        self.aborted        = False
        self.status         = "In Progress"
        self.current_action = None
        self.last_result    = None
        self.retry_count    = 0
        self.MAX_RETRIES    = 2

    # ── Recording ──────────────────────────────────────────────────────────────

    def add_step(self, action: str, result: str, success: bool = True):
        """Record a completed step in history."""
        self.history.append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "action":    action,
            "result":    result,
            "success":   success,
        })
        if success and action not in self.completed_tasks:
            self.completed_tasks.append(action)
            self.pending_tasks = [t for t in self.pending_tasks if t != action]
            self.retry_count   = 0

    def record_edge_case(self, action: str, description: str):
        """Log a non-blocking edge case (e.g. duplicate client) without aborting."""
        self.history.append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "action":    f"EDGE_CASE:{action}",
            "result":    description,
            "success":   False,
        })

    # ── State summary for Planner LLM ─────────────────────────────────────────

    def get_state_summary(self) -> str:
        """
        Rich natural-language summary fed to the Planner on every iteration.
        Explicitly signals missing email so the LLM can reason correctly.
        """
        email = self.client_data.get("contact_email")
        email_status = email if email else "⚠️  MISSING — skip SEND_EMAIL or ABORT"
        return (
            f"Client: '{self.client_data.get('client_name')}' | "
            f"Industry: {self.client_data.get('industry', 'Unknown')} | "
            f"Email: {email_status} | "
            f"Completed: [{', '.join(self.completed_tasks) or 'none'}] | "
            f"Remaining: [{', '.join(self.pending_tasks) or 'ALL DONE'}] | "
            f"Status: {self.status}"
        )

    # ── Control ────────────────────────────────────────────────────────────────

    def abort(self, reason: str):
        """Permanently halt the session."""
        self.aborted = True
        self.status  = f"Aborted: {reason}"
        self.history.append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "action":    "ABORT",
            "result":    reason,
            "success":   False,
        })

    def finalize(self):
        """Mark session successfully completed."""
        if not self.aborted:
            self.status = "Completed Successfully"

    def is_terminal(self) -> bool:
        """True when the loop must stop."""
        return self.aborted or self.status == "Completed Successfully"

    def can_retry(self) -> bool:
        return self.retry_count < self.MAX_RETRIES

    def increment_retry(self):
        self.retry_count += 1
