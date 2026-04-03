"""
agents/executor_agent.py
-------------------------
Po — The Executor Agent

Receives an action string from the Planner and routes it to the
correct simulated tool. Acts as a clean interface between the loop
and the tool layer — no business logic lives here.
"""

from tools.email_tool    import send_email
from tools.drive_tool    import create_drive_folder
from tools.notion_tool   import create_notion_page
from tools.airtable_tool import create_airtable_record


class ExecutorAgent:
    """
    Po — routes Planner decisions to the appropriate tool function.
    """

    def __init__(self):
        # Tool registry: action name → callable
        self._tool_map = {
            "SEND_EMAIL":             send_email,
            "CREATE_DRIVE_FOLDER":    create_drive_folder,
            "CREATE_NOTION_PAGE":     create_notion_page,
            "CREATE_AIRTABLE_RECORD": create_airtable_record,
        }

    def execute(self, action: str, client_data: dict) -> dict:
        """
        Dispatch the action to the correct tool.

        Args:
            action:      One of the AVAILABLE_ACTIONS strings.
            client_data: The client dict from sample_input.json.

        Returns:
            Tool result dict: { success: bool, output: str } or { success: False, error: str }
        """
        tool_fn = self._tool_map.get(action)

        if not tool_fn:
            return {
                "success": False,
                "error":   f"Unknown action '{action}' — no tool registered.",
            }

        try:
            name     = client_data.get("client_name", "")
            email    = client_data.get("contact_email", "")
            industry = client_data.get("industry", "N/A")

            if action == "SEND_EMAIL":
                return tool_fn(name, email)
            elif action == "CREATE_DRIVE_FOLDER":
                return tool_fn(name)
            elif action in ("CREATE_NOTION_PAGE", "CREATE_AIRTABLE_RECORD"):
                return tool_fn(name, industry)

        except Exception as exc:
            return {"success": False, "error": f"Tool raised exception: {exc}"}

        return {"success": False, "error": "Executor: unhandled dispatch path."}
