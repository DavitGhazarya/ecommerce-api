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