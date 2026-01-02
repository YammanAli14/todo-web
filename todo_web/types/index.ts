// User types
export interface User {
  id: number;
  email: string;
  created_at: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterCredentials {
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

// Task types
export interface Task {
  id: number;
  title: string;
  is_complete: boolean;
  created_at: string;
  updated_at: string;
}

export interface TaskCreate {
  title: string;
}

export interface TaskUpdate {
  title: string;
}

// API Error
export interface ApiError {
  detail: string;
}
