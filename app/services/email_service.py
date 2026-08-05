import smtplib

from email.message import EmailMessage

from app.config import settings


def send_email(
    recipient: str,
    subject: str,
    body: str
):
    message = EmailMessage()

    message["From"] = settings.MAIL_FROM
    message["To"] = recipient
    message["Subject"] = subject

    message.set_content(body)


    with smtplib.SMTP(
        settings.MAIL_SERVER,
        settings.MAIL_PORT
    ) as server:

        server.starttls()

        server.login(
            settings.MAIL_USERNAME,
            settings.MAIL_PASSWORD
        )

        server.send_message(
            message
        )


def send_verification_email(
    email: str,
    token: str
):
    link = (
        f"{settings.BASE_URL}/auth/verify-email"
        f"?token={token}"
    )


    body = f"""
Здравствуйте!

Подтвердите ваш аккаунт Market API:

{link}


Ссылка действует 24 часа.
"""


    send_email(
        recipient=email,
        subject="Verify your Market API account",
        body=body
    )