/**
 * API client for backend communication.
 */
import {
  SignupRequest,
  SigninRequest,
  AuthResponse,
  User,
  ApiException,
} from '../types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Make an API request with error handling.
 */
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_URL}${endpoint}`;

  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new ApiException(response.status, error);
    }

    return await response.json();
  } catch (error) {
    if (error instanceof ApiException) {
      throw error;
    }
    // Network or other errors
    throw new Error('Network error or server unavailable');
  }
}

/**
 * Authentication API methods.
 */
export const authApi = {
  /**
   * Register a new user.
   */
  async signup(data: SignupRequest): Promise<AuthResponse> {
    return apiRequest<AuthResponse>('/auth/signup', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  /**
   * Sign in an existing user.
   */
  async signin(data: SigninRequest): Promise<AuthResponse> {
    return apiRequest<AuthResponse>('/auth/signin', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  /**
   * Sign out the current user (client-side only).
   */
  async signout(): Promise<void> {
    // JWT tokens are stateless, so signout is handled client-side
    // The backend endpoint exists for API completeness
    return apiRequest<void>('/auth/signout', {
      method: 'POST',
    });
  },

  /**
   * Get current authenticated user.
   */
  async me(token: string): Promise<User> {
    return apiRequest<User>('/auth/me', {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  },
};

/**
 * Todos API methods.
 */
export const todosApi = {
  /**
   * Get all todos for the current user.
   */
  async getAll(token: string): Promise<any[]> {
    return apiRequest<any[]>('/todos', {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  },

  /**
   * Create a new todo.
   */
  async create(token: string, title: string): Promise<any> {
    return apiRequest<any>('/todos', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ title }),
    });
  },

  /**
   * Update a todo's title.
   */
  async update(token: string, todoId: number, title: string): Promise<any> {
    return apiRequest<any>(`/todos/${todoId}`, {
      method: 'PUT',
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ title }),
    });
  },

  /**
   * Toggle todo completion status.
   */
  async toggle(token: string, todoId: number): Promise<any> {
    return apiRequest<any>(`/todos/${todoId}/toggle`, {
      method: 'PATCH',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  },

  /**
   * Delete a todo.
   */
  async delete(token: string, todoId: number): Promise<void> {
    return apiRequest<void>(`/todos/${todoId}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  },
};
