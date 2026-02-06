// Custom auth client for Better Auth integration
// Since Better Auth v1.x doesn't have a standardized client API, we'll implement a custom one
// that communicates with our backend auth endpoints

class BetterAuthClient {
  private baseUrl: string;

  constructor() {
    // Use the same base URL as the API client for consistency
    this.baseUrl = process.env.NEXT_PUBLIC_API_URL?.replace('/api', '') || 'http://localhost:8000';
  }

  async getSession() {
    try {
      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
      };

      // Note: localStorage is only available in the browser
      // On the server-side (middleware), this will have no token
      // which is fine - the API will return 401 and we treat it as no session
      if (typeof window !== 'undefined') {
        const token = localStorage.getItem('todo_app_token');
        if (token) {
          headers['Authorization'] = `Bearer ${token}`;
        }
      }

      const response = await fetch(`${this.baseUrl}/api/auth/session`, {
        credentials: 'include',
        headers,
      });

      if (!response.ok) {
        if (response.status === 401) {
          return { data: null, error: { message: 'Unauthorized' } };
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return { data, error: null };
    } catch (error) {
      console.error('Error getting session:', error);
      return { data: null, error: error instanceof Error ? error : new Error(String(error)) };
    }
  }

  async signIn(email: string, password: string) {
    try {
      const response = await fetch(`${this.baseUrl}/api/auth/signin`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        return { data: null, error: { message: errorData.detail || 'Sign in failed' } };
      }

      const data = await response.json();
      return { data, error: null };
    } catch (error) {
      console.error('Error signing in:', error);
      return { data: null, error: { message: error instanceof Error ? error.message : 'Sign in failed' } };
    }
  }

  async signUp(email: string, password: string, name?: string) {
    try {
      const response = await fetch(`${this.baseUrl}/api/auth/signup`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password, name }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        return { data: null, error: { message: errorData.detail || 'Sign up failed' } };
      }

      const data = await response.json();
      return { data, error: null };
    } catch (error) {
      console.error('Error signing up:', error);
      return { data: null, error: { message: error instanceof Error ? error.message : 'Sign up failed' } };
    }
  }

  async signOut() {
    try {
      const response = await fetch(`${this.baseUrl}/api/auth/signout`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return { data: await response.json(), error: null };
    } catch (error) {
      console.error('Error signing out:', error);
      return { data: null, error: error instanceof Error ? error : new Error(String(error)) };
    }
  }
}

// Create and export the auth client instance
export const auth = new BetterAuthClient();

// Export types for client-side usage
export type { Session, User } from 'better-auth';

// Helper functions for middleware and other parts of the app
export const getSession = async () => {
  try {
    const result = await auth.getSession();
    if (result.error || !result.data) {
      return null;
    }
    return result.data;
  } catch (error) {
    console.error('Error getting session:', error);
    return null;
  }
};

export const signOut = async (options?: any) => {
  try {
    await auth.signOut();

    // Execute any success callback if provided
    if (options?.fetchOptions?.onSuccess) {
      options.fetchOptions.onSuccess();
    }
  } catch (error) {
    console.error('Error signing out:', error);
  }
};