'use client';

import React, { useState } from 'react';
import TaskCard from '@/components/dashboard/TaskCard';
import Skeleton from '@/components/common/Skeleton';
import { Todo, TodoUpdateInput, UseTodoReturn } from '@/hooks/todo';

interface TodoListProps {
  todo: UseTodoReturn;
}

type FilterType = 'all' | 'pending' | 'completed';

export default function TodoList({ todo }: TodoListProps) {
  const [deletingIds, setDeletingIds] = useState<Set<string>>(new Set());
  const [updatingIds, setUpdatingIds] = useState<Set<string>>(new Set());
  const [filter, setFilter] = useState<FilterType>('all');

  const handleUpdate = async (id: string, input: TodoUpdateInput) => {
    try {
      setUpdatingIds((prev) => new Set([...prev, id]));
      await todo.updateTodo(id, input);
    } finally {
      setUpdatingIds((prev) => {
        const newSet = new Set(prev);
        newSet.delete(id);
        return newSet;
      });
    }
  };

  const handleDelete = async (id: string) => {
    try {
      setDeletingIds((prev) => new Set([...prev, id]));
      await todo.deleteTodo(id);
      // Refetch tasks to ensure UI is synchronized with backend state
      await todo.refetch();
    } finally {
      setDeletingIds((prev) => {
        const newSet = new Set(prev);
        newSet.delete(id);
        return newSet;
      });
    }
  };

  const handleToggle = async (id: string) => {
    try {
      setUpdatingIds((prev) => new Set([...prev, id]));
      await todo.toggleTodo(id);
    } finally {
      setUpdatingIds((prev) => {
        const newSet = new Set(prev);
        newSet.delete(id);
        return newSet;
      });
    }
  };

  if (todo.loading) {
    return (
      <div className="space-y-4">
        {[...Array(3)].map((_, index) => (
          <Skeleton 
            key={index} 
            className="h-24 w-full rounded-2xl" 
          />
        ))}
      </div>
    );
  }

  if (todo.error) {
    return (
      <div className="rounded-lg bg-rose-900/20 p-4 border border-rose-700/30">
        <p className="text-sm text-rose-300">{todo.error}</p>
        <button
          onClick={todo.refetch}
          className="mt-2 text-sm font-medium text-rose-300 hover:text-rose-200"
        >
          Try again
        </button>
      </div>
    );
  }

  const completedCount = todo.todos.filter((t) => t.is_completed).length;
  const pendingCount = todo.todos.length - completedCount;

  // Filter todos based on selected filter
  const filteredTodos = todo.todos.filter((t) => {
    if (filter === 'completed') return t.is_completed;
    if (filter === 'pending') return !t.is_completed;
    return true; // 'all'
  });

  // Separate pending and completed for display
  const pendingTodos = filteredTodos.filter((t) => !t.is_completed);
  const completedTodos = filteredTodos.filter((t) => t.is_completed);

  return (
    <div>
      {/* Filter Buttons */}
      <div className="mb-8 flex flex-wrap gap-3">
        <button
          onClick={() => setFilter('all')}
          className={`px-6 py-3 rounded-full font-semibold transition-all duration-200 ${
            filter === 'all'
              ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/30'
              : 'bg-slate-700/50 text-slate-300 hover:bg-slate-600/50 backdrop-blur-sm'
          }`}
        >
          All ({todo.todos.length})
        </button>
        <button
          onClick={() => setFilter('pending')}
          className={`px-6 py-3 rounded-full font-semibold transition-all duration-200 ${
            filter === 'pending'
              ? 'bg-amber-500 text-slate-900 shadow-lg shadow-amber-500/30'
              : 'bg-slate-700/50 text-slate-300 hover:bg-slate-600/50 backdrop-blur-sm'
          }`}
        >
          Pending ({pendingCount})
        </button>
        <button
          onClick={() => setFilter('completed')}
          className={`px-6 py-3 rounded-full font-semibold transition-all duration-200 ${
            filter === 'completed'
              ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-500/30'
              : 'bg-slate-700/50 text-slate-300 hover:bg-slate-600/50 backdrop-blur-sm'
          }`}
        >
          Completed ({completedCount})
        </button>
      </div>

      {/* Todo List */}
      {filteredTodos.length === 0 ? (
        <div className="text-center py-16 bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-slate-700/50">
          <div className="mx-auto h-20 w-20 rounded-full bg-slate-700/50 flex items-center justify-center mb-6">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <p className="text-white font-medium text-lg mb-2">
            {filter === 'completed' && 'No completed tasks yet'}
            {filter === 'pending' && 'No pending tasks'}
            {filter === 'all' && 'No tasks yet'}
          </p>
          <p className="text-slate-400 text-base">
            {filter === 'all' && 'Create your first task to get started'}
            {filter !== 'all' && 'Switch filters to see other tasks'}
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {/* Pending todos */}
          {filter !== 'completed' && pendingTodos.length > 0 && (
            <>
              {filter === 'all' && pendingTodos.length > 0 && (
                <div className="text-lg font-semibold text-slate-300 mb-3">Pending Tasks</div>
              )}
              {pendingTodos.map((t) => (
                <TaskCard
                  key={t.id}
                  todo={t}
                  onUpdate={handleUpdate}
                  onDelete={handleDelete}
                  onToggle={handleToggle}
                  isDeleting={deletingIds.has(t.id)}
                  isUpdating={updatingIds.has(t.id)}
                />
              ))}
            </>
          )}

          {/* Completed todos */}
          {filter !== 'pending' && completedTodos.length > 0 && (
            <>
              {filter === 'all' && (
                <div className="relative mt-8 mb-4">
                  <div className="absolute inset-0 flex items-center">
                    <div className="w-full border-t border-slate-700/50"></div>
                  </div>
                  <div className="relative flex justify-center">
                    <span className="px-4 bg-slate-900/80 text-slate-400 text-base backdrop-blur-sm">Completed</span>
                  </div>
                </div>
              )}
              {completedTodos.map((t) => (
                <TaskCard
                  key={t.id}
                  todo={t}
                  onUpdate={handleUpdate}
                  onDelete={handleDelete}
                  onToggle={handleToggle}
                  isDeleting={deletingIds.has(t.id)}
                  isUpdating={updatingIds.has(t.id)}
                />
              ))}
            </>
          )}
        </div>
      )}
    </div>
  );
}
