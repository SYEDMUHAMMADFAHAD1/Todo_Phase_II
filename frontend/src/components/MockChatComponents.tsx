import React, { useState } from 'react';

// Define the types that were imported from @openai/chat-components
export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: Array<{
    type: 'text';
    text: {
      value: string;
    };
  }>;
}

export interface ChatRequestOptions {
  // Add any options that might be needed for chat requests
  [key: string]: any;
}

interface ChatComponentProps {
  messages: ChatMessage[];
  onSend: (message: string, conversationId?: string, options?: ChatRequestOptions) => void;
  isLoading?: boolean;
  onReset?: () => void;
  inputDisabled?: boolean;
}

// Mock Chat component implementation
export const Chat: React.FC<ChatComponentProps> = ({
  messages,
  onSend,
  isLoading = false,
  onReset,
  inputDisabled = false,
}) => {
  const [inputValue, setInputValue] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim() && !isLoading && !inputDisabled) {
      onSend(inputValue);
      setInputValue('');
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Chat messages container */}
      <div className="flex-grow overflow-y-auto max-h-96 p-4 bg-gray-50">
        {messages.length === 0 ? (
          <p className="text-gray-500 italic">No messages yet. Start the conversation!</p>
        ) : (
          <div className="space-y-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`p-3 rounded-lg max-w-[80%] ${
                  message.role === 'user'
                    ? 'bg-blue-100 ml-auto text-right'
                    : 'bg-gray-200'
                }`}
              >
                {message.content.map((contentItem, idx) => {
                  if (contentItem.type === 'text') {
                    return <p key={idx}>{contentItem.text.value}</p>;
                  }
                  return null;
                })}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Input area */}
      <div className="p-4 border-t">
        <form onSubmit={handleSubmit} className="flex gap-2">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            disabled={isLoading || inputDisabled}
            placeholder={inputDisabled ? 'Sign in to chat...' : 'Type your message...'}
            className="flex-grow p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            disabled={isLoading || inputDisabled || !inputValue.trim()}
            className="p-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? 'Sending...' : 'Send'}
          </button>
          {onReset && (
            <button
              type="button"
              onClick={onReset}
              className="p-2 bg-gray-500 text-white rounded hover:bg-gray-600"
            >
              Reset
            </button>
          )}
        </form>
      </div>
    </div>
  );
};