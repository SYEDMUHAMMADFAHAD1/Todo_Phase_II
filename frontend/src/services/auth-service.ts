import { LoginCredentials, RegisterCredentials, AuthResponse, ApiError, User } from '@/types/auth';
import { sessionStorage } from '@/lib/session';

// Use the same base URL as the API client
// Remove /api suffix since we'll add it with basePath
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

// Ensure no trailing slash
const cleanBaseUrl = API_BASE_URL.endsWith('/') ? API_BASE_URL.slice(0, -1) : API_BASE_URL;

export class AuthService {
  private basePath = '/auth';

  async signIn(credentials: LoginCredentials): Promise<AuthResponse> {
    try {
      const url = `${cleanBaseUrl}${this.basePath}/signin`;
      console.log('🔐 Signin request:', { url, email: credentials.email });

      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.error('❌ Signin error:', errorData);
        throw new Error(errorData.detail || `Sign in failed (${response.status})`);
      }

      const data = await response.json();
      console.log('✅ Signin successful');

      const authResponse = {
        user: data.user,
        session: data.session,
        token: data.token,
      };

      // Store token SYNCHRONOUSLY before returning
      if (authResponse.token) {
        localStorage.setItem('todo_app_token', authResponse.token);
        console.log('✅ Token stored in localStorage');
      }

      return authResponse;
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Sign in failed';
      console.error('🚨 Signin error:', message);
      throw new Error(message);
    }
  }

  async signUp(credentials: RegisterCredentials): Promise<AuthResponse> {
    try {
      const url = `${cleanBaseUrl}${this.basePath}/signup`;
      console.log('🔐 Signup request:', { url, email: credentials.email });

      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.error('❌ Signup error:', errorData);
        throw new Error(errorData.detail || `Sign up failed (${response.status})`);
      }

      const data = await response.json();
      console.log('✅ Signup successful');

      const authResponse = {
        user: data.user,
        session: data.session,
        token: data.token,
      };

      // Store token SYNCHRONOUSLY
      if (authResponse.token) {
        localStorage.setItem('todo_app_token', authResponse.token);
        console.log('✅ Token stored in localStorage');
      }

      return authResponse;
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Sign up failed';
      console.error('🚨 Signup error:', message);
      throw new Error(message);
    }
  }

  async signOut(): Promise<void> {
    try {
      await fetch(`${cleanBaseUrl}${this.basePath}/signout`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      // Clear local storage as well
      this.clearSession();
    } catch (error) {
      // Even if API call fails, we consider user signed out locally
      console.warn('Sign out API call failed, clearing local session anyway', error);
      this.clearSession();
    }
  }

  async getSession(): Promise<AuthResponse> {
    try {
      const token = localStorage.getItem('todo_app_token');

      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
      };

      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(`${cleanBaseUrl}${this.basePath}/session`, {
        method: 'GET',
        headers,
      });

      if (!response.ok) {
        if (response.status === 401) {
          localStorage.removeItem('todo_app_token');
          throw new Error('Unauthorized');
        }
        throw new Error('Failed to get session');
      }

      const data = await response.json();
      // Map the backend response to the expected AuthResponse format
      const authResponse = {
        user: data.user,
        session: data.session,
        token: token || '', // Use the existing token from storage since session endpoint returns empty token
      };

      // Store token for use by apiClient
      if (authResponse.token) {
        localStorage.setItem('todo_app_token', authResponse.token);
      }

      return authResponse;
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Failed to get session';
      console.error('🔍 Session error:', message, error);
      throw new Error(message);
    }
  }

  // Removed verifyToken as it's not supported by our backend
  async verifyToken(token: string): Promise<{ valid: boolean; user_id?: string; expires_at?: string }> {
    try {
      // Just validate by attempting to get session
      const session = await this.getSession();
      return {
        valid: true,
        user_id: session.user.id,
        expires_at: session.session.expiresAt
      };
    } catch (error) {
      return { valid: false };
    }
  }

  // Removed getCurrentUser as it's not supported by our backend
  async getCurrentUser(): Promise<User> {
    try {
      const session = await this.getSession();
      return session.user;
    } catch (error) {
      const apiError = error as ApiError;
      throw new Error(apiError.message || 'Failed to get current user');
    }
  }

  async refreshToken(): Promise<AuthResponse> {
    try {
      // For now, just get current session which will refresh if needed
      return await this.getSession();
    } catch (error) {
      const apiError = error as ApiError;
      throw new Error(apiError.message || 'Failed to refresh token');
    }
  }

  isAuthenticated(): boolean {
    // Check if we have a valid token in storage
    const token = localStorage.getItem('todo_app_token');
    return !!token;
  }

  clearSession(): void {
    // Clear all auth-related storage
    localStorage.removeItem('todo_app_token');
    localStorage.removeItem('todo_app_session');
    sessionStorage.clearSession();
  }
}

export const authService = new AuthService();