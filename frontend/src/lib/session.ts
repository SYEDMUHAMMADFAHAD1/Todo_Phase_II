import { Session } from '@/types/auth';

export class SessionStorage {
  private static readonly SESSION_KEY = 'todo_app_session';
  private static readonly TOKEN_KEY = 'todo_app_token';

  static saveSession(session: Session): void {
    if (typeof window !== 'undefined') {
      try {
        localStorage.setItem(this.SESSION_KEY, JSON.stringify(session));
      } catch (error) {
        console.error('Failed to save session to localStorage:', error);
      }
    }
  }

  static getSession(): Session | null {
    if (typeof window !== 'undefined') {
      try {
        const stored = localStorage.getItem(this.SESSION_KEY);
        return stored ? JSON.parse(stored) : null;
      } catch (error) {
        console.error('Failed to retrieve session from localStorage:', error);
        return null;
      }
    }
    return null;
  }

  static saveToken(token: string): void {
    if (typeof window !== 'undefined') {
      try {
        sessionStorage.setItem(this.TOKEN_KEY, token);
      } catch (error) {
        console.error('Failed to save token to sessionStorage:', error);
      }
    }
  }

  static getToken(): string | null {
    if (typeof window !== 'undefined') {
      try {
        return sessionStorage.getItem(this.TOKEN_KEY);
      } catch (error) {
        console.error('Failed to retrieve token from sessionStorage:', error);
        return null;
      }
    }
    return null;
  }

  static clearSession(): void {
    if (typeof window !== 'undefined') {
      try {
        localStorage.removeItem(this.SESSION_KEY);
        sessionStorage.removeItem(this.TOKEN_KEY);
      } catch (error) {
        console.error('Failed to clear session storage:', error);
      }
    }
  }

  static isSessionExpired(session: Session): boolean {
    if (!session?.expiresAt) return true;

    const expirationDate = new Date(session.expiresAt);
    const now = new Date();
    return now >= expirationDate;
  }

  static getRemainingSessionTime(session: Session): number {
    if (!session?.expiresAt) return 0;

    const expirationDate = new Date(session.expiresAt);
    const now = new Date();
    return Math.max(0, expirationDate.getTime() - now.getTime());
  }

  static shouldRefreshSession(session: Session): boolean {
    if (!session?.expiresAt) return true;

    const expirationDate = new Date(session.expiresAt);
    const now = new Date();
    const refreshThreshold = 5 * 60 * 1000; // 5 minutes before expiration

    return (expirationDate.getTime() - now.getTime()) <= refreshThreshold;
  }
}

// Export the class itself since it only has static methods
export { SessionStorage as sessionStorage };