'use client';

import React, { useState } from 'react';
import { useAuth } from '@/hooks/auth';
import Button from '@/components/ui/Button';

export default function UserMenu() {
  const { user, signOut } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const [isSigningOut, setIsSigningOut] = useState(false);

  if (!user) {
    return (
      <div className="flex items-center space-x-4">
        <Button
          variant="outline"
          size="sm"
          onClick={() => window.location.href = '/signin'}
        >
          Sign In
        </Button>
        <Button
          variant="primary"
          size="sm"
          onClick={() => window.location.href = '/signup'}
        >
          Sign Up
        </Button>
      </div>
    );
  }

  const handleSignOut = async () => {
    setIsSigningOut(true);
    try {
      await signOut();
      window.location.href = '/signin';
    } catch (error) {
      console.error('Sign out failed:', error);
    } finally {
      setIsSigningOut(false);
    }
  };

  const handleProfileClick = () => {
    // Navigate to user profile (to be implemented)
    window.location.href = '/profile';
  };

  const handleSettingsClick = () => {
    // Navigate to settings (to be implemented)
    window.location.href = '/settings';
  };

  return (
    <div className="relative">
      <button
        type="button"
        className="flex items-center space-x-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 rounded-full"
        onClick={() => setIsOpen(!isOpen)}
        aria-expanded={isOpen}
        aria-haspopup="true"
      >
        <div className="flex items-center justify-center w-8 h-8 bg-blue-600 text-white rounded-full">
          {user.name ? (
            user.name.charAt(0).toUpperCase()
          ) : (
            user.email.charAt(0).toUpperCase()
          )}
        </div>
        <span className="hidden md:inline text-sm font-medium text-gray-700">
          {user.name || user.email}
        </span>
        <svg
          className={`w-4 h-4 text-gray-500 transition-transform ${isOpen ? 'rotate-180' : ''}`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {isOpen && (
        <>
          {/* Backdrop */}
          <div
            className="fixed inset-0 z-10"
            onClick={() => setIsOpen(false)}
          />

          {/* Dropdown menu */}
          <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 z-20 py-1">
            <div className="px-4 py-2 border-b border-gray-100">
              <p className="text-sm font-medium text-gray-900">{user.name || 'User'}</p>
              <p className="text-xs text-gray-500 truncate">{user.email}</p>
            </div>

            <button
              onClick={handleProfileClick}
              className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
            >
              Your Profile
            </button>

            <button
              onClick={handleSettingsClick}
              className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
            >
              Settings
            </button>

            <div className="border-t border-gray-100 my-1" />

            <button
              onClick={handleSignOut}
              disabled={isSigningOut}
              className="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-50 transition-colors disabled:opacity-50"
            >
              {isSigningOut ? 'Signing Out...' : 'Sign Out'}
            </button>
          </div>
        </>
      )}
    </div>
  );
}