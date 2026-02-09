import { useState, useEffect } from 'react';
import { nanoid } from 'nanoid';

export interface Notification {
  id: string;
  message: string;
  type: 'info' | 'success' | 'warning' | 'error';
  timestamp: Date;
}

export const useNotification = () => {
  const [notifications, setNotifications] = useState<Notification[]>([]);

  const addNotification = (message: string, type: 'info' | 'success' | 'warning' | 'error' = 'info') => {
    const newNotification: Notification = {
      id: nanoid(),
      message,
      type,
      timestamp: new Date(),
    };

    setNotifications(prev => [...prev, newNotification]);

    // Auto-remove notification after 5 seconds
    setTimeout(() => {
      removeNotification(newNotification.id);
    }, 5000);
  };

  const removeNotification = (id: string) => {
    setNotifications(prev => prev.filter(notification => notification.id !== id));
  };

  return {
    notifications,
    addNotification,
    removeNotification,
  };
};