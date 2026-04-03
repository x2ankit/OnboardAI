"""
tools/email_tool.py
--------------------
Simulated email-sending tool.

In a real system this would call SendGrid / SMTP.
Here we validate inputs and return a structured result dict.
"""


def send_email(client_name: str, contact_email: str) -> dict:
    """
    Send a welcome onboarding email to the client.

    Args:
        client_name:   The client's company name.
        contact_email: The recipient email address.

    Returns:
        A result dict with keys: success (bool), output (str), error (str).
    """
    # ── Validation ────────────────────────────────────────────────────────────
    if not contact_email or not str(contact_email).strip():
        return {
            "success": False,
            "error": "Missing email address — cannot send welcome email.",
        }

    if "@" not in contact_email or "." not in contact_email.split("@")[-1]:
        return {
            "success": False,
            "error": f"Invalid email format: '{contact_email}'.",
        }

    # ── Simulated success ─────────────────────────────────────────────────────
    return {
        "success": True,
        "output": (
            f"✉️  Welcome email dispatched to {client_name} "
            f"<{contact_email}> — Subject: 'Welcome aboard, {client_name}!'"
        ),
    }
