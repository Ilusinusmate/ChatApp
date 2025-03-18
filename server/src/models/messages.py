from sqlmodel import SQLModel, Field

import uuid
from datetime import datetime

class Messages(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    sender_id: uuid.UUID = Field(foreign_key="users.id")
    group_id: uuid.UUID = Field(foreign_key="groups.id", nullable=True)
    content: str = Field(nullable=False)
    timestamp: datetime = Field(default_factory=datetime.now, index=True)


class MessageIn(SQLModel):
    content: str

class MessageOut(SQLModel):
    group_id: uuid.UUID | None
    sender_id: uuid.UUID
    content: str
    timestamp: datetime

class MessageAtGroupOut(SQLModel):
    sender_id: uuid.UUID
    content: str
    timestamp: datetime

class MessageOutGroup(SQLModel):
    group_id: uuid.UUID
    group_name: str
    messages: list[MessageAtGroupOut]