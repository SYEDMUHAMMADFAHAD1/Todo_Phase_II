import { useAuth as useAuthFromContext } from '@/contexts/AuthContext';

export function useAuth() {
  const auth = useAuthFromContext();
  return {
    ...auth,
    isAuthenticated: !!auth.user,
  };
}

export function useSession() {
  const auth = useAuth();
  return {
    user: auth.user,
    session: auth.session,
    isLoading: auth.isLoading,
    isAuthenticated: !!auth.user,
    signIn: auth.signIn,
    signUp: auth.signUp,
    signOut: auth.signOut,
    refreshSession: auth.refreshSession,
  };
}

export function useProtectedRoute(redirectTo = '/signin') {
  const { user, isLoading, isAuthenticated, signIn, signUp, signOut, refreshSession } = useAuth();

  return {
    user,
    isLoading,
    isAuthenticated,
    signIn,
    signUp,
    signOut,
    refreshSession,
  };
}