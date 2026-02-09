from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import TYPE_CHECKING, Optional
import uuid

if TYPE_CHECKING:
    from .message import Message


class ConversationBase(SQLModel):
    user_id: str = Field(index=True)
    title: Optional[str] = Field(default=None)


class Conversation(ConversationBase, table=True):
    __tablename__ = "conversations"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to messages
    messages: list["Message"] = Relationship(back_populates="conversation")


class ConversationRead(ConversationBase):
    id: str
    created_at: datetime
    updated_at: datetime