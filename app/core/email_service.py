import smtplib
from email.mime.text import MIMEText

from app.config import settings


def send_reset_email(
    email: str,
    token: str
):

    reset_link = (
        f"http://localhost:8000/reset-password?token={token}"
    )

    message = MIMEText(
        f"""
        Click the link to reset your password:

        {reset_link}

        This link expires in 30 minutes.
        """
    )

    message["Subject"] = "Reset password"
    message["From"] = settings.EMAIL_USER
    message["To"] = email


    with smtplib.SMTP(
        settings.SMTP_HOST,
        settings.SMTP_PORT
    ) as server:

        server.starttls()

        server.login(
            settings.EMAIL_USER,
            settings.EMAIL_PASSWORD
        )

        server.send_message(message)