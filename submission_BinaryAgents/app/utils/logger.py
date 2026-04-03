"""
utils/logger.py
---------------
Structured logger for OnboardAI.

Provides clear, color-coded log tags:
  [PLAN]     → Planner/LLM decisions
  [ACTION]   → Executor tool dispatches
  [RESULT]   → Tool outputs
  [DECISION] → Validator decisions
  [ERROR]    → Critical failures
  [REPORT]   → Report generation events
"""

from datetime import datetime

# ANSI color codes for terminal output
COLORS = {
    "PLAN":     "\033[94m",   # Blue
    "ACTION":   "\033[93m",   # Yellow
    "RESULT":   "\033[92m",   # Green
    "DECISION": "\033[96m",   # Cyan
    "ERROR":    "\033[91m",   # Red
    "REPORT":   "\033[95m",   # Magenta
}
RESET = "\033[0m"


class OnboardLogger:
    """
    Central structured logger. Every agent step is logged with a clear tag,
    timestamp, and optional color for readability in the terminal.
    """

    @staticmethod
    def log(tag: str, message: str):
        """Generic log with timestamp and color."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        color = COLORS.get(tag, "")
        print(f"{color}[{timestamp}] [{tag}] {message}{RESET}")

    @staticmethod
    def plan(message: str):
        """Log a Planner (LLM) decision."""
        OnboardLogger.log("PLAN", message)

    @staticmethod
    def action(message: str):
        """Log an Executor tool dispatch."""
        OnboardLogger.log("ACTION", message)

    @staticmethod
    def result(message: str):
        """Log a tool/executor result."""
        OnboardLogger.log("RESULT", message)

    @staticmethod
    def decision(message: str):
        """Log a Validator decision."""
        OnboardLogger.log("DECISION", message)

    @staticmethod
    def error(message: str):
        """Log a critical error."""
        OnboardLogger.log("ERROR", message)

    @staticmethod
    def separator(label: str = ""):
        """Print a visual separator for readability."""
        line = "─" * 60
        if label:
            print(f"\n  {line}\n  🔁 {label}\n  {line}")
        else:
            print(f"  {line}")
