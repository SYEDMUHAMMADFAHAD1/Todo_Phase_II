'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useAuth } from '@/hooks/auth';
import { useTodo } from '@/hooks/todo';
import Sidebar from '@/components/dashboard/Sidebar';
import Header from '@/components/dashboard/Header';
import TodoFormWithUpdate from '@/components/todo/TodoFormWithUpdate';
import TodoList from '@/components/todo/TodoList';
import StatsSection from '@/components/dashboard/StatsSection';
import FloatingChatButton from '@/components/chat/FloatingChatButton';
import { useCalendarPicker } from '@/contexts/CalendarPickerContext';

const DashboardPage = () => {
  const { user, isAuthenticated, isLoading, signOut } = useAuth();
  const todo = useTodo();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-slate-950 to-black">
        <div className="text-white">Loading...</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    // This shouldn't happen due to ProtectedRoute, but as a fallback
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-slate-950 to-black">
        <div className="text-destructive">Unauthorized. Please sign in.</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-950 to-black">
      <div className="flex h-screen overflow-hidden">
        <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

        <div className="flex flex-1 flex-col overflow-hidden">
          <Header
            onMenuToggle={() => setSidebarOpen(!sidebarOpen)}
            sidebarOpen={sidebarOpen}
          />

          <main className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">
            <div className="max-w-7xl mx-auto">
              <div className="mb-8">
                <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-2">
                  <div>
                    <h2 className="text-3xl font-bold text-white">Dashboard</h2>
                    <p className="text-slate-400">Manage your tasks efficiently</p>
                  </div>
                </div>
              </div>

              {todo.error && (
                <div className="mb-6 rounded-lg bg-rose-900/30 border border-rose-700/50 p-4 backdrop-blur-sm">
                  <div className="flex items-start">
                    <div className="flex-shrink-0">
                      <svg className="h-5 w-5 text-rose-400" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                      </svg>
                    </div>
                    <div className="ml-3">
                      <h3 className="text-sm font-medium text-rose-300">Error</h3>
                      <p className="mt-1 text-sm text-rose-200/80">{todo.error}</p>
                    </div>
                  </div>
                </div>
              )}

              <StatsSection todo={todo} />

              <div className="mb-8">
                <TodoFormWithUpdate
                  onCreate={async (data) => {
                    await todo.createTodo(data);
                  }}
                  onUpdate={async (id, data) => {
                    await todo.updateTodo(id, data);
                  }}
                  isLoading={todo.loading}
                  onSuccess={() => {
                    todo.refetch();
                  }}
                />
              </div>

              <div>
                <TodoList todo={todo} />
              </div>
            </div>
          </main>
        </div>
      </div>
      
      {/* Floating Chat Button */}
      <FloatingChatButton />
    </div>
  );
};

export default DashboardPage;
