import React from 'react';
import { cn } from '@/lib/utils';

interface MessageBubbleProps {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: Date;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ 
  role, 
  content, 
  timestamp 
}) => {
  const isUser = role === 'user';
  
  return (
    <div className={cn(
      'flex mb-4',
      isUser ? 'justify-end' : 'justify-start'
    )}>
      <div className={cn(
        'max-w-[80%] rounded-lg px-4 py-2',
        isUser 
          ? 'bg-blue-500 text-white rounded-br-none' 
          : 'bg-gray-200 text-gray-800 rounded-bl-none'
      )}>
        <div className="whitespace-pre-wrap">{content}</div>
        {timestamp && (
          <div className={cn(
            'text-xs mt-1',
            isUser ? 'text-blue-100' : 'text-gray-500'
          )}>
            {timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </div>
        )}
      </div>
    </div>
  );
};

export default MessageBubble;