'use client';

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { TodoCreateInput, TodoUpdateInput } from '@/hooks/todo';
import Toast from '@/components/common/Toast';
import { useCalendarPicker } from '@/contexts/CalendarPickerContext';

interface TodoFormProps {
  onCreate: (data: TodoCreateInput) => Promise<void>;
  onUpdate?: (id: string, data: TodoUpdateInput) => Promise<void>;
  taskToEdit?: {
    id: string;
    title: string;
    description?: string;
    dateTime: string;
  } | null;
  isLoading?: boolean;
  onSuccess?: () => void;
}

export default function TodoForm({ 
  onCreate, 
  onUpdate, 
  taskToEdit, 
  isLoading = false, 
  onSuccess 
}: TodoFormProps) {
  const { showCalendarPicker, setShowCalendarPicker, taskTitle, taskDescription, setTaskTitle, setTaskDescription, onTaskCreated } = useCalendarPicker();
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [dateTime, setDateTime] = useState(() => {
    // Initialize with current date + 1 hour as default for new tasks
    const defaultDate = new Date();
    defaultDate.setHours(defaultDate.getHours() + 1);
    return defaultDate.toISOString().slice(0, 16);
  });
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [toast, setToast] = useState({ message: '', type: 'success' as 'success' | 'error', isVisible: false });

  // Listen to changes from the AI chatbot
  useEffect(() => {
    if (taskTitle) {
      setTitle(taskTitle);
    }
    if (taskDescription) {
      setDescription(taskDescription);
    }
  }, [taskTitle, taskDescription]);

  // Handle editing a task
  useEffect(() => {
    if (taskToEdit) {
      setTitle(taskToEdit.title);
      setDescription(taskToEdit.description || '');
      // Format the date for the datetime-local input
      const taskDate = new Date(taskToEdit.dateTime);
      if (isNaN(taskDate.getTime())) {
        // If the date is invalid, use current date + 1 hour as default
        const defaultDate = new Date();
        defaultDate.setHours(defaultDate.getHours() + 1);
        setDateTime(defaultDate.toISOString().slice(0, 16));
      } else {
        setDateTime(taskDate.toISOString().slice(0, 16));
      }
    } else {
      // Reset form when not editing
      setTitle('');
      setDescription('');
      // Set default date to current date + 1 hour for new tasks
      const defaultDate = new Date();
      defaultDate.setHours(defaultDate.getHours() + 1);
      setDateTime(defaultDate.toISOString().slice(0, 16));
    }
  }, [taskToEdit]);

  const showToast = (message: string, type: 'success' | 'error') => {
    setToast({ message, type, isVisible: true });
  };

  const hideToast = () => {
    setToast({ ...toast, isVisible: false });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!title.trim()) {
      setError('Title is required');
      showToast('Please enter a task title', 'error');
      return;
    }

    if (!dateTime) {
      setError('Date & Time is required');
      showToast('Please select date & time', 'error');
      return;
    }

    // Validate the date
    const dateObj = new Date(dateTime);
    if (isNaN(dateObj.getTime())) {
      setError('Invalid date & time selected');
      showToast('Please select a valid date & time', 'error');
      return;
    }

    try {
      setIsSubmitting(true);

      if (taskToEdit && onUpdate) {
        // Update existing task
        await onUpdate(taskToEdit.id, {
          title: title.trim(),
          description: description.trim() || undefined,
          dateTime: dateObj,
        });
        showToast('Task updated successfully!', 'success');
      } else {
        // Create new task
        await onCreate({
          title: title.trim(),
          description: description.trim() || undefined,
          dateTime: dateObj,
          reminderTriggered: false, // Initialize reminder as not triggered
        });
        setTitle('');
        setDescription('');
        // Set default date to current date + 1 hour for new tasks
        const defaultDate = new Date();
        defaultDate.setHours(defaultDate.getHours() + 1);
        setDateTime(defaultDate.toISOString().slice(0, 16));
        showToast('Task created successfully!', 'success');
      }

      // Reset the task details in the context only if not editing via AI
      if (!showCalendarPicker || !taskToEdit) {
        setTaskTitle('');
        setTaskDescription('');
      }
      setShowCalendarPicker(false);
      onSuccess?.();
      if (onTaskCreated) {
        onTaskCreated(); // Call the callback if provided
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to create/update todo';
      setError(errorMessage);
      showToast(`Error: ${errorMessage}`, 'error');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      {showCalendarPicker && (
        <div className="mb-4 p-3 rounded-lg bg-amber-900/20 border border-amber-700/30 text-amber-200 text-center">
          Please select date & time to continue
        </div>
      )}
      <motion.form
        onSubmit={handleSubmit}
        className="bg-slate-800/40 backdrop-blur-xl rounded-2xl border border-slate-700/50 shadow-xl p-6 mb-8 relative"
      >
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-white">
            {taskToEdit ? 'Update Task' : 'Create New Task'}
          </h2>
          <div className="h-3 w-3 rounded-full bg-emerald-500 animate-pulse"></div>
        </div>

        {error && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            className="mb-4 rounded-lg bg-rose-900/30 p-3 border border-rose-700/50 backdrop-blur-sm"
          >
            <p className="text-sm text-rose-300">{error}</p>
          </motion.div>
        )}

        <div className="space-y-5">
          <div className="space-y-2">
            <label htmlFor="title" className="block text-sm font-medium text-slate-300">
              Task Title *
            </label>
            <div className="relative">
              <input
                id="title"
                name="title"
                type="text"
                placeholder="What needs to be done?"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                disabled={isSubmitting || isLoading}
                className="w-full px-4 py-3.5 text-sm rounded-xl border border-slate-600 bg-slate-800/50 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 disabled:cursor-not-allowed disabled:opacity-50 transition-all duration-200 pl-12"
              />
              <div className="absolute left-4 top-1/2 transform -translate-y-1/2 text-slate-400">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                </svg>
              </div>
            </div>
          </div>

          <div className="space-y-2">
            <label htmlFor="description" className="block text-sm font-medium text-slate-300">
              Description (Optional)
            </label>
            <textarea
              id="description"
              name="description"
              placeholder="Add details..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              disabled={isSubmitting || isLoading}
              className="flex min-h-[100px] w-full rounded-xl border border-slate-600 bg-slate-800/50 text-sm ring-offset-slate-900 placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 disabled:cursor-not-allowed disabled:opacity-50 text-white p-4 transition-all duration-200 resize-none"
            />
          </div>

          <div className="space-y-2">
            <label htmlFor="datetime" className="block text-sm font-medium text-slate-300">
              Date & Time *
            </label>
            <div className="relative">
              <input
                id="datetime"
                name="datetime"
                type="datetime-local"
                value={dateTime}
                onChange={(e) => setDateTime(e.target.value)}
                disabled={isSubmitting || isLoading}
                onKeyDown={(e) => {
                  // Prevent all keyboard input to force using the date/time picker
                  if(['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Tab'].indexOf(e.key) === -1) {
                    e.preventDefault();
                  }
                }}
                className="w-full px-4 py-3.5 text-sm rounded-xl border border-slate-600 bg-slate-800/50 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 disabled:cursor-not-allowed disabled:opacity-50 transition-all duration-200 pl-12"
              />
              <div className="absolute left-4 top-1/2 transform -translate-y-1/2 text-slate-400">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clipRule="evenodd" />
                </svg>
              </div>
            </div>
          </div>

          <motion.button
            type="submit"
            disabled={isSubmitting || isLoading || !title.trim() || !dateTime}
            className={`w-full py-3.5 rounded-xl text-base font-semibold shadow-lg transition-all duration-300 flex items-center justify-center ${
              isSubmitting || isLoading || !title.trim() || !dateTime
                ? 'bg-slate-700 text-slate-400 cursor-not-allowed'
                : 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white hover:from-indigo-700 hover:to-purple-700 hover:shadow-indigo-500/30 transform hover:-translate-y-0.5'
            }`}
            whileHover={!isSubmitting && !isLoading && title.trim() && dateTime ? { scale: 1.02 } : {}}
            whileTap={!isSubmitting && !isLoading && title.trim() && dateTime ? { scale: 0.98 } : {}}
          >
            {isSubmitting ? (
              <>
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {taskToEdit ? 'Updating...' : 'Creating...'}
              </>
            ) : (
              <>
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
                </svg>
                {taskToEdit ? 'Update Task' : 'Add Task'}
              </>
            )}
          </motion.button>
        </div>

        <Toast
          message={toast.message}
          type={toast.type}
          isVisible={toast.isVisible}
          onClose={hideToast}
        />
      </motion.form>
    </motion.div>
  );
}