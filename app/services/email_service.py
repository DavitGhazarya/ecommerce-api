def send_verification_email(
    email: str,
    token: str
):

    link = (
        "http://127.0.0.1:8000/auth/verify-email"
        f"?token={token}"
    )

    print("----------------")
    print("EMAIL TO:", email)
    print("VERIFY LINK:", link)
    print("----------------")
# import smtplib
# from email.message import EmailMessage
#
# from app.config import settings
#
#
# def send_email(
#     recipient: str,
#     subject: str,
#     body: str
# ):
#     message = EmailMessage()
#
#     message["From"] = settings.SMTP_USER
#     message["To"] = recipient
#     message["Subject"] = subject
#
#     message.set_content(body)
#
#     with smtplib.SMTP(
#         settings.SMTP_HOST,
#         settings.SMTP_PORT
#     ) as server:
#
#         server.starttls()
#
#         server.login(
#             settings.SMTP_USER,
#             settings.SMTP_PASSWORD
#         )
#
#         server.send_message(message)
#
# def send_verification_email(
#     email: str,
#     token: str
# ):
#     link = (
#         "http://127.0.0.1:8000/auth/verify-email"
#         f"?token={token}"
#     )
#
#     body = f"""
# Hello!
#
# Please verify your account:
#
# {link}
#
# This link expires in 24 hours.
# """
#
#     send_email(
#         recipient=email,
#         subject="Verify your account",
#         body=body
#     )