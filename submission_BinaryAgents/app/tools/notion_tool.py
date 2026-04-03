"""
tools/notion_tool.py
---------------------
Simulated Notion page creation tool.

In a real system this would call the Notion API (notion-client SDK).
"""

import random
import string


def create_notion_page(client_name: str, industry: str) -> dict:
    """
    Create a Notion onboarding dashboard for the client.

    Args:
        client_name: The client's company name.
        industry:    The client's industry (for page template selection).

    Returns:
        A result dict with keys: success (bool), output (str), error (str).
    """
    if not client_name or not str(client_name).strip():
        return {
            "success": False,
            "error": "Client name is required to create a Notion page.",
        }

    page_id = "".join(random.choices(string.hexdigits.lower(), k=32))
    slug = client_name.lower().replace(" ", "-").replace(".", "")
    url = f"https://notion.so/onboarding/{slug}-{page_id[:8]}"

    return {
        "success": True,
        "output": (
            f"📝 Notion dashboard created for '{client_name}' "
            f"(Industry: {industry}) | "
            f"URL: {url} | "
            f"Template: 'Client Onboarding v2'"
        ),
    }
