// Utility functions for authentication

export const getAuthToken = async (): Promise<string | null> => {
  // In a real implementation, this would get the token from wherever it's stored
  // For now, we'll assume it's in localStorage
  if (typeof window !== 'undefined') {
    return localStorage.getItem('todo_app_token');
  }
  return null;
};

export const setAuthToken = (token: string): void => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('todo_app_token', token);
  }
};

export const removeAuthToken = (): void => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('todo_app_token');
  }
};