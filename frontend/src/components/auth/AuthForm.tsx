'use client';

import React, { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import Card from '@/components/ui/Card';
import Link from 'next/link';

interface AuthFormProps {
  mode: 'signin' | 'signup';
  onSubmit: (data: { email: string; password: string; name?: string }) => Promise<{ success: boolean; error?: string }>;
  isLoading?: boolean;
}

export default function AuthForm({ mode, onSubmit, isLoading = false }: AuthFormProps) {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    name: '',
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [submitError, setSubmitError] = useState('');

  useEffect(() => {
    const error = searchParams.get('error');
    if (error) {
      setSubmitError('Session expired. Please sign in again.');
    }
  }, [searchParams]);

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    }

    if (mode === 'signup') {
      if (!formData.name) {
        newErrors.name = 'Name is required';
      }
      if (!formData.confirmPassword) {
        newErrors.confirmPassword = 'Please confirm your password';
      } else if (formData.password !== formData.confirmPassword) {
        newErrors.confirmPassword = 'Passwords do not match';
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitError('');

    if (!validateForm()) {
      return;
    }

    try {
      const result = await onSubmit({
        email: formData.email,
        password: formData.password,
        name: mode === 'signup' ? formData.name : undefined,
      });

      if (result.success) {
        const redirectTo = searchParams.get('redirect') || '/authenticated/dashboard';
        router.push(redirectTo);
      } else {
        setSubmitError(result.error || 'An error occurred');
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'An unexpected error occurred';
      setSubmitError(errorMessage);
      console.error('Form submission error:', error);
    }
  };

  return (
    <div className="w-full max-w-md">
      <div className="bg-slate-800/50 backdrop-blur-xl rounded-2xl border border-slate-700/50 shadow-2xl p-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-bold text-white">
            {mode === 'signin' ? 'Sign in to your account' : 'Create your account'}
          </h2>
        </div>
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {submitError && (
            <div className="rounded-lg bg-rose-900/30 p-4 border border-rose-700/50 backdrop-blur-sm">
              <div className="text-sm text-rose-300">{submitError}</div>
            </div>
          )}
          <div className="space-y-5">
            {mode === 'signup' && (
              <Input
                id="name"
                name="name"
                type="text"
                autoComplete="name"
                required
                label="Full Name"
                value={formData.name}
                onChange={handleChange}
                error={errors.name}
                placeholder="Full Name"
              />
            )}
            <Input
              id="email"
              name="email"
              type="email"
              autoComplete="email"
              required
              label="Email address"
              value={formData.email}
              onChange={handleChange}
              error={errors.email}
              placeholder="Email address"
            />
            <Input
              id="password"
              name="password"
              type="password"
              autoComplete={mode === 'signin' ? 'current-password' : 'new-password'}
              required
              label="Password"
              value={formData.password}
              onChange={handleChange}
              error={errors.password}
              placeholder="Password"
            />
            {mode === 'signup' && (
              <Input
                id="confirmPassword"
                name="confirmPassword"
                type="password"
                autoComplete="new-password"
                required
                label="Confirm Password"
                value={formData.confirmPassword}
                onChange={handleChange}
                error={errors.confirmPassword}
                placeholder="Confirm Password"
              />
            )}
          </div>

          <div>
            <Button
              type="submit"
              className="w-full flex justify-center py-3 rounded-xl text-base font-semibold bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 shadow-lg hover:shadow-indigo-500/30 transition-all duration-200 transform hover:-translate-y-0.5"
              disabled={isLoading}
              isLoading={isLoading}
            >
              {mode === 'signin' ? 'Sign in' : 'Sign up'}
            </Button>
          </div>
        </form>

        <div className="mt-8">
          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-slate-700/50" />
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-4 bg-slate-800/50 text-slate-400 backdrop-blur-sm">
                {mode === 'signin' ? 'New to Todo App?' : 'Already have an account?'}
              </span>
            </div>
          </div>

          <div className="mt-6 text-center">
            <Link
              href={mode === 'signin' ? '/signup' : '/signin'}
              className="font-medium text-indigo-400 hover:text-indigo-300 hover:underline"
            >
              {mode === 'signin' ? 'Create an account' : 'Sign in to your account'}
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
