from datetime import datetime
from fastapi import HTTPException, status
from repositories.message_repository import MessageRepository
from repositories.group_repository import GroupRepository
from repositories.user_repository import UserRepository
from sqlmodel import Session
from typing import List
from models.messages import Messages, MessageOut, MessageOutGroup, MessageAtGroupOut
from models.groups import Groups 
import uuid

class MessageService:
    def __init__(self, session: Session):
        self.session = session
        self.message_repo = MessageRepository(session)
        self.group_repo = GroupRepository(session)
        self.user_repo = UserRepository(session)

    def get_last_messages(self, user_id: uuid.UUID, since: datetime) -> List[MessageOutGroup]:
        """ Fetch messages for a user in all groups, starting from a given datetime. """
        # Get the list of groups the user is part of
        groups = self.group_repo.get_all_groups_by_user(user_id)
        if not groups:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No groups found for user")

        # Fetch messages for each group since the provided datetime
        messages: List[MessageOutGroup] = []
        for group in groups:
            group_messages = self.message_repo.get_messages_since(group.id, since)
            group_data = MessageOutGroup(
                group_id=group.id,
                group_name=group.name,
                messages=[
                    MessageAtGroupOut(
                        content=msg.content,
                        sender_id=msg.sender_id,
                        timestamp=msg.timestamp
                    ) 
                    for msg in group_messages
                ]
            )
            messages.append(group_data)
        
        return messages


    def send_message_to_group(self, sender_id: uuid.UUID, group_id: uuid.UUID, content: str) -> MessageOut:
            """ Send a message to a group chat. """

            # Check if the group exists
            group = self.group_repo.get_group_by_id(group_id)
            if not group:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

            # Check if the sender is a member of the group
            if not self.group_repo.is_user_in_group(sender_id, group_id):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a member of this group")

            # Create and save the message
            message = Messages(
                sender_id=sender_id,
                group_id=group_id,
                content=content,
                timestamp=datetime.utcnow()
            )
            self.message_repo.create_message(message)

            return MessageOut(
                group_id=group_id,
                content=content,
                sender_id=sender_id,
                timestamp=message.timestamp
            )
            


    def send_message_to_user(self, sender_id: uuid.UUID, recipient_id: uuid.UUID, content: str) -> MessageOut:
        """ Send a message to a user. Creates a DM group if it doesn't exist. """
        # Check if recipient exists
        recipient = self.user_repo.get_user_by_id(recipient_id)
        if not recipient:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipient not found")

        # Check if a direct message group already exists
        dm_group = self.group_repo.get_direct_message_group(sender_id, recipient_id)
        
        if not dm_group:
            # Create a new direct message group
            dm_group = Groups(
                name=f"DM_{sender_id}_{recipient_id}",
                is_direct=True,
                user_manager=sender_id
            )
            self.group_repo.create_group(dm_group)
            self.group_repo.add_user_to_group(sender_id, dm_group.id)
            self.group_repo.add_user_to_group(recipient_id, dm_group.id)

        # Create and save the message
        message = Messages(
            sender_id=sender_id,
            group_id=dm_group.id,
            content=content,
            timestamp=datetime.utcnow()
        )
        self.message_repo.create_message(message)

        return MessageOut(
            group_id=dm_group.id,
            content=content,
            sender_id=sender_id,
            timestamp=message.timestamp
        )