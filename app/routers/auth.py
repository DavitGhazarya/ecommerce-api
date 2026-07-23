from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.permissions import admin_only
from app.auth.security import (
    create_access_token,
    generate_token,
    hash_password,
    verify_password
)

from app.database import get_db

from app.models.user import User
from app.models.role import UserRole

from app.schemas.auth import (
    Token,
    UserCreate,
    UserRead,
    ForgotPasswordRequest,
    ResetPasswordRequest
)
from app.schemas.user import UserResponse
from app.services.email_service import send_verification_email
from app.services.token_service import create_user_refresh_token

from app.core.email_service import send_reset_email
import secrets
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# REGISTER CUSTOMER
@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    payload: UserCreate,
    db: Annotated[Session, Depends(get_db)]
):

    existing_user = db.query(User).filter(
        or_(
            User.email == payload.email,
            User.username == payload.username
        )
    ).first()


    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already registered"
        )


    verification_token = generate_token()
    print("USERNAME:", payload.username)
    print("EMAIL:", payload.email)
    user = User(
        username=payload.username,
        email=str(payload.email),
        hashed_password=hash_password(payload.password),
        role=UserRole.USER,
        is_verified=False,
        verification_token=verification_token
    )

    db.add(user)
    db.commit()
    db.refresh(user)


    send_verification_email(
        user.email,
        verification_token
    )


    return user



# VERIFY EMAIL
@router.get("/verify-email")
def verify_email(
    token: str,
    db: Annotated[Session, Depends(get_db)]
):

    user = db.query(User).filter(
        User.verification_token == token
    ).first()


    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid verification token"
        )


    user.is_verified = True
    user.verification_token = None


    db.commit()


    return {
        "message": "Email verified successfully"
    }



# LOGIN
@router.post(
    "/login",
    response_model=Token
)
def login(
    form_data: Annotated[
        OAuth2PasswordRequestForm,
        Depends()
    ],

    db: Annotated[
        Session,
        Depends(get_db)
    ]
):

    user = db.query(User).filter(
        User.username == form_data.username
    ).first()


    if (
        user is None
        or not verify_password(
            form_data.password,
            user.hashed_password
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    access_token = create_access_token(
        str(user.id)
    )

    refresh_token = create_user_refresh_token(
        db,
        user.id
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )



# CURRENT USER
@router.get(
    "/me",
    response_model=UserRead
)
def read_current_user(
    current_user: Annotated[
        User,
        Depends(get_current_user)
    ]
):

    return current_user


@router.post("/forgot-password")
def forgot_password(
    data: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )


    if not user:
        return {
            "message": "If email exists, reset link was sent"
        }


    token = secrets.token_urlsafe(32)


    user.reset_password_token = token

    user.reset_password_token_expire = (
        datetime.utcnow()
        + timedelta(minutes=30)
    )


    db.commit()


    send_reset_email(
        user.email,
        token
    )


    return {
        "message": "Reset email sent"
    }
@router.post("/reset-password")
def reset_password(
    data: ResetPasswordRequest,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(
            User.reset_password_token == data.token
        )
        .first()
    )


    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid token"
        )


    if (
        user.reset_password_token_expire
        < datetime.utcnow()
    ):
        raise HTTPException(
            status_code=400,
            detail="Token expired"
        )


    user.password_hash = hash_password(
        data.new_password
    )


    user.reset_password_token = None
    user.reset_password_token_expire = None


    db.commit()


    return {
        "message": "Password changed successfully"
    }
# ADMIN CREATE SELLER
@router.post(
    "/register-seller",
    response_model=UserRead
)
def register_seller(
    payload: UserCreate,

    db: Annotated[
        Session,
        Depends(get_db)
    ],

    current_user: Annotated[
        User,
        Depends(admin_only)
    ]
):

    existing_user = db.query(User).filter(
        or_(
            User.email == payload.email,
            User.username == payload.username
        )
    ).first()


    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="User already exists"
        )


    user = User(
        username=payload.username,
        email=str(payload.email),

        hashed_password=hash_password(
            payload.password
        ),

        role=UserRole.SELLER,

        is_verified=True
    )


    db.add(user)
    db.commit()
    db.refresh(user)


    return user