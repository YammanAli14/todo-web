# TypeScript API Client Interface

**Date**: 2026-01-02
**Feature**: 1-phase-ii-fullstack
**Purpose**: Define TypeScript types and API client structure for frontend

---

## Type Definitions

### User Types

```typescript
export interface User {
  id: number;
  email: string;
  created_at: string;  // ISO 8601 datetime
  updated_at: string;  // ISO 8601 datetime
}

export interface SignupRequest {
  email: string;
  password: string;
}

export interface SigninRequest {
  email: string;
  password: string;
}

export interface AuthResponse {
  user: User;
  token: string;
}
```

### Todo Types

```typescript
export interface Todo {
  id: number;
  title: string;
  is_complete: boolean;
  created_at: string;  // ISO 8601 datetime
  updated_at: string;  // ISO 8601 datetime
}

export interface TodoCreateRequest {
  title: string;
}

export interface TodoUpdateRequest {
  title: string;
}
```

### Error Types

```typescript
export interface ApiError {
  detail: string;
  code?: string;
  field?: string;
}

export class ApiException extends Error {
  constructor(
    public status: number,
    public error: ApiError
  ) {
    super(error.detail);
    this.name = 'ApiException';
  }
}
```

---

## API Client Structure

### Base Client

```typescript
// lib/api/client.ts

export interface ApiClientConfig {
  baseUrl: string;
  getToken: () => string | null;
  onUnauthorized?: () => void;
}

export class ApiClient {
  constructor(private config: ApiClientConfig) {}

  private async request<T>(
    endpoint: string,
    options?: RequestInit
  ): Promise<T> {
    const token = this.config.getToken();
    const headers = {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options?.headers,
    };

    const response = await fetch(`${this.config.baseUrl}${endpoint}`, {
      ...options,
      headers,
    });

    if (response.status === 401 && this.config.onUnauthorized) {
      this.config.onUnauthorized();
      throw new ApiException(401, {
        detail: 'Authentication required',
        code: 'UNAUTHORIZED',
      });
    }

    if (!response.ok) {
      const error: ApiError = await response.json();
      throw new ApiException(response.status, error);
    }

    if (response.status === 204) {
      return null as T;
    }

    return response.json();
  }

  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET' });
  }

  async post<T>(endpoint: string, body?: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: body ? JSON.stringify(body) : undefined,
    });
  }

  async put<T>(endpoint: string, body: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: JSON.stringify(body),
    });
  }

  async patch<T>(endpoint: string, body?: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PATCH',
      body: body ? JSON.stringify(body) : undefined,
    });
  }

  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'DELETE' });
  }
}
```

---

## Authentication API

### Interface

```typescript
// lib/api/auth.ts

export interface AuthApi {
  signup(request: SignupRequest): Promise<AuthResponse>;
  signin(request: SigninRequest): Promise<AuthResponse>;
  signout(): Promise<void>;
  getCurrentUser(): Promise<User>;
}
```

### Implementation

```typescript
export class AuthApiImpl implements AuthApi {
  constructor(private client: ApiClient) {}

  async signup(request: SignupRequest): Promise<AuthResponse> {
    return this.client.post<AuthResponse>('/auth/signup', request);
  }

  async signin(request: SigninRequest): Promise<AuthResponse> {
    return this.client.post<AuthResponse>('/auth/signin', request);
  }

  async signout(): Promise<void> {
    return this.client.post<void>('/auth/signout');
  }

  async getCurrentUser(): Promise<User> {
    return this.client.get<User>('/auth/me');
  }
}
```

---

## Todo API

### Interface

```typescript
// lib/api/todos.ts

export interface TodoApi {
  getTodos(): Promise<Todo[]>;
  getTodo(id: number): Promise<Todo>;
  createTodo(request: TodoCreateRequest): Promise<Todo>;
  updateTodo(id: number, request: TodoUpdateRequest): Promise<Todo>;
  deleteTodo(id: number): Promise<void>;
  toggleTodo(id: number): Promise<Todo>;
}
```

### Implementation

```typescript
export class TodoApiImpl implements TodoApi {
  constructor(private client: ApiClient) {}

  async getTodos(): Promise<Todo[]> {
    return this.client.get<Todo[]>('/todos');
  }

  async getTodo(id: number): Promise<Todo> {
    return this.client.get<Todo>(`/todos/${id}`);
  }

  async createTodo(request: TodoCreateRequest): Promise<Todo> {
    return this.client.post<Todo>('/todos', request);
  }

  async updateTodo(id: number, request: TodoUpdateRequest): Promise<Todo> {
    return this.client.put<Todo>(`/todos/${id}`, request);
  }

  async deleteTodo(id: number): Promise<void> {
    return this.client.delete<void>(`/todos/${id}`);
  }

  async toggleTodo(id: number): Promise<Todo> {
    return this.client.patch<Todo>(`/todos/${id}/toggle`);
  }
}
```

---

## API Factory

### Usage

```typescript
// lib/api/index.ts

export interface Api {
  auth: AuthApi;
  todos: TodoApi;
}

export function createApi(config: ApiClientConfig): Api {
  const client = new ApiClient(config);

  return {
    auth: new AuthApiImpl(client),
    todos: new TodoApiImpl(client),
  };
}

// Example usage in Next.js:
const api = createApi({
  baseUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  getToken: () => localStorage.getItem('auth_token'),
  onUnauthorized: () => {
    localStorage.removeItem('auth_token');
    window.location.href = '/auth/signin';
  },
});

// Use in components:
const todos = await api.todos.getTodos();
const user = await api.auth.getCurrentUser();
```

---

## Error Handling Examples

### Frontend Error Handling

```typescript
// Example: Handle signup errors
try {
  const response = await api.auth.signup({ email, password });
  // Success: store token and redirect
  localStorage.setItem('auth_token', response.token);
  router.push('/todos');
} catch (error) {
  if (error instanceof ApiException) {
    switch (error.error.code) {
      case 'EMAIL_EXISTS':
        setError('This email is already registered');
        break;
      case 'INVALID_EMAIL':
        setError('Please enter a valid email address');
        break;
      case 'WEAK_PASSWORD':
        setError('Password must be at least 8 characters');
        break;
      default:
        setError(error.error.detail);
    }
  } else {
    setError('Network error: Please try again');
  }
}
```

```typescript
// Example: Handle todo creation errors
try {
  const newTodo = await api.todos.createTodo({ title: todoTitle });
  setTodos([...todos, newTodo]);
  setTodoTitle('');
} catch (error) {
  if (error instanceof ApiException) {
    if (error.status === 401) {
      // Redirect to signin (handled by onUnauthorized callback)
    } else if (error.error.field === 'title') {
      setTitleError(error.error.detail);
    } else {
      setError('Failed to create todo');
    }
  } else {
    setError('Network error: Please try again');
  }
}
```

---

## Request/Response Flow

### Authentication Flow

```
Frontend                    Backend
   │                           │
   │  POST /auth/signup        │
   ├──────────────────────────>│
   │  { email, password }       │
   │                           │
   │  201 Created              │
   │<───────────────────────────┤
   │  { user, token }           │
   │                           │
   │  Store token in           │
   │  localStorage             │
   │                           │
```

### Todo CRUD Flow

```
Frontend                    Backend
   │                           │
   │  GET /todos               │
   ├──────────────────────────>│
   │  Authorization: Bearer    │
   │  <token>                  │
   │                           │
   │  200 OK                   │
   │<───────────────────────────┤
   │  [{ id, title, ... }]     │
   │                           │
   │  POST /todos              │
   ├──────────────────────────>│
   │  { title: "..." }         │
   │                           │
   │  201 Created              │
   │<───────────────────────────┤
   │  { id, title, ... }       │
   │                           │
```

---

*End of TypeScript API Client Interface*
