'use client';

import React, { useState } from 'react';
import FloatingChatPopup from './FloatingChatPopup';

const FloatingChatButton: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  return (
    <>
      {/* Floating Chat Button */}
      <button
        onClick={toggleChat}
        className="fixed bottom-6 right-6 z-50 w-14 h-14 rounded-full bg-gradient-to-r from-purple-500 to-indigo-600 shadow-lg flex items-center justify-center hover:from-purple-600 hover:to-indigo-700 transition-all duration-300 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-purple-400 focus:ring-opacity-75"
        aria-label="Open AI Assistant"
      >
        <div className="relative w-8 h-8">
          {/* Odama-style icon with sparkle/star */}
          <div className="absolute inset-0 rounded-full bg-white bg-opacity-20 backdrop-blur-sm"></div>
          <div className="absolute inset-1 rounded-full bg-gradient-to-r from-white to-cyan-100 flex items-center justify-center">
            <svg 
              xmlns="http://www.w3.org/2000/svg" 
              width="16" 
              height="16" 
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
          {/* Sparkle/star element */}
          <div className="absolute -top-1 -right-1 w-4 h-4">
            <svg 
              xmlns="http://www.w3.org/2000/svg" 
              width="100%" 
              height="100%" 
              viewBox="0 0 24 24" 
              fill="none" 
              stroke="currentColor" 
              strokeWidth="2" 
              strokeLinecap="round" 
              strokeLinejoin="round"
              className="text-yellow-400"
            >
              <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
            </svg>
          </div>
        </div>
      </button>

      {/* Chat Popup Panel */}
      {isOpen && <FloatingChatPopup onClose={() => setIsOpen(false)} />}
    </>
  );
};

export default FloatingChatButton;