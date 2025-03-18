from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlmodel import select

import uuid
from typing import Annotated

from models.users import Users, UsersPublic
from core.db import engine, Session, get_session
from core.oauth import get_current_user
from models.groups import Groups
from repositories.user_repository import UserRepository
from repositories.group_repository import GroupRepository

router = APIRouter(prefix="/group", tags=["Groups"])

@router.get("/members/{group_id}", response_model=list[UsersPublic])
def get_members(
    group_id: uuid.UUID,
    session: Session = Depends(get_session)
):
    repo = GroupRepository(session)
    members = repo.get_members_by_group_id(group_id)
    return members


@router.get("/list", response_model=list[Groups])
def list_groups(
    session: Session = Depends(get_session)
):
    repo = GroupRepository(session)
    return repo.get_all_groups()