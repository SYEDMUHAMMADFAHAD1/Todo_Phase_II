from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import TEXT as sa_text
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional
import uuid

if TYPE_CHECKING:
    from .conversation import Conversation


class RoleType(str, Enum):
    user = "user"
    assistant = "assistant"


class MessageBase(SQLModel):
    conversation_id: str = Field(foreign_key="conversations.id", index=True)
    role: RoleType = Field(sa_column_kwargs={"name": "role"})
    content: str = Field(sa_column=sa_text)


class Message(MessageBase, table=True):
    __tablename__ = "messages"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to conversation
    conversation: "Conversation" = Relationship(back_populates="messages")


class MessageRead(MessageBase):
    id: str
    created_at: datetime
    updated_at: datetime