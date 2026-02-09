import asyncio
import logging
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, asc
from datetime import datetime
import openai
from openai import AsyncOpenAI
import json

from ..models.conversation import Conversation
from ..models.message import Message, RoleType
from ..core.config import settings
from ..mcp.server import get_mcp_server

# Set up logging
logger = logging.getLogger(__name__)


class ChatService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.mcp_server = get_mcp_server()
        self.mcp_tools = self.mcp_server.get_tools()

    async def process_chat_message(
        self,
        user_id: str,
        user_message: str,
        conversation_id: Optional[str] = None
    ) -> dict:
        """
        Process a chat message from the user and return an AI response.

        Args:
            user_id: The ID of the user sending the message
            user_message: The message content from the user
            conversation_id: Optional ID of existing conversation to continue

        Returns:
            Dictionary containing conversation_id, response, and message_id
        """
        logger.info(f"Processing chat message for user {user_id}")
        logger.info(f"User message: {user_message}")
        logger.info(f"Conversation ID: {conversation_id}")
        
        # Get or create conversation
        if conversation_id:
            logger.info(f"Attempting to use existing conversation: {conversation_id}")
            conversation = await self._get_conversation(conversation_id, user_id)
            if not conversation:
                logger.warning(f"Conversation {conversation_id} not found or doesn't belong to user {user_id}, creating new conversation")
                conversation = await self._create_new_conversation(user_id)
        else:
            logger.info("Creating new conversation")
            conversation = await self._create_new_conversation(user_id)

        # Save user message to database
        logger.info("Saving user message to database")
        user_msg = Message(
            conversation_id=conversation.id,
            role=RoleType.user,
            content=user_message
        )
        self.db.add(user_msg)
        await self.db.commit()
        await self.db.refresh(user_msg)

        # Retrieve full conversation history for context
        logger.info("Retrieving conversation history")
        conversation_history = await self._get_conversation_history(conversation.id)
        logger.info(f"Conversation history has {len(conversation_history)} messages")

        # Generate AI response using the AI service
        logger.info("Generating AI response")
        ai_response = await self._generate_ai_response(conversation_history, user_id)
        logger.info(f"AI response generated: {ai_response}")

        # Save AI response to database
        logger.info("Saving AI response to database")
        ai_msg = Message(
            conversation_id=conversation.id,
            role=RoleType.assistant,
            content=ai_response
        )
        self.db.add(ai_msg)
        await self.db.commit()
        await self.db.refresh(ai_msg)

        # Update conversation timestamp
        logger.info("Updating conversation timestamp")
        conversation.updated_at = datetime.utcnow()
        self.db.add(conversation)
        await self.db.commit()

        result = {
            "conversation_id": conversation.id,
            "response": ai_response,
            "message_id": ai_msg.id
        }
        
        logger.info(f"Returning result: {result}")
        return result

    async def _get_conversation(self, conversation_id: str, user_id: str) -> Optional[Conversation]:
        """Get a specific conversation for a user."""
        query = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def _create_new_conversation(self, user_id: str) -> Conversation:
        """Create a new conversation for the user."""
        conversation = Conversation(user_id=user_id)
        self.db.add(conversation)
        await self.db.commit()
        await self.db.refresh(conversation)
        return conversation

    async def _get_conversation_history(self, conversation_id: str) -> list:
        """Retrieve all messages in a conversation, ordered by creation time."""
        query = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(asc(Message.created_at))
        result = await self.db.execute(query)
        messages = result.scalars().all()

        return [
            {
                "role": msg.role.value,
                "content": msg.content
            } for msg in messages
        ]

    async def _generate_ai_response(self, conversation_history: list, user_id: str) -> str:
        """Generate an AI response based on the conversation history."""
        logger.info(f"Starting AI response generation for user {user_id}")
        logger.info(f"Conversation history: {conversation_history}")
        
        try:
            # Check if the user message contains a task-related request
            # If so, use MCP tools to handle the request
            last_message = conversation_history[-1] if conversation_history else None
            logger.info(f"Last message: {last_message}")
            
            if last_message and self._contains_task_request(last_message.get("content", "")):
                logger.info("Detected task-related request, using MCP tools")
                # Extract task operation from user message
                task_operation = self._extract_task_operation(last_message.get("content", ""))
                logger.info(f"Task operation: {task_operation}")

                if task_operation:
                    # In a real implementation, the agent would call the appropriate MCP tool
                    # For now, we'll simulate the tool call
                    tool_name = task_operation["tool_name"]
                    params = task_operation["params"]
                    logger.info(f"Executing tool: {tool_name} with params: {params}")

                    try:
                        # Execute the appropriate MCP tool based on the tool name
                        if tool_name == "add_task":
                            from ..mcp.tools.add_task import add_task_impl
                            result = await add_task_impl(
                                title=params.get("title"),
                                description=params.get("description"),
                                user_id=user_id
                            )
                        elif tool_name == "list_tasks":
                            from ..mcp.tools.list_tasks import list_tasks_impl
                            result = await list_tasks_impl(
                                filter_param=params.get("filter", "all"),
                                user_id=user_id
                            )
                        elif tool_name == "update_task":
                            from ..mcp.tools.update_task import update_task_impl
                            result = await update_task_impl(
                                task_id=params.get("task_id"),
                                title=params.get("title"),
                                description=params.get("description"),
                                user_id=user_id
                            )
                        elif tool_name == "complete_task":
                            from ..mcp.tools.complete_task import complete_task_impl
                            result = await complete_task_impl(
                                task_id=params.get("task_id"),
                                user_id=user_id
                            )
                        elif tool_name == "delete_task":
                            from ..mcp.tools.delete_task import delete_task_impl
                            result = await delete_task_impl(
                                task_id=params.get("task_id"),
                                user_id=user_id
                            )
                        else:
                            logger.error(f"Unknown tool: {tool_name}")
                            return f"Unknown tool: {tool_name}"

                        logger.info(f"MCP tool result: {result}")
                        
                        # Handle the result based on its type
                        if hasattr(result, 'success') and result.success:
                            # If result is a Pydantic model with success attribute
                            result_dict = result.dict() if hasattr(result, 'dict') else result.__dict__
                            response = self._format_task_success_response(tool_name, result_dict)
                            logger.info(f"Formatted task response: {response}")
                            return response
                        elif isinstance(result, dict) and result.get("success"):
                            # If result is a dictionary with success key
                            response = self._format_task_success_response(tool_name, result)
                            logger.info(f"Formatted task response: {response}")
                            return response
                        else:
                            # Handle error case
                            error_msg = getattr(result, 'error', None) if hasattr(result, 'error') else \
                                       (result.get("error", "Unknown error") if isinstance(result, dict) else "Unknown error")
                            logger.error(f"Tool execution failed: {error_msg}")
                            return f"I tried to perform the requested task, but encountered an error: {error_msg}"
                    except Exception as tool_error:
                        logger.error(f"Error executing MCP tool {tool_name}: {tool_error}", exc_info=True)
                        import traceback
                        traceback.print_exc()
                        return f"I encountered an error while trying to perform the requested task: {str(tool_error)}"

            # If not a task request, check for simple greetings first (fallback without OpenAI)
            user_message_lower = last_message.get("content", "").lower() if last_message else ""

            # Handle common greetings and simple messages without OpenAI
            simple_responses = {
                "hi": "Hey! 😊 How can I help you with your tasks today?",
                "hello": "Hello! 👋 I'm here to help you manage your tasks. What would you like to do?",
                "hey": "Hey there! 😊 Ready to tackle your tasks?",
                "good morning": "Good morning! ☀️ Let's make today productive!",
                "good afternoon": "Good afternoon! 👋 How can I assist you with your tasks?",
                "good evening": "Good evening! 🌙 What can I help you with?",
                "thanks": "You're welcome! 😊 Let me know if you need anything else.",
                "thank you": "Happy to help! 😊 Feel free to ask if you need more assistance.",
                "bye": "Goodbye! 👋 Come back anytime you need help with your tasks!",
                "goodbye": "Take care! 😊 I'll be here when you need me.",
                "help": "I can help you manage your tasks! You can:\n• Add tasks: 'Add a task to buy groceries'\n• List tasks: 'Show my tasks'\n• Complete tasks: 'Mark task as complete'\n• Delete tasks: 'Delete task'\n\nWhat would you like to do?",
                "what can you do": "I'm your todo assistant! 📋 I can help you:\n• ✅ Add new tasks\n• 📝 List your tasks\n• ✏️ Update tasks\n• 🎉 Mark tasks as complete\n• 🗑️ Delete tasks\n\nJust tell me what you need!",
                "how are you": "I'm doing great, thanks for asking! 😊 Ready to help you stay organized!",
                "hi there": "Hi there! 👋 What would you like to accomplish today?"
            }

            # Check for exact matches or close matches
            for key, response in simple_responses.items():
                if user_message_lower.strip() == key or user_message_lower.strip() == key + "!":
                    logger.info(f"Using simple response for '{user_message_lower}'")
                    return response

            # If OpenAI is available, use it for complex queries
            try:
                logger.info("Using OpenAI for general response")
                from backend.src.core.config import settings

                # Add system prompt for better conversational behavior
                system_prompt = {
                    "role": "system",
                    "content": """You are an AI Chat Assistant inside a Todo application.

Your job:
- Reply like a real, helpful assistant in natural language.
- Understand user intent from chat messages.
- If the user asks to add, update, delete, or list a task, respond clearly and confirm the action.
- If the user just says hi or talks normally, reply conversationally.

Rules:
- NEVER reply with only the time.
- NEVER reply with empty text.
- ALWAYS return a helpful text response.
- Do NOT include timestamps unless explicitly asked.
- Be short, clear, and friendly.
- Use emojis occasionally to be more engaging (✅ 📋 🗑️ 😊).

Examples:
User: "hi"
You: "Hey! 😊 How can I help you with your tasks today?"

User: "what tasks do I have?"
You: "📋 Let me check your tasks for you!"

User: "thanks"
You: "You're welcome! Let me know if you need anything else."
"""
                }

                # Prepend system prompt to conversation history
                messages_with_system = [system_prompt] + conversation_history

                response = await self.openai_client.chat.completions.create(
                    model=settings.OPENAI_MODEL or "gpt-3.5-turbo",
                    messages=messages_with_system,
                    max_tokens=settings.OPENAI_MAX_TOKENS or 500,
                    temperature=settings.OPENAI_TEMPERATURE or 0.7
                )

                ai_response = response.choices[0].message.content.strip()
                logger.info(f"OpenAI response: {ai_response}")
                return ai_response
            except Exception as openai_error:
                # If OpenAI fails, return a friendly fallback
                logger.warning(f"OpenAI unavailable, using fallback response: {openai_error}")
                return "I'm here to help you manage your tasks! 😊 Try saying:\n• 'Add a task to [task name]'\n• 'Show my tasks'\n• 'List my tasks'\n\nWhat would you like to do?"
        except Exception as e:
            # Log the error and return a helpful fallback response
            logger.error(f"Error generating AI response: {e}", exc_info=True)
            import traceback
            traceback.print_exc()
            return "I'm here to help! 😊 Try asking me to add, list, update, or delete tasks."

    def _contains_task_request(self, message: str) -> bool:
        """Check if the message contains a task-related request."""
        task_keywords = [
            "add task", "create task", "new task",
            "list tasks", "show tasks", "my tasks",
            "update task", "change task", "edit task",
            "complete task", "finish task", "done task",
            "delete task", "remove task"
        ]
        
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in task_keywords)

    def _extract_task_operation(self, message: str) -> Optional[dict]:
        """Extract the task operation and parameters from the user message."""
        message_lower = message.lower()
        
        # Add task operation
        if any(keyword in message_lower for keyword in ["add task", "create task", "new task"]):
            # Extract title and description from message
            title = self._extract_title_from_message(message)
            description = self._extract_description_from_message(message)
            
            return {
                "tool_name": "add_task",
                "params": {
                    "title": title,
                    "description": description
                }
            }
        
        # List tasks operation
        if any(keyword in message_lower for keyword in ["list tasks", "show tasks", "my tasks"]):
            # Check for filter
            filter_param = "all"
            if "pending" in message_lower:
                filter_param = "pending"
            elif "completed" in message_lower:
                filter_param = "completed"
            
            return {
                "tool_name": "list_tasks",
                "params": {
                    "filter": filter_param
                }
            }
        
        # Update task operation
        if any(keyword in message_lower for keyword in ["update task", "change task", "edit task"]):
            # Extract task ID and new details
            task_id = self._extract_task_id_from_message(message)
            title = self._extract_title_from_message(message)
            description = self._extract_description_from_message(message)
            
            params = {"task_id": task_id}
            if title:
                params["title"] = title
            if description:
                params["description"] = description
                
            return {
                "tool_name": "update_task",
                "params": params
            }
        
        # Complete task operation
        if any(keyword in message_lower for keyword in ["complete task", "finish task", "done task"]):
            task_id = self._extract_task_id_from_message(message)
            
            return {
                "tool_name": "complete_task",
                "params": {
                    "task_id": task_id
                }
            }
        
        # Delete task operation
        if any(keyword in message_lower for keyword in ["delete task", "remove task"]):
            task_id = self._extract_task_id_from_message(message)
            
            return {
                "tool_name": "delete_task",
                "params": {
                    "task_id": task_id
                }
            }
        
        return None

    def _extract_title_from_message(self, message: str) -> str:
        """Extract the task title from the user message."""
        # Simple extraction - in a real implementation, this would be more sophisticated
        # Look for phrases like "to <title>" or "called <title>"
        import re
        
        # Look for patterns like "to buy groceries" or "called 'meeting'"
        patterns = [
            r"(?:to|called|named)\s+(?:\"([^\"]+)\"|\'([^\']+)\'|([^,.!?]+))",
            r"(?:add|create|new)\s+(?:a\s+)?task\s+(?:to|for)\s+(?:\"([^\"]+)\"|\'([^\']+)\'|([^,.!?]+))"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                # Return the first non-None group
                groups = match.groups()
                for group in groups:
                    if group:
                        return group.strip()
        
        return ""

    def _extract_description_from_message(self, message: str) -> str:
        """Extract the task description from the user message."""
        # For simplicity, we'll just return an empty description
        # In a real implementation, this would extract more detailed information
        return ""

    def _extract_task_id_from_message(self, message: str) -> str:
        """Extract the task ID from the user message."""
        # In a real implementation, this would identify the specific task
        # For now, we'll return a placeholder
        return "placeholder_task_id"

    def _format_task_success_response(self, tool_name: str, result: dict) -> str:
        """Format the response for successful task operations."""
        if tool_name == "add_task":
            title = result.get('message', '').split("'")[1] if "'" in result.get('message', '') else 'your task'
            return f"✅ Task added: *{title}*. Let me know if you need anything else!"
        elif tool_name == "list_tasks":
            tasks = result.get("tasks", [])
            count = result.get("count", len(tasks))
            if not tasks:
                return "📋 You don't have any tasks right now. Want to add one?"
            else:
                task_list = "\n".join([f"  • {task.get('title', 'Untitled')} {'✅' if task.get('is_completed') else '⏳'}" for task in tasks])
                return f"📋 You have {count} task{'s' if count != 1 else ''}:\n\n{task_list}"
        elif tool_name == "update_task":
            task = result.get("task", {})
            title = task.get('title', 'Untitled')
            return f"✏️ Updated: *{title}*"
        elif tool_name == "complete_task":
            task = result.get("task", {})
            title = task.get('title', 'Untitled')
            return f"🎉 Great job! Marked *{title}* as completed!"
        elif tool_name == "delete_task":
            message = result.get('message', 'Task deleted')
            return f"🗑️ {message}"
        else:
            return "✅ Task operation completed successfully!"