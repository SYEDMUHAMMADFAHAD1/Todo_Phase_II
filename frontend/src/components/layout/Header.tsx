import React from 'react';

export default function Header() {
  return (
    <header className="border-b border-gray-200 bg-white shadow-sm">
      <div className="mx-auto max-w-7xl px-4 py-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <h1 className="text-2xl font-bold text-gray-900">Todo App</h1>
          </div>
          <nav className="flex items-center space-x-4">
            {/* User menu will be added later */}
          </nav>
        </div>
      </div>
    </header>
  );
}