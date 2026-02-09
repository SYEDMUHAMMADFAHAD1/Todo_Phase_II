import { useState, useCallback } from 'react';
import { apiClient } from '@/lib/api-client';

interface Message {
  id?: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export const useChat = (initialConversationId?: string) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [conversationId, setConversationId] = useState<string | undefined>(initialConversationId);

  const loadConversation = useCallback(async (convId: string) => {
    try {
      setIsLoading(true);
      setError(null);
      
      // In a real implementation, we would fetch the conversation history
      // For now, we'll just set the conversation ID and clear messages
      setConversationId(convId);
      // In a real implementation, we would fetch the conversation history from the API
      // const response = await apiClient.getConversationHistory(convId);
      // setMessages(response.messages);
    } catch (err) {
      setError('Failed to load conversation history');
      console.error('Error loading conversation:', err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const sendMessage = useCallback(async (message: string, userId: string) => {
    try {
      setIsLoading(true);
      setError(null);

      // Add user message to UI immediately
      const userMessage: Message = {
        role: 'user',
        content: message,
        timestamp: new Date(),
      };
      
      setMessages(prev => [...prev, userMessage]);

      // Call the API to get AI response
      const response = await apiClient.sendChatMessage(userId, message, conversationId);

      // Update conversation ID if it's the first message
      if (!conversationId) {
        setConversationId(response.conversation_id);
      }

      // Add AI response to messages
      const aiMessage: Message = {
        role: 'assistant',
        content: response.response,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (err) {
      setError('Failed to send message. Please try again.');
      console.error('Error sending message:', err);
      
      // Remove the user message if the API call failed
      setMessages(prev => prev.slice(0, -1));
    } finally {
      setIsLoading(false);
    }
  }, [conversationId]);

  const retry = useCallback(() => {
    setError(null);
  }, []);

  return {
    messages,
    sendMessage,
    isLoading,
    error,
    retry,
    loadConversation,
    conversationId
  };
};