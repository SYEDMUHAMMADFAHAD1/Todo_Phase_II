'use client';

import { Suspense } from 'react';
import AuthForm from '@/components/auth/AuthForm';
import { useAuth } from '@/hooks/auth';

function SignInContent() {
  const { signIn, isLoading } = useAuth();

  const handleSignIn = async (data: { email: string; password: string }) => {
    return await signIn(data.email, data.password);
  };

  return <AuthForm mode="signin" onSubmit={handleSignIn} isLoading={isLoading} />;
}

export default function SignInPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-slate-900 to-indigo-950 flex items-center justify-center p-4">
      <Suspense fallback={<div>Loading...</div>}>
        <SignInContent />
      </Suspense>
    </div>
  );
}