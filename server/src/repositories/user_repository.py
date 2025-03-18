from sqlmodel import Session, select
from models.users import Users
from models.groups import UserGroupLink
import uuid

from core.security import hash_password, check_password

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def validate_user_creation(self, username: str, email: str) -> bool:
        """ Check if a user with the same username or email already exists. """
        if self.get_user_by_email(email) or self.get_user_by_username(username):
            return False
        return True

    def create_user(self, username: str, email: str, password: str) -> Users:
        """ Create a new user with hashed password. """
        user = Users(username=username, email=email, password=hash_password(password))
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def authenticate_user(self, username: str, password: str) -> Users | None:
        """ Authenticate a user and check if password matches. """
        user = self.session.exec(select(Users).where(Users.username == username)).first()
        if user and check_password(password, user.password):
            return user
        return None

    def get_user_by_id(self, user_id: uuid.UUID) -> Users | None:
        return self.session.get(Users, user_id)

    def get_user_by_username(self, username: str) -> Users | None:
        return self.session.exec(select(Users).where(Users.username == username)).first()

    def get_user_by_email(self, email:str) -> Users | None:
        return self.session.exec(select(Users).where(Users.email == email)).first()

    def get_all_users(self):
        return self.session.exec(select(Users)).all()
    
    def get_user_friends(self, user_id: uuid.UUID) -> list[Users]:
        return self.session.exec(
            select(Users).join(UserGroupLink).where(UserGroupLink.user_id == user_id)
        ).all()

    def delete_user(self, user_id: uuid.UUID):
        user = self.get_user_by_id(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        return False
