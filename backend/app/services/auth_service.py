# Authentication service — logic for registration and login.
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password, create_access_token
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserLogin, Token, UserResponse
from app.utils.logger import get_logger

logger = get_logger("auth_service")


def register_user(payload: UserCreate, db: Session) -> UserResponse:
    """
    Register a new user.

    Raises:
        HTTPException 400 if the email is already taken.
    """
    # Check for existing user
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        logger.warning("Registration failed — duplicate email: %s", payload.email)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists.",
        )

    # Create new user
    new_user = User(
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role=payload.role or "user",
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logger.info("User registered successfully: %s (role=%s)", new_user.email, new_user.role)
    return UserResponse.model_validate(new_user)


def login_user(payload: UserLogin, db: Session) -> Token:
    """
    Authenticate a user and return a JWT access token.

    Raises:
        HTTPException 401 if credentials are invalid.
    """
    user = db.query(User).filter(User.email == payload.email).first()

    if not user or not verify_password(payload.password, user.password_hash):
        logger.warning("Login failed for email: %s", payload.email)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate JWT
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role}
    )

    logger.info("User logged in: %s", user.email)
    return Token(access_token=access_token)
