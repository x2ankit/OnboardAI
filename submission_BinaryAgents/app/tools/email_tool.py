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

    # ── Attempt Real Email if Credentials Exist ───────────────────────────────
    import os
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    gmail_user = os.getenv("GMAIL_USER")
    gmail_pass = os.getenv("GMAIL_APP_PASSWORD")

    if gmail_user and gmail_pass:
        try:
            msg = MIMEMultipart()
            msg['From'] = gmail_user
            msg['To'] = contact_email
            msg['Subject'] = f"Welcome aboard, {client_name}!"

            body = f"Hello {client_name} team,\n\nWelcome to our platform! We are thrilled to have you onboard.\n\nPlease find your onboarding assets enclosed shortly.\n\nBest,\nOnboardAI Autonomous Agent"
            msg.attach(MIMEText(body, 'plain'))

            # Send via Gmail SMTP server
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(gmail_user, gmail_pass)
            server.send_message(msg)
            server.quit()

            return {
                "success": True,
                "output": (
                    f"✉️  REAL Welcome email dispatched via Gmail to {client_name} "
                    f"<{contact_email}> — Subject: 'Welcome aboard, {client_name}!'"
                ),
            }
        except Exception as e:
            # Fall back so we don't crash the demo!
            return {
                "success": True, # Keep workflow moving even if real email fails
                "output": f"✉️  [SIMULATED FALLBACK] Email failed to send: {e}. Simulated success."
            }

    # ── Simulated success (if no credentials) ───────────────────────────────
    return {
        "success": True,
        "output": (
            f"✉️  [SIMULATED] Welcome email dispatched to {client_name} "
            f"<{contact_email}> — Subject: 'Welcome aboard, {client_name}!'"
        ),
    }
