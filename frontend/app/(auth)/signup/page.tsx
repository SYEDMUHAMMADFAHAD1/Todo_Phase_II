'use client';

import { Suspense } from 'react';
import AuthForm from '@/components/auth/AuthForm';
import { useAuth } from '@/hooks/auth';

function SignUpContent() {
  const { signUp, isLoading } = useAuth();

  const handleSignUp = async (data: { email: string; password: string; name?: string }) => {
    return await signUp(data.email, data.password, data.name);
  };

  return <AuthForm mode="signup" onSubmit={handleSignUp} isLoading={isLoading} />;
}

export default function SignUpPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-slate-900 to-indigo-950 flex items-center justify-center p-4">
      <Suspense fallback={<div>Loading...</div>}>
        <SignUpContent />
      </Suspense>
    </div>
  );
}