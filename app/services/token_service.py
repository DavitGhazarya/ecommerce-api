from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.refresh_token import RefreshToken
from app.auth.refresh_token import create_refresh_token
from app.config import settings


def create_user_refresh_token(
    db: Session,
    user_id: int
):

    token, token_hash = create_refresh_token()

    expires = datetime.utcnow() + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    db_token = RefreshToken(
        user_id=user_id,
        token_hash=token_hash,
        expires_at=expires
    )

    db.add(db_token)
    db.commit()

    return token