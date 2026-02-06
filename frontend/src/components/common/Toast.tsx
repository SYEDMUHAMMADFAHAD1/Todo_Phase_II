'use client';

import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

type ToastType = 'success' | 'error' | 'info';

interface ToastProps {
  message: string;
  type: ToastType;
  isVisible: boolean;
  onClose: () => void;
}

const Toast = ({ message, type, isVisible, onClose }: ToastProps) => {
  const [show, setShow] = useState(false);

  useEffect(() => {
    if (isVisible) {
      setShow(true);
      const timer = setTimeout(() => {
        setShow(false);
        setTimeout(onClose, 300); // Wait for animation to complete
      }, 3000); // Auto-hide after 3 seconds

      return () => clearTimeout(timer);
    }
  }, [isVisible, onClose]);

  const getTypeStyles = () => {
    switch (type) {
      case 'success':
        return {
          bg: 'bg-emerald-900/90',
          border: 'border-emerald-700/50',
          text: 'text-emerald-200',
          icon: '✅'
        };
      case 'error':
        return {
          bg: 'bg-rose-900/90',
          border: 'border-rose-700/50',
          text: 'text-rose-200',
          icon: '❌'
        };
      case 'info':
        return {
          bg: 'bg-blue-900/90',
          border: 'border-blue-700/50',
          text: 'text-blue-200',
          icon: 'ℹ️'
        };
      default:
        return {
          bg: 'bg-slate-800/90',
          border: 'border-slate-700/50',
          text: 'text-slate-200',
          icon: '🔔'
        };
    }
  };

  const styles = getTypeStyles();

  return (
    <AnimatePresence>
      {show && (
        <motion.div
          initial={{ opacity: 0, y: 50, scale: 0.8 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: 50, scale: 0.8 }}
          transition={{ type: 'spring', damping: 25, stiffness: 200 }}
          className={`${styles.bg} backdrop-blur-xl border ${styles.border} rounded-xl p-4 shadow-2xl max-w-sm w-full`}
        >
          <div className="flex items-start">
            <span className="text-xl mr-3">{styles.icon}</span>
            <p className={`text-sm ${styles.text} flex-1`}>{message}</p>
            <button
              onClick={() => {
                setShow(false);
                setTimeout(onClose, 300);
              }}
              className="text-slate-400 hover:text-white ml-2"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </button>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default Toast;