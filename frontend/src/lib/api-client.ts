import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';
import { ApiError } from '@/types/auth';

// Custom Error class that extends Error so instanceof Error works
export class ApiErrorClass extends Error {
  public statusCode: number;
  public errors?: Record<string, string[]>;

  constructor(message: string, statusCode: number, errors?: Record<string, string[]>) {
    super(message);
    this.statusCode = statusCode;
    this.errors = errors;
    this.name = 'ApiError';
    Object.setPrototypeOf(this, ApiErrorClass.prototype);
  }
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
      // Removed withCredentials: true since we're using JWT tokens in Authorization header
      // The authentication is handled via JWT tokens stored in localStorage
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Request interceptor to add auth token
    this.client.interceptors.request.use(
      (config) => {
        // Always check localStorage fresh before each request
        const token = localStorage.getItem('todo_app_token');

        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
          console.log('🔐 Authorization header attached:', { token: token.slice(0, 20) + '...' });
        } else {
          console.warn('⚠️ No token found in localStorage');
        }

        return config;
      },
      (error) => {
        console.error('Request interceptor error:', error);
        return Promise.reject(error);
      }
    );

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response: AxiosResponse) => response,
      (error: AxiosError) => {
        const data = error.response?.data as any;
        const statusCode = error.response?.status || 500;
        const message = data?.detail || error.message || 'An unknown error occurred';

        console.error('API Error:', statusCode, message, data);

        // Handle 401 Unauthorized (token expired or invalid)
        if (statusCode === 401) {
          localStorage.removeItem('todo_app_token');
          window.location.href = '/signin';
        }

        // Throw proper Error object so instanceof Error works
        const apiErrorObj = new ApiErrorClass(message, statusCode, data?.errors);
        return Promise.reject(apiErrorObj);
      }
    );
  }

  public async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    try {
      const response = await this.client.get<T>(url, config);
      return response.data;
    } catch (error) {
      console.error(`GET request failed to ${url}:`, error);
      throw error;
    }
  }

  public async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    try {
      const response = await this.client.post<T>(url, data, config);
      return response.data;
    } catch (error) {
      console.error(`POST request failed to ${url}:`, error);
      throw error;
    }
  }

  public async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    try {
      const response = await this.client.put<T>(url, data, config);
      return response.data;
    } catch (error) {
      console.error(`PUT request failed to ${url}:`, error);
      throw error;
    }
  }

  public async patch<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    try {
      const response = await this.client.patch<T>(url, data, config);
      return response.data;
    } catch (error) {
      console.error(`PATCH request failed to ${url}:`, error);
      throw error;
    }
  }

  public async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    try {
      const response = await this.client.delete<T>(url, config);
      return response.data;
    } catch (error) {
      console.error(`DELETE request failed to ${url}:`, error);
      throw error;
    }
  }

  public setAuthToken(token: string) {
    localStorage.setItem('todo_app_token', token);
    this.client.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  }

  public clearAuthToken() {
    localStorage.removeItem('todo_app_token');
    delete this.client.defaults.headers.common['Authorization'];
  }
}

export const apiClient = new ApiClient();
