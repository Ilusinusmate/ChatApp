from fastapi import APIRouter, Depends, Security
from fastapi.responses import JSONResponse
from sqlmodel import Session

import uuid

from core.db import engine, Session, get_session
from core.oauth import get_current_active_user
from models.users import UserCreationIn, UsersPublic, Users
from repositories.user_repository import UserRepository

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UsersPublic)
def get_me(
    current_user: Users = Security(get_current_active_user)
):
    return current_user


@router.get("/list", response_model=list[UsersPublic])
def list_users(
    session: Session = Depends(get_session)
):
    repo = UserRepository(session)
    users = repo.get_all_users()
    return users


@router.get("/get/{user_id}", response_model=UsersPublic)
def get_user(
    user_id: uuid.UUID,
    session: Session = Depends(get_session)
):
    repo = UserRepository(session)
    user = repo.get_user_by_id(user_id)
    return user


@router.get("/friends", response_model=list[UsersPublic])
def get_friends(
    session: Session = Depends(get_session),
    current_user: Users = Security(get_current_active_user)
):
    repo = UserRepository(session)
    friends = repo.get_user_friends(current_user.id)
    return friends


@router.post("/register", response_model=UsersPublic)
async def register_user(
    body_user: UserCreationIn,
    session: Session = Depends(get_session),
):
    try:
        repo = UserRepository(session)
        if not repo.validate_user_creation(body_user.username, body_user.email):
            return JSONResponse(content={"error": "Email or username already taken."}, status_code=400)
        
        user = repo.create_user(
            body_user.username,
            body_user.email,
            body_user.password
        )
    
    except Exception as e:
        session.rollback()
        return JSONResponse(content={"error": str(e)}, status_code=400)
    
    return user