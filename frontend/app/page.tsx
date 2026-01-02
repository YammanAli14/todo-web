'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/lib/auth/AuthContext';

export default function HomePage() {
  const router = useRouter();
  const { user, isLoading } = useAuth();

  useEffect(() => {
    if (!isLoading && user) {
      // Redirect to todos if already signed in
      router.push('/todos');
    }
  }, [user, isLoading, router]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-gray-600">Loading...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4">
      <div className="max-w-2xl w-full text-center space-y-8">
        <h1 className="text-5xl font-bold text-gray-900">
          Welcome to Todo App
        </h1>
        <p className="text-xl text-gray-600">
          Manage your tasks efficiently with our simple and elegant todo application.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center mt-8">
          <Link
            href="/auth/signup"
            className="px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 md:py-4 md:text-lg md:px-10"
          >
            Get Started
          </Link>
          <Link
            href="/auth/signin"
            className="px-8 py-3 border border-gray-300 text-base font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 md:py-4 md:text-lg md:px-10"
          >
            Sign In
          </Link>
        </div>

        <div className="mt-12 grid grid-cols-1 gap-8 sm:grid-cols-3">
          <div className="text-center">
            <div className="text-3xl font-bold text-blue-600 mb-2">✓</div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Simple</h3>
            <p className="text-gray-600">Easy to use interface for managing your tasks</p>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-blue-600 mb-2">⚡</div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Fast</h3>
            <p className="text-gray-600">Quick access to all your todos</p>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-blue-600 mb-2">🔒</div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Secure</h3>
            <p className="text-gray-600">Your data is protected with authentication</p>
          </div>
        </div>
      </div>
    </div>
  );
}
