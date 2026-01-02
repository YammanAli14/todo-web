'use client';

/**
 * Authentication context for managing user state.
 */
import React, { createContext, useContext, useState, useEffect } from 'react';
import { User, SignupRequest, SigninRequest } from '../types';
import { authApi } from '../api/client';

interface AuthContextType {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  signup: (data: SignupRequest) => Promise<void>;
  signin: (data: SigninRequest) => Promise<void>;
  signout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const TOKEN_KEY = 'auth_token';
const USER_KEY = 'auth_user';

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Load user from localStorage on mount
  useEffect(() => {
    const storedToken = localStorage.getItem(TOKEN_KEY);
    const storedUser = localStorage.getItem(USER_KEY);

    if (storedToken && storedUser) {
      try {
        setToken(storedToken);
        setUser(JSON.parse(storedUser));
      } catch (error) {
        console.error('Failed to parse stored user:', error);
        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem(USER_KEY);
      }
    }

    setIsLoading(false);
  }, []);

  const signup = async (data: SignupRequest) => {
    try {
      const response = await authApi.signup(data);
      setUser(response.user);
      setToken(response.access_token);
      localStorage.setItem(TOKEN_KEY, response.access_token);
      localStorage.setItem(USER_KEY, JSON.stringify(response.user));
    } catch (error) {
      throw error;
    }
  };

  const signin = async (data: SigninRequest) => {
    try {
      const response = await authApi.signin(data);
      setUser(response.user);
      setToken(response.access_token);
      localStorage.setItem(TOKEN_KEY, response.access_token);
      localStorage.setItem(USER_KEY, JSON.stringify(response.user));
    } catch (error) {
      throw error;
    }
  };

  const signout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    // Optionally call backend signout endpoint
    authApi.signout().catch(() => {
      // Ignore errors on signout
    });
  };

  return (
    <AuthContext.Provider
      value={{ user, token, isLoading, signup, signin, signout }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
