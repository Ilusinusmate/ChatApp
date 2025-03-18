from sqlmodel import Session, select
from models.messages import Messages
import uuid
from datetime import datetime

class MessageRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_message(self, message: Messages) -> Messages:
        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)
        return message

    def get_message_by_id(self, message_id: uuid.UUID) -> Messages | None:
        return self.session.get(Messages, message_id)

    def get_messages_by_user(self, user_id: uuid.UUID) -> list[Messages]:
        return self.session.exec(select(Messages).where(Messages.user_id == user_id)).all()

    def get_messages_by_group(self, group_id: uuid.UUID)  -> list[Messages]:
        return self.session.exec(select(Messages).where(Messages.group_id == group_id)).all()

    def get_messages_since(self, group_id: uuid.UUID, since: datetime) -> list[Messages]:
        """ Fetch messages for a specific group sent after a certain datetime. """
        statement = select(Messages).where(Messages.group_id == group_id, Messages.timestamp > since)
        return self.session.exec(statement).all()