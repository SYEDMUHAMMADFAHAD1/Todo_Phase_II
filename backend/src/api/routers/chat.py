import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import uuid

from ...core.config import settings
from ...core.db import get_session
from ...models.conversation import Conversation, ConversationRead
from ...models.message import Message, MessageRead, RoleType
from ...services.intelligent_chat_service import IntelligentChatService
from ..deps import get_current_user
from auth import UserIdentity as User
from pydantic import BaseModel
from sqlalchemy import select, asc

# Set up logging
logger = logging.getLogger(__name__)

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

router = APIRouter(prefix="/{user_id}", tags=["chat"])

@router.post("/chat", response_model=dict)
async def chat(
    user_id: str,
    request: ChatRequest,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Send a message to the chatbot and receive a response.

    Creates a new conversation if none exists, or appends to existing conversation.
    Returns the AI assistant's response.
    """
    # Log request received
    logger.info(f"Chat request received for user_id: {user_id}")
    logger.info(f"Request body: {request}")
    logger.info(f"Authenticated user: {current_user.id if current_user else 'None'}")

    # Verify that the user_id in the path matches the authenticated user
    if current_user.id != user_id:
        logger.error(f"User ID mismatch: path user_id={user_id}, authenticated user_id={current_user.id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user ID mismatch"
        )

    try:
        chat_service = IntelligentChatService(db)

        # Log AI request preparation
        logger.info(f"Preparing to process chat message for user {user_id}")

        # Process the chat request and get response
        result = await chat_service.process_chat_message(
            user_id=user_id,
            user_message=request.message,
            conversation_id=request.conversation_id
        )

        # Log AI response received
        logger.info(f"Successfully processed chat message, result: {result}")

        return result
    except Exception as e:
        # Log error with full stack trace
        logger.error(f"Error processing chat message: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat message: {str(e)}"
        )


@router.get("/conversations/{conversation_id}/messages")
async def get_conversation_messages(
    user_id: str,
    conversation_id: str,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get all messages from a specific conversation.
    """
    # Verify user_id matches
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user ID mismatch"
        )

    try:
        # First verify the conversation belongs to the user
        conv_query = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        conv_result = await db.execute(conv_query)
        conversation = conv_result.scalar_one_or_none()

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )

        # Get all messages for this conversation
        msg_query = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(asc(Message.created_at))

        msg_result = await db.execute(msg_query)
        messages = msg_result.scalars().all()

        # Format messages for frontend
        formatted_messages = [
            {
                "id": str(msg.id),
                "role": msg.role.value,
                "content": msg.content,
                "timestamp": msg.created_at.isoformat() if msg.created_at else None
            }
            for msg in messages
        ]

        return {
            "conversation_id": conversation_id,
            "messages": formatted_messages
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching conversation messages: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching messages: {str(e)}"
        )
    #     )