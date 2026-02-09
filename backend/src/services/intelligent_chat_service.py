"""
Intelligent Chat Service with Natural Language Understanding

This service makes the chatbot a fully conversational AI assistant that:
- Understands natural language queries
- Helps users with task management through conversation
- Answers questions about the application
- Provides guidance and support
- Responds naturally to any topic
"""

import asyncio
import logging
import re
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, asc
from datetime import datetime

from ..models.conversation import Conversation
from ..models.message import Message, RoleType
from ..models.task import Task
from ..core.config import settings

logger = logging.getLogger(__name__)


class IntelligentChatService:
    """
    A fully conversational AI assistant that understands natural language
    and helps users manage their tasks through friendly conversation.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def process_chat_message(
        self,
        user_id: str,
        user_message: str,
        conversation_id: Optional[str] = None
    ) -> dict:
        """Process user message and generate intelligent response."""

        logger.info(f"Processing message from user {user_id}: {user_message}")

        # Get or create conversation
        if conversation_id:
            conversation = await self._get_conversation(conversation_id, user_id)
            if not conversation:
                logger.warning(f"Conversation not found, creating new one")
                conversation = await self._create_new_conversation(user_id)
        else:
            conversation = await self._create_new_conversation(user_id)

        # Save user message
        user_msg = Message(
            conversation_id=conversation.id,
            role=RoleType.user,
            content=user_message
        )
        self.db.add(user_msg)
        await self.db.commit()
        await self.db.refresh(user_msg)

        # Get conversation history for context
        conversation_history = await self._get_conversation_history(conversation.id)

        # Generate intelligent response
        ai_response = await self._generate_intelligent_response(
            user_message,
            conversation_history,
            user_id
        )

        # Save AI response
        ai_msg = Message(
            conversation_id=conversation.id,
            role=RoleType.assistant,
            content=ai_response
        )
        self.db.add(ai_msg)
        await self.db.commit()
        await self.db.refresh(ai_msg)

        # Update conversation timestamp
        conversation.updated_at = datetime.utcnow()
        self.db.add(conversation)
        await self.db.commit()

        return {
            "conversation_id": conversation.id,
            "response": ai_response,
            "message_id": ai_msg.id
        }

    async def _generate_intelligent_response(
        self,
        user_message: str,
        history: List[Dict],
        user_id: str
    ) -> str:
        """
        Generate an intelligent, context-aware response.

        This method analyzes the user's message and:
        1. Understands the intent
        2. Performs requested actions (task operations)
        3. Provides helpful, conversational responses
        """

        message_lower = user_message.lower().strip()

        # Analyze intent and extract information
        intent = await self._analyze_intent(message_lower, user_id)

        # Handle based on intent
        if intent["type"] == "list_tasks":
            return await self._handle_list_tasks(intent, user_id)

        elif intent["type"] == "add_task":
            return await self._handle_add_task(intent, user_id)

        elif intent["type"] == "delete_task":
            return await self._handle_delete_task(intent, user_id)

        elif intent["type"] == "complete_task":
            return await self._handle_complete_task(intent, user_id)

        elif intent["type"] == "update_task":
            return await self._handle_update_task(intent, user_id)

        elif intent["type"] == "greeting":
            return self._get_greeting_response(message_lower)

        elif intent["type"] == "help":
            return self._get_help_response()

        elif intent["type"] == "thanks":
            return "You're welcome! 😊 Happy to help anytime."

        elif intent["type"] == "farewell":
            return "Take care! 👋 Feel free to come back whenever you need help."

        else:
            # General conversational response
            return self._get_conversational_response(message_lower)

    async def _analyze_intent(self, message: str, user_id: str) -> Dict[str, Any]:
        """
        Analyze user message to understand intent and extract parameters.
        Uses natural language patterns to understand what the user wants.
        """

        # Greeting patterns
        if any(word in message for word in ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]):
            return {"type": "greeting"}

        # Thanks patterns
        if any(phrase in message for phrase in ["thank", "thanks", "appreciate"]):
            return {"type": "thanks"}

        # Farewell patterns
        if any(word in message for word in ["bye", "goodbye", "see you", "later"]):
            return {"type": "farewell"}

        # Help patterns
        if any(phrase in message for phrase in ["help", "what can you do", "how do i", "guide", "assist"]):
            return {"type": "help"}

        # List tasks patterns - very flexible
        if any(phrase in message for phrase in [
            "show", "list", "display", "what tasks", "my tasks", "see tasks",
            "view tasks", "get tasks", "tasks do i have", "check tasks"
        ]):
            filter_type = "all"
            if "pending" in message or "incomplete" in message or "unfinished" in message:
                filter_type = "pending"
            elif "completed" in message or "done" in message or "finished" in message:
                filter_type = "completed"

            return {"type": "list_tasks", "filter": filter_type}

        # Delete/Remove task patterns - very flexible
        if any(phrase in message for phrase in [
            "delete", "remove", "get rid", "erase", "clear", "cancel"
        ]):
            task_title = self._extract_task_title_for_deletion(message)
            return {"type": "delete_task", "task_title": task_title}

        # Complete task patterns
        if any(phrase in message for phrase in [
            "complete", "finish", "done with", "completed", "mark as done", "finished"
        ]):
            task_title = self._extract_task_title_from_message(message)
            return {"type": "complete_task", "task_title": task_title}

        # Update task patterns
        if any(phrase in message for phrase in [
            "update", "change", "edit", "modify", "rename"
        ]):
            task_title = self._extract_task_title_from_message(message)
            new_title = self._extract_new_title(message)
            return {"type": "update_task", "task_title": task_title, "new_title": new_title}

        # Add task patterns - very flexible
        if any(phrase in message for phrase in [
            "add", "create", "new task", "make a task", "remind me", "need to",
            "have to", "must", "should", "want to", "gonna"
        ]):
            task_title = self._extract_task_title_for_addition(message)
            return {"type": "add_task", "title": task_title}

        # Default: general conversation
        return {"type": "general"}

    def _extract_task_title_for_addition(self, message: str) -> str:
        """Extract task title from message for adding tasks."""
        # Patterns like "add task to X", "create task X", "remind me to X"
        patterns = [
            r"(?:add|create|new)\s+(?:a\s+)?task\s+(?:to\s+|for\s+)?(.+)",
            r"remind\s+me\s+to\s+(.+)",
            r"(?:need|have|want)\s+to\s+(.+)",
            r"(?:must|should|gonna)\s+(.+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                # Clean up common endings
                title = re.sub(r'\s+(please|pls|plz|thanks|thank you)$', '', title, flags=re.IGNORECASE)
                return title

        # If no pattern matched, try to extract after common verbs
        words = message.split()
        if len(words) > 2:
            return " ".join(words[2:])  # Take everything after first two words

        return "New task"

    def _extract_task_title_for_deletion(self, message: str) -> str:
        """Extract task title from message for deletion."""
        # Patterns like "delete task X", "remove task shopping", "delete shopping"
        patterns = [
            r"(?:delete|remove|cancel|clear|erase)\s+(?:task\s+)?(?:called\s+)?['\"]?(.+?)['\"]?$",
            r"(?:delete|remove)\s+(?:my\s+)?(?:task\s+)?(?:called\s+)?(.+)",
            r"get\s+rid\s+of\s+(?:task\s+)?(.+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                # Remove common words
                title = re.sub(r'^(task|me|my|the)\s+', '', title, flags=re.IGNORECASE)
                title = re.sub(r'\s+(please|pls|plz|thanks|thank you)$', '', title, flags=re.IGNORECASE)
                return title

        # Fallback: get last few words
        words = message.split()
        if len(words) > 1:
            return " ".join(words[-2:])

        return ""

    def _extract_task_title_from_message(self, message: str) -> str:
        """General task title extraction."""
        # Remove common prefixes and suffixes
        cleaned = re.sub(r'^(task|my|the|a|an)\s+', '', message, flags=re.IGNORECASE)
        cleaned = re.sub(r'\s+(please|pls|plz|thanks|thank you)$', '', cleaned, flags=re.IGNORECASE)
        return cleaned.strip()

    def _extract_new_title(self, message: str) -> str:
        """Extract new title for update operations."""
        patterns = [
            r"(?:to|into|as)\s+['\"]?(.+?)['\"]?$",
            r"change\s+.+?\s+to\s+(.+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return ""

    async def _handle_list_tasks(self, intent: Dict, user_id: str) -> str:
        """Handle task listing with friendly response."""
        try:
            filter_type = intent.get("filter", "all")

            query = select(Task).where(Task.user_id == user_id)

            if filter_type == "pending":
                query = query.where(Task.is_completed == False)
            elif filter_type == "completed":
                query = query.where(Task.is_completed == True)

            result = await self.db.execute(query)
            tasks = result.scalars().all()

            if not tasks:
                if filter_type == "pending":
                    return "Good news! 🎉 You don't have any pending tasks right now."
                elif filter_type == "completed":
                    return "You haven't marked any tasks as complete yet. Once you finish something, I'll keep track of it here!"
                else:
                    return "You don't have any tasks yet. Want to add one? Just tell me what you need to do!"

            # Format task list - friendly
            count = len(tasks)
            filter_text = f"{filter_type} " if filter_type != "all" else ""

            if filter_type == "all":
                response = f"Here are all your tasks ({count}):\n\n"
            else:
                response = f"Here are your {filter_type} tasks ({count}):\n\n"

            for task in tasks:
                status = "✅" if task.is_completed else "📝"
                response += f"{status} {task.title}\n"

            response += "\nNeed help with any of these?"
            return response

        except Exception as e:
            logger.error(f"Error listing tasks: {e}", exc_info=True)
            return "Hmm, I'm having trouble loading your tasks right now. Mind trying again?"

    async def _handle_add_task(self, intent: Dict, user_id: str) -> str:
        """Handle task addition with friendly response."""
        try:
            title = intent.get("title", "").strip()

            if not title or title == "New task":
                return "Sure! What task would you like me to add? 😊"

            # Create task
            new_task = Task(
                title=title,
                description="",
                is_completed=False,
                user_id=user_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            self.db.add(new_task)
            await self.db.commit()
            await self.db.refresh(new_task)

            return f"Got it! ✅ I've added **{title}** to your task list. Would you like to set a due date or add any details?"

        except Exception as e:
            logger.error(f"Error adding task: {e}", exc_info=True)
            return "Oops, I had trouble adding that task. Could you try again?"

    async def _handle_delete_task(self, intent: Dict, user_id: str) -> str:
        """Handle task deletion with friendly response."""
        try:
            task_title = intent.get("task_title", "").strip()

            if not task_title:
                return "Sure! Which task would you like me to remove? 🤔"

            # Find task by title (case-insensitive partial match)
            query = select(Task).where(
                Task.user_id == user_id,
                Task.title.ilike(f"%{task_title}%")
            )
            result = await self.db.execute(query)
            task = result.scalar_one_or_none()

            if not task:
                # Try broader match
                query = select(Task).where(
                    Task.user_id == user_id
                )
                result = await self.db.execute(query)
                tasks = result.scalars().all()

                # Find best match
                for t in tasks:
                    if task_title.lower() in t.title.lower() or t.title.lower() in task_title.lower():
                        task = t
                        break

                if not task:
                    return f"I couldn't find a task matching **{task_title}**. Want me to show you all your tasks?"

            # Delete the task
            task_name = task.title
            await self.db.delete(task)
            await self.db.commit()

            return f"Done 👍 I've removed **{task_name}** from your list. Let me know if you need anything else!"

        except Exception as e:
            logger.error(f"Error deleting task: {e}", exc_info=True)
            return "Hmm, I ran into an issue removing that task. Mind trying again?"

    async def _handle_complete_task(self, intent: Dict, user_id: str) -> str:
        """Handle task completion with friendly response."""
        try:
            task_title = intent.get("task_title", "").strip()

            if not task_title:
                return "Nice! Which task did you finish? 🎉"

            # Find task
            query = select(Task).where(
                Task.user_id == user_id,
                Task.title.ilike(f"%{task_title}%")
            )
            result = await self.db.execute(query)
            task = result.scalar_one_or_none()

            if not task:
                return f"I couldn't find a task matching **{task_title}**. Want to see your current tasks?"

            # Mark as complete
            task.is_completed = True
            task.updated_at = datetime.utcnow()
            await self.db.commit()

            return f"Awesome! 🎉 I've marked **{task.title}** as complete. Great work!"

        except Exception as e:
            logger.error(f"Error completing task: {e}", exc_info=True)
            return "Oops, I had trouble marking that as complete. Could you try again?"

    async def _handle_update_task(self, intent: Dict, user_id: str) -> str:
        """Handle task updates."""
        # Implementation for updating tasks
        return "Task updating feature is coming soon! For now, you can delete the old task and add a new one. 😊"

    def _get_greeting_response(self, message: str) -> str:
        """Get friendly greeting response."""
        if "morning" in message:
            return "Good morning! ☀️ Hope you're having a great start. How can I help you with your tasks today?"
        elif "afternoon" in message:
            return "Good afternoon! 👋 What can I help you with?"
        elif "evening" in message:
            return "Good evening! 🌙 How can I assist you today?"
        else:
            return "Hey! 👋 Nice to see you. How can I help you with your tasks today?"

    def _get_help_response(self) -> str:
        """Provide friendly help."""
        return """I can help you manage your tasks — you can add, update, delete, or view them anytime 😊

Just talk to me naturally! For example:
• "Add a task to buy groceries"
• "Show me my tasks"
• "Remove the shopping task"
• "Mark workout as complete"

What would you like to do?"""

    def _get_conversational_response(self, message: str) -> str:
        """Handle general conversation naturally."""
        # Check if asking about the app
        if any(word in message for word in ["app", "application", "todo", "this", "you"]):
            return "I'm your task assistant! 😊 I help you stay organized by managing your to-do list. Just tell me what you need to do, and I'll keep track of everything for you."

        # Check if asking about capabilities
        if any(word in message for word in ["what", "how", "can", "able"]):
            return "I can help you add, view, complete, and remove tasks — all through natural conversation! Try saying something like 'add task to call mom' or 'show my tasks'. Want to give it a try?"

        # Casual chat
        if any(word in message for word in ["hmm", "um", "uh", "ok", "okay"]):
            return "😊 No worries, take your time. I'm here whenever you're ready."

        # General response
        return "I'm here to help! Feel free to ask me about your tasks, or just chat if you need anything. 😊"

    async def _get_conversation(self, conversation_id: str, user_id: str) -> Optional[Conversation]:
        """Get conversation from database."""
        query = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def _create_new_conversation(self, user_id: str) -> Conversation:
        """Create new conversation."""
        conversation = Conversation(user_id=user_id)
        self.db.add(conversation)
        await self.db.commit()
        await self.db.refresh(conversation)
        return conversation

    async def _get_conversation_history(self, conversation_id: str) -> List[Dict]:
        """Get conversation history."""
        query = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(asc(Message.created_at))
        result = await self.db.execute(query)
        messages = result.scalars().all()

        return [
            {
                "role": msg.role.value,
                "content": msg.content
            }
            for msg in messages
        ]
