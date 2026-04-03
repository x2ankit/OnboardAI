"""
core/agent_loop.py
-------------------
The main orchestration engine for OnboardAI.

Implements the continuous reasoning loop:
    PLAN → ACTION → RESULT → DECISION → LOOP

Each iteration:
 1. Planner (Oogway) queries the LLM for the next action.
 2. Executor (Po)    runs the appropriate simulated tool.
 3. Validator (Viper) checks the result and decides Continue / Retry / Abort.
 4. StateManager records the step and updates history.

The loop halts when the Planner returns DONE, the Validator issues an ABORT,
or the maximum retry budget is exhausted.
"""

from utils.logger import OnboardLogger
from utils.report_generator import ReportGenerator


class AgentLoop:
    """Orchestrates the three agents in a closed reasoning loop."""

    def __init__(self, planner, executor, validator, state_manager):
        self.planner       = planner
        self.executor      = executor
        self.validator     = validator
        self.state_manager = state_manager

    def start(self):
        """Entry point — runs the loop until a terminal condition."""
        OnboardLogger.separator("Starting Agentic Loop")

        iteration = 0

        while not self.state_manager.is_terminal():
            iteration += 1
            OnboardLogger.separator(f"Iteration {iteration}")

            # ── 1. PLAN ───────────────────────────────────────────────────────
            current_state = self.state_manager.get_state_summary()
            decision      = self.planner.decide(current_state, self.state_manager.client_data)
            action        = decision.get("action", "").strip().upper()
            reasoning     = decision.get("reasoning", "")

            self.state_manager.current_action = action

            if reasoning:
                OnboardLogger.plan(f"LLM Reasoning: {reasoning}")

            if action == "DONE":
                self.state_manager.finalize()
                OnboardLogger.plan("Planner determined all onboarding tasks complete.")
                break

            OnboardLogger.plan(f"Next action selected: {action}")

            # ── 2. ACTION ─────────────────────────────────────────────────────
            OnboardLogger.action(f"Executor dispatching tool: {action}")
            result_data = self.executor.execute(action, self.state_manager.client_data)
            self.state_manager.last_result = result_data.get("output") or result_data.get("error")

            output_msg = result_data.get("output") or result_data.get("error", "No output")
            OnboardLogger.result(output_msg)

            # ── 3. DECISION (Validate) ────────────────────────────────────────
            feedback = self.validator.validate(action, result_data, self.state_manager)
            v_status  = feedback.get("status")
            v_message = feedback.get("message", "")

            if v_status == "ABORT":
                self.state_manager.abort(v_message)
                OnboardLogger.error(f"Validator ABORT → {v_message}")
                self.state_manager.add_step(action, v_message, success=False)
                break

            elif v_status == "RETRY":
                if self.state_manager.can_retry():
                    self.state_manager.increment_retry()
                    OnboardLogger.decision(
                        f"Validator RETRY ({self.state_manager.retry_count}/"
                        f"{self.state_manager.MAX_RETRIES}) → {v_message}"
                    )
                    continue
                else:
                    # Out of retries — abort
                    abort_msg = f"Max retries exceeded for {action}: {v_message}"
                    self.state_manager.abort(abort_msg)
                    OnboardLogger.error(abort_msg)
                    break

            elif v_status == "WARN":
                # Non-blocking warning (e.g. duplicate client)
                OnboardLogger.decision(f"⚠️  Validator WARN → {v_message}")
                self.state_manager.record_edge_case(action, v_message)
                # Still mark the step as succeeded so the loop advances
                self.state_manager.add_step(action, output_msg, success=True)

            else:
                # CONTINUE — happy path
                OnboardLogger.decision(f"Validator approved. → {v_message}")
                self.state_manager.add_step(action, output_msg, success=True)

        # ── 4. REPORT ─────────────────────────────────────────────────────────
        OnboardLogger.separator("Generating Report")
        report_path = ReportGenerator.generate(
            client_data=self.state_manager.client_data,
            history=self.state_manager.history,
            final_status=self.state_manager.status,
            project_root=self.state_manager.project_root,
        )
        OnboardLogger.log("REPORT", f"Report saved → {report_path}")
