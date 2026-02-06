'use client';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import { ReactNode } from 'react';

export default function AuthenticatedLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <ProtectedRoute redirectTo="/signin">
      {children}
    </ProtectedRoute>
  );
}