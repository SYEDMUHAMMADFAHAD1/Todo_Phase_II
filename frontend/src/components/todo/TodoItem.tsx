'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Todo, TodoUpdateInput } from '@/hooks/todo';

interface TodoItemProps {
  todo: Todo;
  onUpdate: (id: string, input: TodoUpdateInput) => Promise<void>;
  onDelete: (id: string) => Promise<void>;
  onToggle: (id: string) => Promise<void>;
  isDeleting?: boolean;
  isUpdating?: boolean;
}

export default function TodoItem({
  todo,
  onUpdate,
  onDelete,
  onToggle,
  isDeleting = false,
  isUpdating = false,
}: TodoItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(todo.title);
  const [editDescription, setEditDescription] = useState(todo.description || '');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleToggle = async () => {
    try {
      await onToggle(todo.id);
    } catch (err) {
      console.error('Error toggling todo:', err);
    }
  };

  const handleSave = async () => {
    if (!editTitle.trim()) {
      return;
    }

    try {
      setIsSubmitting(true);
      await onUpdate(todo.id, {
        title: editTitle.trim(),
        description: editDescription.trim() || undefined,
      });
      setIsEditing(false);
    } catch (err) {
      console.error('Error updating todo:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleCancel = () => {
    setEditTitle(todo.title);
    setEditDescription(todo.description || '');
    setIsEditing(false);
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await onDelete(todo.id);
      } catch (err) {
        console.error('Error deleting todo:', err);
      }
    }
  };

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3 }}
      className={`bg-slate-800/40 backdrop-blur-sm rounded-2xl border ${
        todo.is_completed 
          ? 'border-emerald-500/20 bg-emerald-900/10' 
          : 'border-slate-700/50'
      } p-5 transition-all duration-300 hover:shadow-lg hover:shadow-slate-900/20 ${
        isDeleting ? 'opacity-50' : ''
      }`}
    >
      <div className="flex items-start space-x-4">
        {/* Checkbox */}
        <motion.button
          whileTap={{ scale: 0.9 }}
          onClick={handleToggle}
          disabled={isUpdating || isDeleting}
          className={`mt-1 h-6 w-6 rounded-full flex items-center justify-center ${
            todo.is_completed
              ? 'bg-emerald-500/20 border-2 border-emerald-500'
              : 'bg-slate-700/50 border-2 border-slate-600'
          }`}
        >
          <AnimatePresence>
            {todo.is_completed && (
              <motion.svg
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                exit={{ scale: 0 }}
                xmlns="http://www.w3.org/2000/svg"
                className="h-4 w-4 text-emerald-400"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fillRule="evenodd"
                  d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                  clipRule="evenodd"
                />
              </motion.svg>
            )}
          </AnimatePresence>
        </motion.button>

        {/* Content */}
        <div className="flex-1 min-w-0">
          {isEditing ? (
            <div className="space-y-3">
              <input
                type="text"
                value={editTitle}
                onChange={(e) => setEditTitle(e.target.value)}
                disabled={isSubmitting}
                className="w-full px-4 py-2.5 text-sm rounded-lg border border-slate-600 bg-slate-700/50 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
              />
              <textarea
                value={editDescription}
                onChange={(e) => setEditDescription(e.target.value)}
                disabled={isSubmitting}
                className="w-full px-4 py-2.5 text-sm rounded-lg border border-slate-600 bg-slate-700/50 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
                rows={2}
              />
            </div>
          ) : (
            <div className="flex-1">
              <motion.h3
                animate={{
                  textDecoration: todo.is_completed ? 'line-through' : 'none',
                  color: todo.is_completed ? '#9CA3AF' : '#F9FAFB'
                }}
                transition={{ duration: 0.3 }}
                className={`font-semibold text-lg ${
                  todo.is_completed ? 'text-slate-400' : 'text-white'
                }`}
              >
                {todo.title}
              </motion.h3>
              {todo.description && (
                <motion.p
                  animate={{
                    textDecoration: todo.is_completed ? 'line-through' : 'none',
                    color: todo.is_completed ? '#9CA3AF' : '#9CA3AF'
                  }}
                  transition={{ duration: 0.3 }}
                  className={`text-sm mt-2 ${
                    todo.is_completed ? 'text-slate-500' : 'text-slate-400'
                  }`}
                >
                  {todo.description}
                </motion.p>
              )}
              <div className="flex items-center justify-between mt-4">
                <p className="text-xs text-slate-500">
                  Created {new Date(todo.created_at).toLocaleDateString()}
                </p>
                <div className="flex space-x-2">
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    todo.is_completed 
                      ? 'bg-emerald-900/30 text-emerald-300' 
                      : 'bg-amber-900/30 text-amber-300'
                  }`}>
                    {todo.is_completed ? 'Completed' : 'Pending'}
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="flex-shrink-0 flex items-center space-x-2">
          {isEditing ? (
            <div className="flex space-x-2">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleSave}
                disabled={isSubmitting || !editTitle.trim()}
                className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                Save
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleCancel}
                disabled={isSubmitting}
                className="px-4 py-2 text-sm font-medium text-slate-300 bg-slate-700 rounded-lg hover:bg-slate-600 disabled:opacity-50 transition-colors"
              >
                Cancel
              </motion.button>
            </div>
          ) : (
            <div className="flex space-x-2">
              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={() => setIsEditing(true)}
                disabled={isDeleting}
                className="p-2 text-slate-400 hover:text-white hover:bg-slate-700/50 rounded-lg transition-colors backdrop-blur-sm"
                title="Edit"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                </svg>
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={handleDelete}
                disabled={isDeleting}
                className="p-2 text-rose-400 hover:text-rose-300 hover:bg-rose-900/30 rounded-lg transition-colors"
                title="Delete"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
              </motion.button>
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
}
