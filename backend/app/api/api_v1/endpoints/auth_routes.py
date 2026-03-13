from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse, Token
from app.services import auth_service
router = APIRouter(prefix="/auth", tags=["Authentication"])
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user account.

    - Validates input via Pydantic schema.
    - Hashes the password with bcrypt.
    - Returns the created user (without password_hash).
    """
    return auth_service.register_user(payload, db)
@router.post(
    "/login",
    response_model=Token,
    summary="Login via Swagger Authorize (form-based)",
)
def login_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    payload = UserLogin(email=form_data.username, password=form_data.password)
    return auth_service.login_user(payload, db)
@router.post(
    "/login/json",
    response_model=Token,
    summary="Login via JSON body",
)
def login_json(payload: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate with email and password (JSON body).

    - Returns a signed JWT access token on success.
    - Returns 401 on invalid credentials.
    """
    return auth_service.login_user(payload, db)