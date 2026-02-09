import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Notification } from '@/hooks/useNotification';

interface NotificationListProps {
  notifications: Notification[];
  onRemove: (id: string) => void;
}

const NotificationList: React.FC<NotificationListProps> = ({ notifications, onRemove }) => {
  return (
    <div className="fixed top-4 right-4 z-50 space-y-2 w-80 max-w-full">
      <AnimatePresence>
        {notifications.map((notification) => (
          <motion.div
            key={notification.id}
            initial={{ opacity: 0, y: -20, scale: 0.8 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -20, scale: 0.8 }}
            transition={{ duration: 0.2 }}
            className={`p-4 rounded-xl shadow-lg backdrop-blur-sm ${
              notification.type === 'success'
                ? 'bg-emerald-900/80 border border-emerald-700/50 text-emerald-100'
                : notification.type === 'error'
                ? 'bg-rose-900/80 border border-rose-700/50 text-rose-100'
                : notification.type === 'warning'
                ? 'bg-amber-900/80 border border-amber-700/50 text-amber-100'
                : 'bg-slate-800/80 border border-slate-700/50 text-slate-100'
            }`}
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <p className="text-sm font-medium">{notification.message}</p>
              </div>
              <button
                onClick={() => onRemove(notification.id)}
                className="ml-4 text-slate-400 hover:text-slate-200 transition-colors"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
              </button>
            </div>
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
};

export default NotificationList;