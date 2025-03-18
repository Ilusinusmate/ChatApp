from sqlmodel import Session, select
from models.groups import Groups, UserGroupLink
from models.users import Users
import uuid

class GroupRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_group(self, group: Groups) -> Groups:
        self.session.add(group)
        self.session.commit()
        self.session.refresh(group)
        return group

    def get_group_by_id(self, group_id: uuid.UUID) -> Groups | None:
        return self.session.get(Groups, group_id)

    def get_group_info_by_id(self, group_id: uuid.UUID) -> Groups | None:
        """ Fetch group information with members """
        return self.session.exec(
            select(Users).join(UserGroupLink).where(UserGroupLink.group_id == group_id)
        ).first()
    
    def get_members_by_group_id(self, group_id: uuid.UUID) -> list[Users]:
        return self.session.exec(
            select(Users).where(
                UserGroupLink.user_id == Users.id,
                UserGroupLink.group_id == group_id
            )
        ).all()

    def get_group_by_name(self, name: str) -> Groups | None:
        return self.session.exec(select(Groups).where(Groups.name == name)).first()

    def get_all_groups(self) -> list[Groups]:
        return self.session.exec(select(Groups)).all()

    def get_all_groups_by_user(self, user_id: uuid.UUID) -> list[Groups]:
        return self.session.exec(
            select(Groups).join(UserGroupLink).where(UserGroupLink.user_id == user_id)
        ).all()
    
    def get_direct_message_group(self, user_id1: uuid.UUID, user_id2: uuid.UUID) -> Groups | None:
        """Find a direct message group between two users."""
        statement = (
            select(Groups)
            .join(UserGroupLink, UserGroupLink.group_id == Groups.id)
            .where(
                Groups.is_direct == True
            )
            .where(
                UserGroupLink.user_id == user_id1
            )
            .where(
                UserGroupLink.group_id.in_(
                    select(UserGroupLink.group_id)
                    .where(UserGroupLink.user_id == user_id2)
                )
            )
        )
        return self.session.exec(statement).first()

    def is_user_in_group(self, user_id: uuid.UUID, group_id: uuid.UUID) -> bool:
        link = self.session.exec(
            select(UserGroupLink).where(
                UserGroupLink.user_id == user_id, UserGroupLink.group_id == group_id
            )
        ).first()
        return link is not None

    def add_user_to_group(self, user_id: uuid.UUID, group_id: uuid.UUID) -> None:
        link = UserGroupLink(user_id=user_id, group_id=group_id)
        self.session.add(link)
        self.session.commit()

    def remove_user_from_group(self, user_id: uuid.UUID, group_id: uuid.UUID) -> bool:
        link = self.session.exec(
            select(UserGroupLink).where(
                UserGroupLink.user_id == user_id, UserGroupLink.group_id == group_id
            )
        ).first()
        if link:
            self.session.delete(link)
            self.session.commit()
            return True
        return False
