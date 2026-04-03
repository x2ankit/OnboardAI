"""
tools/drive_tool.py
--------------------
Simulated Google Drive folder creation tool.

In a real system this would use the Google Drive API (google-api-python-client).
"""

import random
import string


def create_drive_folder(client_name: str) -> dict:
    """
    Create a Google Drive folder for the client's assets.

    Args:
        client_name: The client's company name.

    Returns:
        A result dict with keys: success (bool), output (str), error (str).
    """
    if not client_name or not str(client_name).strip():
        return {
            "success": False,
            "error": "Client name is required to create a Drive folder.",
        }

    # Simulate a Drive folder ID (16-char alphanumeric)
    folder_id = "".join(random.choices(string.ascii_letters + string.digits, k=16))
    folder_name = f"{client_name.strip()} — Onboarding Assets"

    return {
        "success": True,
        "output": (
            f"📁 Google Drive folder created: '{folder_name}' | "
            f"Folder ID: {folder_id} | "
            f"Shared with: onboard@company.io"
        ),
    }
