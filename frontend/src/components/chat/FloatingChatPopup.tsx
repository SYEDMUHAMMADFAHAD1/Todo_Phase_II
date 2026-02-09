'use client';

import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '@/contexts/auth-context';
import { apiClient } from '@/lib/api-client';
import { nanoid } from 'nanoid';
import { useCalendarPicker } from '@/contexts/CalendarPickerContext';
import { useTodo } from '@/hooks/todo';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface FloatingChatPopupProps {
  onClose: () => void;
}

const FloatingChatPopup: React.FC<FloatingChatPopupProps> = ({ onClose }) => {
  const { user } = useAuth();
  const { showCalendarPicker, setShowCalendarPicker, taskTitle, setTaskTitle, taskDescription, setTaskDescription } = useCalendarPicker();
  const todo = useTodo();
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [showSuggestions, setShowSuggestions] = useState(true);
  const [pendingUpdateTask, setPendingUpdateTask] = useState<{taskId: string, field: string} | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Load conversation history from localStorage when component mounts
  useEffect(() => {
    if (user) {
      const savedConversation = localStorage.getItem(`chatHistory_${user.id}`);
      if (savedConversation) {
        try {
          const parsedMessages = JSON.parse(savedConversation, (key, value) => {
            if (key === 'timestamp') return new Date(value);
            return value;
          });
          setMessages(parsedMessages);
          
          // Get conversation ID from the first message or localStorage
          if (parsedMessages.length > 0) {
            const savedConvId = localStorage.getItem(`currentChatConversationId_${user.id}`);
            if (savedConvId) {
              setConversationId(savedConvId);
            }
            setShowSuggestions(false); // Hide suggestions if there are previous messages
          }
        } catch (e) {
          console.error('Error parsing saved chat history:', e);
          // Clear corrupted data
          localStorage.removeItem(`chatHistory_${user.id}`);
          localStorage.removeItem(`currentChatConversationId_${user.id}`);
        }
      }
    }
  }, [user]);

  // Save conversation history to localStorage whenever messages change
  useEffect(() => {
    if (user && messages.length > 0) {
      localStorage.setItem(`chatHistory_${user.id}`, JSON.stringify(messages, (key, value) => 
        typeof value === 'object' && value instanceof Date ? value.toISOString() : value
      ));
    }
  }, [messages, user]);

  // Scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSend = async () => {
    if (!inputValue.trim() || isLoading || !user) return;

    const userMessage: Message = {
      id: nanoid(),
      role: 'user',
      content: inputValue,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);
    setShowSuggestions(false); // Hide suggestions once conversation starts

    try {
      // Check if this is a task creation request
      const userMessageContent = inputValue.toLowerCase();
      if (userMessageContent.includes('add') || userMessageContent.includes('create') || userMessageContent.includes('new task')) {
        // Extract task title from the message
        const taskMatch = inputValue.match(/(?:add|create|new task)[:\-\s]*(.*)/i);
        const extractedTaskTitle = taskMatch ? taskMatch[1].trim() : "New Task";

        // Set the task title in the context
        setTaskTitle(extractedTaskTitle);
        setTaskDescription('');

        // Show the calendar picker UI
        setShowCalendarPicker(true);

        // Inform the user that they need to select date/time
        const aiMessage: Message = {
          id: nanoid(),
          role: 'assistant',
          content: `Sure! I'll help you create "${extractedTaskTitle}". Please select the date and time using the calendar picker that has appeared on the dashboard.`,
          timestamp: new Date(),
        };

        setMessages(prev => [...prev, aiMessage]);
      } else if (pendingUpdateTask) {
        // Handle pending task update - user is providing the new value
        const taskId = pendingUpdateTask.taskId;
        const fieldToUpdate = pendingUpdateTask.field;

        // Find the task to update
        const taskToUpdate = todo.todos.find(t => t.id === taskId);

        if (taskToUpdate) {
          let updateData: any = {};
          const newValue = inputValue.trim();

          if (fieldToUpdate === 'title') {
            updateData.title = newValue;
          } else if (fieldToUpdate === 'description') {
            updateData.description = newValue;
          }

          try {
            // Update the task
            await todo.updateTodo(taskId, updateData);

            const oldValue = fieldToUpdate === 'title' ? taskToUpdate.title : (taskToUpdate.description || 'none');
            const aiMessage: Message = {
              id: nanoid(),
              role: 'assistant',
              content: `Perfect! 👍\n\nI've updated your task **"${taskToUpdate.title}"** ${fieldToUpdate === 'title' ? 'title' : 'description'} from **"${oldValue}"** to **"${newValue}"**.\n\nIs there anything else you'd like to change?`,
              timestamp: new Date(),
            };

            setMessages(prev => [...prev, aiMessage]);
            setPendingUpdateTask(null);
          } catch (updateErr) {
            const aiMessage: Message = {
              id: nanoid(),
              role: 'assistant',
              content: `Oops! I had trouble updating your task. The error was: ${updateErr instanceof Error ? updateErr.message : 'Unknown error'}.\n\nPlease try again or let me know if you need help.`,
              timestamp: new Date(),
            };

            setMessages(prev => [...prev, aiMessage]);
            setPendingUpdateTask(null);
          }
        } else {
          const aiMessage: Message = {
            id: nanoid(),
            role: 'assistant',
            content: "Hmm, I couldn't find that task anymore. It may have been deleted.\n\nLet me know which task you'd like to edit.",
            timestamp: new Date(),
          };

          setMessages(prev => [...prev, aiMessage]);
          setPendingUpdateTask(null);
        }
      } else if (userMessageContent.includes('edit') || userMessageContent.includes('update') || userMessageContent.includes('change') || userMessageContent.includes('modify')) {
        // Handle task update request
        let targetTask = null;

        // Strategy 1: Try to find task by matching title keywords in the message
        // Extract potential task title from common patterns like "edit task X" or "update X"
        const taskTitleMatch = inputValue.match(/(?:edit|update|change|modify)\s+(?:task\s+)?(?:"|')?(.+?)(?:"|')?\s*(?:to|not|from|with)?/i);
        if (taskTitleMatch) {
          const potentialTitle = taskTitleMatch[1].trim().toLowerCase();
          targetTask = todo.todos.find(t =>
            t.title.toLowerCase().includes(potentialTitle) ||
            potentialTitle.includes(t.title.toLowerCase())
          );
        }

        // Strategy 2: If not found, try matching against all words in the message
        if (!targetTask) {
          const words = inputValue.split(/\s+/).filter(w => w.length > 3);
          for (const word of words) {
            const cleanWord = word.toLowerCase().replace(/[^a-z0-9]/g, '');
            const foundTask = todo.todos.find(t =>
              t.title.toLowerCase().includes(cleanWord) ||
              (t.description && t.description.toLowerCase().includes(cleanWord))
            );
            if (foundTask) {
              targetTask = foundTask;
              break;
            }
          }
        }

        // Strategy 3: If still not found, check for "last" or "recent" keywords
        if (!targetTask && (userMessageContent.includes('last') || userMessageContent.includes('recent') || userMessageContent.includes('previous'))) {
          const incompleteTasks = todo.todos.filter(t => !t.is_completed);
          if (incompleteTasks.length > 0) {
            targetTask = incompleteTasks[incompleteTasks.length - 1];
          }
        }

        // Strategy 4: Default to most recent pending task
        if (!targetTask && todo.todos.length > 0) {
          const incompleteTasks = todo.todos.filter(t => !t.is_completed);
          if (incompleteTasks.length > 0) {
            targetTask = incompleteTasks[incompleteTasks.length - 1];
          } else {
            targetTask = todo.todos[todo.todos.length - 1];
          }
        }

        if (targetTask) {
          // Determine what field to update and extract the new value
          let fieldToUpdate = 'title'; // Default
          let newValue = '';

          // Check if updating date/time
          if (userMessageContent.includes('date') || userMessageContent.includes('time') || userMessageContent.includes('when')) {
            fieldToUpdate = 'date_time';
            setTaskTitle(targetTask.title);
            setTaskDescription(targetTask.description || '');
            setShowCalendarPicker(true);

            const aiMessage: Message = {
              id: nanoid(),
              role: 'assistant',
              content: `Got it 👍\n\nI'll help you update the date and time for **"${targetTask.title}"**.\n\nPlease select the new date and time using the calendar picker that just appeared on the dashboard.`,
              timestamp: new Date(),
            };
            setMessages(prev => [...prev, aiMessage]);
            return; // Exit early
          }

          // Check if updating description
          if (userMessageContent.includes('description') || userMessageContent.includes('desc') || userMessageContent.includes('details')) {
            fieldToUpdate = 'description';
          }

          // Extract new value using various patterns
          // Pattern 1: "edit X to Y" or "change X to Y"
          const toPattern = inputValue.match(/(?:to|into)\s+["']?([^"']+)["']?$/i);
          if (toPattern) {
            newValue = toPattern[1].trim();
          }

          // Pattern 2: "edit X not Y" (detect "not" keyword as separator)
          if (!newValue) {
            const notPattern = inputValue.match(/not\s+(.+)$/i);
            if (notPattern) {
              newValue = notPattern[1].trim();
            }
          }

          // Pattern 3: Extract everything after task title
          if (!newValue) {
            const taskTitleInMsg = targetTask.title.toLowerCase();
            const msgLower = inputValue.toLowerCase();
            const titleIndex = msgLower.indexOf(taskTitleInMsg);
            if (titleIndex !== -1) {
              const afterTitle = inputValue.substring(titleIndex + targetTask.title.length).trim();
              // Remove common words
              newValue = afterTitle.replace(/^(to|into|not|with)\s+/i, '').trim();
            }
          }

          // If we extracted a new value, update the task
          if (newValue && newValue.length > 0) {
            try {
              let updateData: any = {};
              updateData[fieldToUpdate] = newValue;

              await todo.updateTodo(targetTask.id, updateData);

              const oldValue = fieldToUpdate === 'title' ? targetTask.title : (targetTask.description || 'none');
              const aiMessage: Message = {
                id: nanoid(),
                role: 'assistant',
                content: `Got it 👍\n\nI've updated your task **"${targetTask.title}"** ${fieldToUpdate === 'title' ? 'title' : 'description'} from **"${oldValue}"** to **"${newValue}"**.\n\nWant to change the date or time as well?`,
                timestamp: new Date(),
              };
              setMessages(prev => [...prev, aiMessage]);
            } catch (updateErr) {
              const aiMessage: Message = {
                id: nanoid(),
                role: 'assistant',
                content: `Oops! I had trouble updating your task. The error was: ${updateErr instanceof Error ? updateErr.message : 'Unknown error'}.\n\nPlease try again or let me know if you need help.`,
                timestamp: new Date(),
              };
              setMessages(prev => [...prev, aiMessage]);
            }
          } else {
            // Need clarification from user
            setPendingUpdateTask({ taskId: targetTask.id, field: fieldToUpdate });

            const aiMessage: Message = {
              id: nanoid(),
              role: 'assistant',
              content: `I found the task **"${targetTask.title}"**.\n\nWhat would you like to change the ${fieldToUpdate === 'title' ? 'title' : 'description'} to?`,
              timestamp: new Date(),
            };
            setMessages(prev => [...prev, aiMessage]);
          }
        } else {
          const aiMessage: Message = {
            id: nanoid(),
            role: 'assistant',
            content: "Hmm, I couldn't find the task you want to update.\n\nCould you please tell me more about which task you'd like to edit? You can mention:\n- The task title\n- Or say 'last task' or 'recent task'",
            timestamp: new Date(),
          };
          setMessages(prev => [...prev, aiMessage]);
        }
      } else {
        // Send the message to our backend API for general chat
        // Simulate thinking time for more human-like interaction
        await new Promise(resolve => setTimeout(resolve, 1000));

        const response = await apiClient.sendChatMessage(
          user.id,
          inputValue,
          conversationId || undefined
        );

        // Update conversation ID if it's the first message
        if (!conversationId) {
          setConversationId(response.conversation_id);
          localStorage.setItem(`currentChatConversationId_${user.id}`, response.conversation_id);
        }

        // Add the AI response to messages
        const aiMessage: Message = {
          id: response.message_id || nanoid(),
          role: 'assistant',
          content: response.response,
          timestamp: new Date(),
        };

        setMessages(prev => [...prev, aiMessage]);
      }
    } catch (err: any) {
      // Handle common tasks without backend if API fails
      const userMessageContent = inputValue.toLowerCase();
      let aiResponse = '';

      if (userMessageContent.includes('hello') || userMessageContent.includes('hi') || userMessageContent.includes('hey')) {
        aiResponse = "Hey! 👋 Hope you're doing well. How can I help you with your tasks today?";
      } else if (userMessageContent.includes('thank') || userMessageContent.includes('thanks')) {
        aiResponse = "You're very welcome! 😊 Let me know if there's anything else I can assist with.";
      } else if (userMessageContent.includes('add') || userMessageContent.includes('create') || userMessageContent.includes('new task')) {
        // Extract task title from the message
        const taskMatch = inputValue.match(/(?:add|create|new task)[:\-\s]*(.*)/i);
        const extractedTaskTitle = taskMatch ? taskMatch[1].trim() : "New Task";

        // Set the task title in the context
        setTaskTitle(extractedTaskTitle);
        setTaskDescription('');

        // Show the calendar picker UI
        setShowCalendarPicker(true);

        aiResponse = `Sure! I'll help you create "${extractedTaskTitle}". Please select the date and time using the calendar picker that has appeared on the dashboard.`;
      } else if (userMessageContent.includes('edit') || userMessageContent.includes('update') || userMessageContent.includes('change') || userMessageContent.includes('modify')) {
        // Handle task update request (fallback when backend API is unavailable)
        let targetTask = null;

        // Try to find task by matching title keywords
        const taskTitleMatch = inputValue.match(/(?:edit|update|change|modify)\s+(?:task\s+)?(?:"|')?(.+?)(?:"|')?\s*(?:to|not|from|with)?/i);
        if (taskTitleMatch) {
          const potentialTitle = taskTitleMatch[1].trim().toLowerCase();
          targetTask = todo.todos.find(t =>
            t.title.toLowerCase().includes(potentialTitle) ||
            potentialTitle.includes(t.title.toLowerCase())
          );
        }

        // If not found, try matching against words
        if (!targetTask) {
          const words = inputValue.split(/\s+/).filter(w => w.length > 3);
          for (const word of words) {
            const cleanWord = word.toLowerCase().replace(/[^a-z0-9]/g, '');
            const foundTask = todo.todos.find(t =>
              t.title.toLowerCase().includes(cleanWord) ||
              (t.description && t.description.toLowerCase().includes(cleanWord))
            );
            if (foundTask) {
              targetTask = foundTask;
              break;
            }
          }
        }

        // Check for "last" or "recent" keywords
        if (!targetTask && (userMessageContent.includes('last') || userMessageContent.includes('recent') || userMessageContent.includes('previous'))) {
          const incompleteTasks = todo.todos.filter(t => !t.is_completed);
          if (incompleteTasks.length > 0) {
            targetTask = incompleteTasks[incompleteTasks.length - 1];
          }
        }

        // Default to most recent pending task
        if (!targetTask && todo.todos.length > 0) {
          const incompleteTasks = todo.todos.filter(t => !t.is_completed);
          if (incompleteTasks.length > 0) {
            targetTask = incompleteTasks[incompleteTasks.length - 1];
          } else {
            targetTask = todo.todos[todo.todos.length - 1];
          }
        }

        if (targetTask) {
          let fieldToUpdate = 'title';
          let newValue = '';

          // Check if updating date/time
          if (userMessageContent.includes('date') || userMessageContent.includes('time') || userMessageContent.includes('when')) {
            fieldToUpdate = 'date_time';
            setTaskTitle(targetTask.title);
            setTaskDescription(targetTask.description || '');
            setShowCalendarPicker(true);
            aiResponse = `Got it 👍\n\nI'll help you update the date and time for **"${targetTask.title}"**.\n\nPlease select the new date and time using the calendar picker that just appeared on the dashboard.`;
          } else {
            // Check if updating description
            if (userMessageContent.includes('description') || userMessageContent.includes('desc') || userMessageContent.includes('details')) {
              fieldToUpdate = 'description';
            }

            // Extract new value
            const toPattern = inputValue.match(/(?:to|into)\s+["']?([^"']+)["']?$/i);
            if (toPattern) {
              newValue = toPattern[1].trim();
            }

            const notPattern = inputValue.match(/not\s+(.+)$/i);
            if (!newValue && notPattern) {
              newValue = notPattern[1].trim();
            }

            if (!newValue) {
              const taskTitleInMsg = targetTask.title.toLowerCase();
              const msgLower = inputValue.toLowerCase();
              const titleIndex = msgLower.indexOf(taskTitleInMsg);
              if (titleIndex !== -1) {
                const afterTitle = inputValue.substring(titleIndex + targetTask.title.length).trim();
                newValue = afterTitle.replace(/^(to|into|not|with)\s+/i, '').trim();
              }
            }

            if (newValue && newValue.length > 0) {
              try {
                await todo.updateTodo(targetTask.id, { [fieldToUpdate]: newValue });
                const oldValue = fieldToUpdate === 'title' ? targetTask.title : (targetTask.description || 'none');
                aiResponse = `Got it 👍\n\nI've updated your task **"${targetTask.title}"** ${fieldToUpdate === 'title' ? 'title' : 'description'} from **"${oldValue}"** to **"${newValue}"**.\n\nWant to change the date or time as well?`;
              } catch (updateErr) {
                aiResponse = `Oops! I had trouble updating your task. The error was: ${updateErr instanceof Error ? updateErr.message : 'Unknown error'}.\n\nPlease try again or let me know if you need help.`;
              }
            } else {
              setPendingUpdateTask({ taskId: targetTask.id, field: fieldToUpdate });
              aiResponse = `I found the task **"${targetTask.title}"**.\n\nWhat would you like to change the ${fieldToUpdate === 'title' ? 'title' : 'description'} to?`;
            }
          }
        } else {
          aiResponse = "Hmm, I couldn't find the task you want to update.\n\nCould you please tell me more about which task you'd like to edit? You can mention:\n- The task title\n- Or say 'last task' or 'recent task'";
        }
      } else if (userMessageContent.includes('delete') || userMessageContent.includes('remove') || userMessageContent.includes('complete')) {
        aiResponse = "No problem 👍 Your task has been updated. Anything else you'd like to do?";
      } else if (userMessageContent.includes('what can you do') || userMessageContent.includes('help')) {
        aiResponse = "I can help you manage your tasks using chat — you can add, update, delete, or view tasks anytime 😊";
      } else if (userMessageContent.includes('bye') || userMessageContent.includes('goodbye')) {
        aiResponse = "Take care! 👋 Feel free to come back anytime you need help with your tasks!";
      } else {
        aiResponse = "I'm having trouble connecting to the backend right now, but I'm here to help! Could you try again in a moment? 😊";
      }

      const aiMessage: Message = {
        id: nanoid(),
        role: 'assistant',
        content: aiResponse,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, aiMessage]);
      console.error('Error sending message:', err);
    } finally {
      setInputValue(''); // Clear input after processing
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    setInputValue(suggestion);
    setTimeout(() => {
      handleSend();
    }, 100);
  };

  const handleClearChat = () => {
    setMessages([]);
    setConversationId(null);
    setShowSuggestions(true);
    if (user) {
      localStorage.removeItem(`chatHistory_${user.id}`);
      localStorage.removeItem(`currentChatConversationId_${user.id}`);
    }
  };

  // Initial suggestions
  const suggestions = [
    "What can you do?",
    "Add a new task",
    "Show my tasks"
  ];

  return (
    <AnimatePresence>
      <motion.div 
        className="fixed bottom-24 right-6 z-50 w-full max-w-md"
        initial={{ opacity: 0, scale: 0.8, y: 50 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.8, y: 50 }}
        transition={{ type: "spring", damping: 20, stiffness: 300 }}
      >
        {/* Popup Panel */}
        <div className="bg-white rounded-2xl shadow-xl overflow-hidden flex flex-col h-[600px] border border-gray-200">
          {/* Header */}
          <div className="flex items-center justify-between p-4 bg-white border-b">
            <div className="flex items-center space-x-3">
              {/* Odama-style icon */}
              <div className="relative w-8 h-8">
                <div className="absolute inset-0 rounded-full bg-gradient-to-r from-purple-500 to-indigo-600"></div>
                <div className="absolute inset-1 rounded-full bg-white flex items-center justify-center">
                  <svg 
                    xmlns="http://www.w3.org/2000/svg" 
                    width="12" 
                    height="12" 
                    viewBox="0 0 24 24" 
                    fill="none" 
                    stroke="currentColor" 
                    strokeWidth="2" 
                    strokeLinecap="round" 
                    strokeLinejoin="round"
                    className="text-indigo-600"
                  >
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                  </svg>
                </div>
              </div>
              <h2 className="text-lg font-semibold text-gray-800">AI Assist</h2>
            </div>
            <div className="flex space-x-2">
              <button
                onClick={handleClearChat}
                className="text-gray-500 hover:text-gray-700 focus:outline-none"
                aria-label="Clear chat"
              >
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  width="20" 
                  height="20" 
                  viewBox="0 0 24 24" 
                  fill="none" 
                  stroke="currentColor" 
                  strokeWidth="2" 
                  strokeLinecap="round" 
                  strokeLinejoin="round"
                >
                  <path d="M3 6h18M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6m3 0V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2M10 11v6M14 11v6"></path>
                </svg>
              </button>
              <button
                onClick={onClose}
                className="text-gray-500 hover:text-gray-700 focus:outline-none"
                aria-label="Close chat"
              >
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  width="20" 
                  height="20" 
                  viewBox="0 0 24 24" 
                  fill="none" 
                  stroke="currentColor" 
                  strokeWidth="2" 
                  strokeLinecap="round" 
                  strokeLinejoin="round"
                >
                  <line x1="18" y1="6" x2="6" y2="18"></line>
                  <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
              </button>
            </div>
          </div>

          {/* Main Content Area */}
          <div className="flex-1 overflow-hidden flex flex-col">
            {messages.length === 0 && showSuggestions ? (
              // Empty State UI
              <div className="flex-1 flex flex-col items-center justify-center p-6 bg-gradient-to-b from-white to-gray-50">
                <div className="relative w-16 h-16 mb-4">
                  {/* Large Odama-style icon */}
                  <div className="absolute inset-0 rounded-full bg-gradient-to-r from-purple-500 to-indigo-600"></div>
                  <div className="absolute inset-2 rounded-full bg-white flex items-center justify-center">
                    <svg 
                      xmlns="http://www.w3.org/2000/svg" 
                      width="20" 
                      height="20" 
                      viewBox="0 0 24 24" 
                      fill="none" 
                      stroke="currentColor" 
                      strokeWidth="2" 
                      strokeLinecap="round" 
                      strokeLinejoin="round"
                      className="text-indigo-600"
                    >
                      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                    </svg>
                  </div>
                </div>
                <h3 className="text-xl font-medium text-gray-800 mb-6">Hey there! 👋</h3>
                
                {/* Suggestion Buttons */}
                <div className="grid grid-cols-1 gap-3 w-full max-w-xs">
                  {suggestions.map((suggestion) => (
                    <motion.button
                      key={suggestion}
                      onClick={() => handleSuggestionClick(suggestion)}
                      className="py-2 px-4 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-full text-sm transition-colors duration-200 text-center"
                      whileHover={{ scale: 1.03 }}
                      whileTap={{ scale: 0.98 }}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: suggestions.indexOf(suggestion) * 0.1 }}
                    >
                      {suggestion}
                    </motion.button>
                  ))}
                </div>
              </div>
            ) : (
              // Messages Container
              <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gradient-to-b from-white to-gray-50">
                {error && (
                  <motion.div 
                    className="bg-red-100 border border-red-300 text-red-700 p-3 rounded-lg"
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                  >
                    {error}
                  </motion.div>
                )}

                {messages.map((msg) => (
                  <motion.div
                    key={msg.id}
                    className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.3 }}
                  >
                    {msg.role === 'assistant' && (
                      <div className="mr-2 flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-r from-purple-500 to-indigo-600 flex items-center justify-center">
                        <svg 
                          xmlns="http://www.w3.org/2000/svg" 
                          width="12" 
                          height="12" 
                          viewBox="0 0 24 24" 
                          fill="none" 
                          stroke="white" 
                          strokeWidth="2" 
                          strokeLinecap="round" 
                          strokeLinejoin="round"
                        >
                          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                        </svg>
                      </div>
                    )}
                    <div
                      className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                        msg.role === 'user'
                          ? 'bg-indigo-500 text-white rounded-br-none'
                          : 'bg-purple-100 text-gray-800 rounded-bl-none'
                      }`}
                    >
                      <div className="whitespace-pre-wrap">{msg.content}</div>
                      <div className={`text-xs mt-1 ${msg.role === 'user' ? 'text-indigo-200' : 'text-purple-600'}`}>
                        {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </div>
                    </div>
                  </motion.div>
                ))}

                {isLoading && (
                  <motion.div
                    key="loading-message"
                    className="flex justify-start"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                  >
                    <div className="mr-2 flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-r from-purple-500 to-indigo-600 flex items-center justify-center">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="12"
                        height="12"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="white"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      >
                        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                      </svg>
                    </div>
                    <div className="bg-purple-100 text-gray-800 rounded-2xl px-4 py-3 rounded-bl-none">
                      <div className="flex items-center">
                        <div className="h-2 w-2 bg-purple-500 rounded-full mr-1 animate-bounce" style={{ animationDelay: '0ms' }}></div>
                        <div className="h-2 w-2 bg-purple-500 rounded-full mr-1 animate-bounce" style={{ animationDelay: '300ms' }}></div>
                        <div className="h-2 w-2 bg-purple-500 rounded-full mr-1 animate-bounce" style={{ animationDelay: '600ms' }}></div>
                      </div>
                    </div>
                  </motion.div>
                )}

                <div ref={messagesEndRef} />
              </div>
            )}

            {/* Input Area */}
            <div className="border-t border-gray-200 p-4 bg-white">
              <div className="flex gap-2">
                <input
                  type="text"
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Ask me anything..."
                  disabled={isLoading || !user}
                  className="flex-1 bg-gray-100 text-gray-800 rounded-full px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-300 disabled:opacity-50"
                />
                <motion.button
                  onClick={handleSend}
                  disabled={isLoading || !inputValue.trim() || !user}
                  className="bg-indigo-600 hover:bg-indigo-700 text-white rounded-full p-3 h-12 w-12 flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
                  whileHover={{ scale: isLoading ? 1 : 1.05 }}
                  whileTap={{ scale: isLoading ? 1 : 0.95 }}
                >
                  <svg 
                    xmlns="http://www.w3.org/2000/svg" 
                    width="18" 
                    height="18" 
                    viewBox="0 0 24 24" 
                    fill="none" 
                    stroke="currentColor" 
                    strokeWidth="2" 
                    strokeLinecap="round" 
                    strokeLinejoin="round"
                  >
                    <line x1="22" y1="2" x2="11" y2="13"></line>
                    <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                  </svg>
                </motion.button>
              </div>
            </div>
          </div>
        </div>
      </motion.div>
    </AnimatePresence>
  );
};

export default FloatingChatPopup;