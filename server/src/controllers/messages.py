from fastapi import APIRouter, Security, Depends
from fastapi.exceptions import HTTPException

from datetime import datetime
import uuid

from core.oauth import get_current_active_user
from core.db import get_session, Session
from models.users import Users
from models.messages import Messages, MessageIn, MessageOut, MessageOutGroup
from services.message_service import MessageService

router = APIRouter(prefix="/msg", tags=["Messages"])


@router.post("/send_message/group/{group_id}", response_model=MessageOut)
def send_message(
    group_id: uuid.UUID,
    body: MessageIn,
    current_user: Users = Security(get_current_active_user),
    session: Session = Depends(get_session),
):
    
    message_service = MessageService(session)
    try:
        message = message_service.send_message_to_group(
            current_user.id, 
            group_id, 
            body.content
        )
    except HTTPException as e:
        raise e
    
    return message


@router.post("/send_message/user/{user_id}", response_model=MessageOut)
def send_direct_message(
    user_id: uuid.UUID,
    body: MessageIn,
    current_user: Users = Security(get_current_active_user),
    session: Session = Depends(get_session),
):
    
    message_service = MessageService(session)
    try:
        message = message_service.send_message_to_user(
            current_user.id, 
            user_id, 
            body.content
        )
    except HTTPException as e:
        raise e
    
    return message


@router.get("/last", response_model=list[MessageOutGroup])
def get_last_messages(
    since: datetime, 
    user: Users = Depends(get_current_active_user), 
    session: Session = Depends(get_session)
):
    """ Endpoint to fetch messages since a certain datetime. """
    message_service = MessageService(session)
    try:
        messages = message_service.get_last_messages(user.id, since)
    except HTTPException as e:
        raise e
    
    return messages
