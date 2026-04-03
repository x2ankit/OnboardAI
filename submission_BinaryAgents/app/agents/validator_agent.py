"""
agents/validator_agent.py
--------------------------
Viper — The Validator Agent

Inspects the raw result from every tool execution and makes a flow decision:
  CONTINUE → step succeeded, advance the loop
  WARN     → non-critical issue detected (e.g. duplicate); log it but continue
  RETRY    → transient failure; the loop may retry the same action
  ABORT    → critical failure (e.g. missing email); halt onboarding for this client

Viper has read-only access to the StateManager so it can make context-aware decisions.
"""


class ValidatorAgent:
    """
    Viper — validates tool results and controls loop flow.
    """

    def validate(self, action: str, result_data: dict, state_manager=None) -> dict:
        """
        Evaluate the result of a tool call.

        Args:
            action:       The action that was just executed.
            result_data:  The dict returned by the tool (success, output/error).
            state_manager: Optional — used for context-aware decisions.

        Returns:
            dict with keys:
                status:  'CONTINUE' | 'WARN' | 'RETRY' | 'ABORT'
                message: Human-readable explanation.
        """
        success = result_data.get("success", False)
        error   = result_data.get("error", "")
        output  = result_data.get("output", "")

        # ── Edge case 1: Missing email ─────────────────────────────────────────
        if action == "SEND_EMAIL" and not success:
            if "missing" in error.lower() or "invalid" in error.lower():
                return {
                    "status":  "ABORT",
                    "message": f"Missing/invalid email address — cannot onboard client safely. ({error})",
                }
            # Other send failure → retry once
            return {
                "status":  "RETRY",
                "message": f"Email send failed: {error}",
            }

        # ── Edge case 2: Duplicate client in Airtable ─────────────────────────
        if action == "CREATE_AIRTABLE_RECORD":
            if "already exists" in output.lower() or "duplicate" in output.lower():
                return {
                    "status":  "WARN",
                    "message": "Duplicate client detected in Airtable — skipping duplicate record creation.",
                }

        # ── Generic failure → RETRY ────────────────────────────────────────────
        if not success:
            return {
                "status":  "RETRY",
                "message": f"Tool failed for action '{action}': {error}",
            }

        # ── Edge case 3: Invalid / empty output ───────────────────────────────
        if not output or not str(output).strip():
            return {
                "status":  "RETRY",
                "message": f"Tool returned empty output for '{action}'.",
            }

        # ── Happy path ─────────────────────────────────────────────────────────
        return {
            "status":  "CONTINUE",
            "message": f"Step '{action}' validated successfully.",
        }
