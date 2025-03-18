from sqlmodel import SQLModel, Field
from pydantic import EmailStr, BaseModel

import datetime
from typing import Optional
import uuid

class UsersBase(SQLModel):
    username: str
    email: EmailStr = Field(index=True, unique=True)
    
    date_joined: datetime.date = Field(
        default_factory=datetime.datetime.now
    )


class Users(UsersBase, table=True):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )
    
    password: bytes
    is_active: bool = Field(default=True)


class UserCreationIn(BaseModel):
    """User creation input model"""
    username: str
    email: EmailStr
    password: str


class UserLoginIn(BaseModel):
    """User login credentials"""
    email: EmailStr
    password: str

class UsersPublic(UsersBase):
    id: uuid.UUID


class AccessTokenModel(BaseModel):
    access_token: str
    # refresh_token: str
    # NÃO IMPLEMENTADO