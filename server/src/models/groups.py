from sqlmodel import SQLModel, Field, Relationship

from typing import List, Optional
import uuid

class Groups(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    name: str = Field(unique=True, index=True, nullable=False)
    user_manager: uuid.UUID = Field(foreign_key="users.id", primary_key=True)
    is_direct: bool = Field(default=False)

class UserGroupLink(SQLModel, table=True):
    user_id: uuid.UUID = Field(foreign_key="users.id", primary_key=True)
    group_id: uuid.UUID = Field(foreign_key="groups.id", primary_key=True)
