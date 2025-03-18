from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlmodel import select

from core.db import get_session
from models.users import (
    AccessTokenModel,
    UserLoginIn,
)

from models.users import Users
from core.db import engine, Session
from core.security import check_password, generate_access_token
from repositories.user_repository import UserRepository

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=AccessTokenModel)
def login_user(
    user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[Session, Depends(get_session)],
):
    repo = UserRepository(session)
    user = repo.get_user_by_email(user_credentials.username)    
    
    if user is None:
        return JSONResponse({"error": "Invalid credentials"}, status_code=401)
    
    if not check_password(user_credentials.password, user):
        return JSONResponse({"error": "Invalid credentials"}, status_code=401)
    
    return AccessTokenModel(
        access_token=generate_access_token(user),
    )