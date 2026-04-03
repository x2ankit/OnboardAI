"""
tools/airtable_tool.py
-----------------------
Simulated Airtable CRM record creation tool.

In a production system this would use the Airtable REST API or pyairtable SDK.
Here we simulate the outcome realistically to test the full agentic flow.
"""

import random
import string


def create_airtable_record(client_name: str, industry: str) -> dict:
    """
    Create a CRM entry for the new client in Airtable.

    Args:
        client_name: The client's company name.
        industry:    The client's industry sector.

    Returns:
        result dict: { success: bool, output: str } or { success: False, error: str }
    """
    if not client_name or not str(client_name).strip():
        return {
            "success": False,
            "error":   "Client name is required to create an Airtable record.",
        }

    record_id = "rec" + "".join(random.choices(string.ascii_letters + string.digits, k=14))

    return {
        "success": True,
        "output": (
            f"📋 Airtable record created in 'CRM_Master_List' | "
            f"Client: '{client_name}' | Industry: {industry} | "
            f"Status: New Account | Record ID: {record_id}"
        ),
    }
