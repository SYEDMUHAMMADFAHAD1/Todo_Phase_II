'use client';

import { AuthProvider } from '@/contexts/AuthContext';
import { NotificationProvider } from '@/contexts/NotificationContext';
import { CalendarPickerProvider } from '@/contexts/CalendarPickerContext';

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <AuthProvider>
      <NotificationProvider>
        <CalendarPickerProvider>
          {children}
        </CalendarPickerProvider>
      </NotificationProvider>
    </AuthProvider>
  );
}