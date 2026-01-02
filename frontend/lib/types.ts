// User Types
export interface User {
  id: number;
  email: string;
  created_at: string;
  updated_at: string;
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
  access_token: string;
  token_type: string;
}

// Todo Types
export interface Todo {
  id: number;
  user_id: number;
  title: string;
  is_complete: boolean;
  created_at: string;
  updated_at: string;
}

export interface TodoCreateRequest {
  title: string;
}

export interface TodoUpdateRequest {
  title: string;
}

// Error Types
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
