"""
utils/report_generator.py
--------------------------
Generates a structured Markdown report after each onboarding run.

The report includes:
  - Client information
  - Step-by-step execution log
  - Tool outputs
  - Final system status
  - Edge case notes
"""

import os
from datetime import datetime
from pathlib import Path


class ReportGenerator:
    """
    Converts the session's history and state into a permanent Markdown report.
    The report is saved to outputs/report_<client_slug>.md relative to the project root.
    """

    @staticmethod
    def generate(
        client_data: dict,
        history: list,
        final_status: str,
        project_root: str = None,
    ) -> str:
        """
        Build and write the Markdown report.

        Args:
            client_data:  The original client dict (name, email, industry, notes).
            history:      List of step dicts from StateManager.
            final_status: The terminal status string (e.g. 'Completed Successfully').
            project_root: Absolute path to the repo root. Defaults to two levels
                          above this file (app/utils/ → repo root).

        Returns:
            Absolute path to the written report file.
        """
        if project_root is None:
            # Resolve abs path: app/utils/report_generator.py → ../../ = repo root
            project_root = str(Path(__file__).resolve().parents[2])

        output_dir = os.path.join(project_root, "outputs")
        os.makedirs(output_dir, exist_ok=True)

        # Slug the client name for a unique filename
        name_slug = client_data.get("client_name", "unknown").lower().replace(" ", "_").replace(".", "")
        output_path = os.path.join(output_dir, f"report_{name_slug}.md")

        # ── Determine overall emoji badge ─────────────────────────────────────
        if "Completed" in final_status:
            badge = "✅ COMPLETED"
        elif "Aborted" in final_status:
            badge = "❌ ABORTED"
        else:
            badge = "⚠️ PARTIAL"

        # ── Build report lines ────────────────────────────────────────────────
        lines = [
            f"# 📊 OnboardAI Onboarding Report",
            f"",
            f"| Field | Value |",
            f"| --- | --- |",
            f"| **Client** | {client_data.get('client_name', 'Unknown')} |",
            f"| **Industry** | {client_data.get('industry', 'N/A')} |",
            f"| **Email** | {client_data.get('contact_email') or '⚠️ MISSING'} |",
            f"| **Generated** | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |",
            f"| **Status** | {badge} |",
            f"",
            f"---",
            f"",
            f"## ⚙️ Execution Steps",
            f"",
            f"| # | Time | Action | Result | Status |",
            f"| --- | --- | --- | --- | --- |",
        ]

        for i, step in enumerate(history, start=1):
            status_icon = "✅" if step.get("success") else "❌"
            result_text = str(step.get("result", "N/A")).replace("|", "\\|")
            lines.append(
                f"| {i} | {step.get('timestamp')} | `{step.get('action')}` "
                f"| {result_text} | {status_icon} |"
            )

        # ── Edge cases section ────────────────────────────────────────────────
        edge_cases = [s for s in history if not s.get("success")]
        if edge_cases:
            lines += [
                f"",
                f"---",
                f"",
                f"## ⚠️ Edge Cases Detected",
                f"",
            ]
            for ec in edge_cases:
                lines.append(f"- **{ec.get('action')}**: {ec.get('result')}")

        # ── Footer ────────────────────────────────────────────────────────────
        lines += [
            f"",
            f"---",
            f"",
            f"## 🏁 Final Status",
            f"",
            f"```",
            final_status,
            f"```",
            f"",
            f"*Generated automatically by OnboardAI — Agentic Onboarding System*",
        ]

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        return output_path
