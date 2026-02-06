import React, { createContext, useContext, useEffect, useState } from 'react';
import { authService } from '@/services/auth-service';
import { authTokenService } from '@/services/auth-token-service';
import { User, Session, AuthState } from '@/types/auth';

type AuthContextType = AuthState & {
  signIn: (email: string, password: string) => Promise<{ success: boolean; error?: string }>;
  signUp: (email: string, password: string, name?: string) => Promise<{ success: boolean; error?: string }>;
  signOut: () => Promise<{ success: boolean; error?: string }>;
  refreshSession: () => Promise<{ success: boolean; error?: string }>;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function useAuthContext() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuthContext must be used within an AuthProvider');
  }
  return context;
}

type AuthProviderProps = {
  children: React.ReactNode;
};

export function AuthProvider({ children }: AuthProviderProps) {
  const [state, setState] = useState<AuthState>({
    user: null,
    session: null,
    isLoading: true,
    error: null,
  });

  useEffect(() => {
    initializeAuth();

    // Clean up token service on unmount
    return () => {
      authTokenService.destroy();
    };
  }, []);

  const initializeAuth = async () => {
    try {
      // Try to get session from API
      const session = await authService.getSession();

      // Only set session if it was successful and has user data
      if (session && session.user) {
        await authTokenService.initialize(session.session);

        setState({
          user: session.user,
          session: session.session,
          isLoading: false,
          error: null,
        });
      } else {
        // No session, user is not authenticated
        setState({
          user: null,
          session: null,
          isLoading: false,
          error: null,
        });
      }
    } catch (error) {
      // Session not found or invalid, user is not authenticated
      setState({
        user: null,
        session: null,
        isLoading: false,
        error: null,
      });
    }
  };

  const signIn = async (email: string, password: string) => {
    try {
      setState(prev => ({ ...prev, isLoading: true, error: null }));

      const response = await authService.signIn({ email, password });

      await authTokenService.initialize(response.session);

      setState({
        user: response.user,
        session: response.session,
        isLoading: false,
        error: null,
      });

      return { success: true };
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Sign in failed';
      setState(prev => ({ ...prev, isLoading: false, error: errorMessage }));
      return { success: false, error: errorMessage };
    }
  };

  const signUp = async (email: string, password: string, name?: string) => {
    try {
      setState(prev => ({ ...prev, isLoading: true, error: null }));

      const response = await authService.signUp({ email, password, name });

      await authTokenService.initialize(response.session);

      setState({
        user: response.user,
        session: response.session,
        isLoading: false,
        error: null,
      });

      return { success: true };
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Sign up failed';
      setState(prev => ({ ...prev, isLoading: false, error: errorMessage }));
      return { success: false, error: errorMessage };
    }
  };

  const signOut = async () => {
    try {
      await authService.signOut();
      authTokenService.clearToken();

      setState({
        user: null,
        session: null,
        isLoading: false,
        error: null,
      });

      return { success: true };
    } catch (error) {
      // Even if API call fails, clear local state
      authTokenService.clearToken();
      setState({
        user: null,
        session: null,
        isLoading: false,
        error: null,
      });
      return { success: true };
    }
  };

  const refreshSession = async () => {
    try {
      const response = await authService.refreshToken();
      await authTokenService.initialize(response.session);

      setState({
        user: response.user,
        session: response.session,
        isLoading: false,
        error: null,
      });

      return { success: true };
    } catch (error) {
      return { success: false, error: 'Failed to refresh session' };
    }
  };

  const value: AuthContextType = {
    ...state,
    signIn,
    signUp,
    signOut,
    refreshSession,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}