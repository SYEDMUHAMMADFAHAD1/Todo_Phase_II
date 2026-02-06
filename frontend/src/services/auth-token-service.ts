import { Session } from '@/types/auth';
import { sessionStorage } from '@/lib/session';

export class AuthTokenService {
  private refreshTimeout: NodeJS.Timeout | null = null;

  async initialize(session: Session | null): Promise<void> {
    if (!session) {
      this.clearToken();
      return;
    }

    if (sessionStorage.isSessionExpired(session)) {
      this.clearToken();
      return;
    }

    // Save session
    sessionStorage.saveSession(session);

    // Schedule token refresh
    this.scheduleTokenRefresh(session);
  }

  getToken(): string | null {
    return sessionStorage.getToken();
  }

  isTokenValid(): boolean {
    const session = sessionStorage.getSession();
    return session !== null && !sessionStorage.isSessionExpired(session);
  }

  clearToken(): void {
    sessionStorage.clearSession();
    this.clearRefreshTimeout();
  }

  async refreshToken(): Promise<{ success: boolean; session?: Session }> {
    try {
      // In a real implementation, this would call your backend refresh endpoint
      const session = sessionStorage.getSession();
      if (!session) {
        return { success: false };
      }

      // For now, we'll just validate the current session
      // In a real app, you would make an API call to refresh the token
      if (sessionStorage.shouldRefreshSession(session)) {
        // Simulate token refresh
        const refreshedSession: Session = {
          ...session,
          expiresAt: new Date(Date.now() + 1000 * 60 * 30).toISOString(), // Extend 30 minutes
        };

        sessionStorage.saveSession(refreshedSession);
        this.scheduleTokenRefresh(refreshedSession);

        return { success: true, session: refreshedSession };
      }

      return { success: true, session };
    } catch (error) {
      console.error('Token refresh failed:', error);
      return { success: false };
    }
  }

  private scheduleTokenRefresh(session: Session): void {
    this.clearRefreshTimeout();

    const refreshTime = sessionStorage.getRemainingSessionTime(session) - (5 * 60 * 1000); // 5 minutes before expiration

    if (refreshTime > 0) {
      this.refreshTimeout = setTimeout(async () => {
        await this.refreshToken();
      }, refreshTime);
    }
  }

  private clearRefreshTimeout(): void {
    if (this.refreshTimeout) {
      clearTimeout(this.refreshTimeout);
      this.refreshTimeout = null;
    }
  }

  // Clean up method to call when component unmounts or user logs out
  destroy(): void {
    this.clearRefreshTimeout();
  }
}

export const authTokenService = new AuthTokenService();