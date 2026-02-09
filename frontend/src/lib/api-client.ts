import { getAuthToken } from '@/lib/auth-utils';
import { nanoid } from 'nanoid';

interface ChatResponse {
  conversation_id: string;
  response: string;
  message_id: string;
}

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

class ApiClient {
  private baseUrl: string;

  constructor() {
    // Use relative URLs to leverage Next.js rewrites when NEXT_PUBLIC_USE_REWRITE_PROXY is set
    if (process.env.NEXT_PUBLIC_USE_REWRITE_PROXY === 'true') {
      this.baseUrl = '';
    } else {
      this.baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
    }
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    // Add the API version prefix to all requests
    // If using relative URLs (empty baseUrl), don't add the baseUrl
    const url = this.baseUrl ? `${this.baseUrl}/api${endpoint}` : `/api${endpoint}`;

    const headers = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string> || {}),
    } as Record<string, string>;

    // Add auth token if available
    const token = await getAuthToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! Status: ${response.status}`);
    }

    return response.json();
  }

  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'GET'
    });
  }

  async post<T>(endpoint: string, data: any): Promise<T> {
    // Format date fields before sending to backend
    const formattedData = this.formatDatesForBackend(data);
    
    return this.request<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(formattedData),
    });
  }

  async put<T>(endpoint: string, data: any): Promise<T> {
    // Format date fields before sending to backend
    const formattedData = this.formatDatesForBackend(data);

    return this.request<T>(endpoint, {
      method: 'PUT',
      body: JSON.stringify(formattedData),
    });
  }

  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'DELETE',
    });
  }

  private formatDatesForBackend(obj: any): any {
    if (obj === null || obj === undefined) {
      return obj;
    }

    if (obj instanceof Date) {
      // Format date to ISO string for backend
      return obj.toISOString();
    }

    if (Array.isArray(obj)) {
      return obj.map(item => this.formatDatesForBackend(item));
    }

    if (typeof obj === 'object') {
      const formattedObj: any = {};
      for (const key in obj) {
        if (obj.hasOwnProperty(key)) {
          if (key === 'dateTime' || key === 'date_time') {
            // Specifically handle date and time fields
            if (obj[key] instanceof Date) {
              formattedObj[key] = obj[key].toISOString();
            } else {
              formattedObj[key] = obj[key];
            }
          } else {
            formattedObj[key] = this.formatDatesForBackend(obj[key]);
          }
        }
      }
      return formattedObj;
    }

    return obj;
  }

  async sendChatMessage(
    userId: string,
    message: string,
    conversationId?: string
  ): Promise<ChatResponse> {
    const body = {
      message,
      ...(conversationId && { conversation_id: conversationId }),
    };

    return this.request<ChatResponse>(`/${userId}/chat`, {
      method: 'POST',
      body: JSON.stringify(body),
    });
  }

  async getConversationHistory(userId: string, conversationId: string): Promise<{ conversation_id: string; messages: Message[] }> {
    return this.request<{ conversation_id: string; messages: Message[] }>(
      `/${userId}/conversations/${conversationId}/messages`,
      { method: 'GET' }
    );
  }
}

export const apiClient = new ApiClient();