import secrets
import hashlib


def create_refresh_token():

    token = secrets.token_urlsafe(64)

    token_hash = hashlib.sha256(
        token.encode()
    ).hexdigest()

    return token, token_hash