import React, { createContext, useContext, ReactNode } from 'react';
import { useNotification } from '@/hooks/useNotification';
import NotificationList from '@/components/common/NotificationList';

interface NotificationContextType {
  addNotification: (message: string, type?: 'info' | 'success' | 'warning' | 'error') => void;
}

const NotificationContext = createContext<NotificationContextType | undefined>(undefined);

export const NotificationProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const { notifications, addNotification, removeNotification } = useNotification();

  return (
    <NotificationContext.Provider value={{ addNotification }}>
      {children}
      <NotificationList notifications={notifications} onRemove={removeNotification} />
    </NotificationContext.Provider>
  );
};

export const useNotificationContext = () => {
  const context = useContext(NotificationContext);
  if (context === undefined) {
    throw new Error('useNotificationContext must be used within a NotificationProvider');
  }
  return context;
};