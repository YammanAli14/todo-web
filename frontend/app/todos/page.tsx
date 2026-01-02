'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth/AuthContext';
import { todosApi } from '@/lib/api/client';

interface Todo {
  id: number;
  user_id: number;
  title: string;
  is_complete: boolean;
  created_at: string;
  updated_at: string;
}

export default function TodosPage() {
  const router = useRouter();
  const { user, token, isLoading, signout } = useAuth();
  const [todos, setTodos] = useState<Todo[]>([]);
  const [newTodoTitle, setNewTodoTitle] = useState('');
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editingTitle, setEditingTitle] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!isLoading && !user) {
      router.push('/auth/signin');
    }
  }, [user, isLoading, router]);

  useEffect(() => {
    if (user && token) {
      loadTodos();
    }
  }, [user, token]);

  const loadTodos = async () => {
    if (!token) return;

    try {
      const data = await todosApi.getAll(token);
      setTodos(data);
      setError('');
    } catch (err: any) {
      setError('Failed to load todos');
      console.error(err);
    }
  };

  const handleCreateTodo = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!token || !newTodoTitle.trim()) return;

    setLoading(true);
    try {
      await todosApi.create(token, newTodoTitle.trim());
      setNewTodoTitle('');
      await loadTodos();
      setError('');
    } catch (err: any) {
      setError(err.error?.detail || 'Failed to create todo');
    } finally {
      setLoading(false);
    }
  };

  const handleToggleTodo = async (todoId: number) => {
    if (!token) return;

    try {
      await todosApi.toggle(token, todoId);
      await loadTodos();
      setError('');
    } catch (err: any) {
      setError(err.error?.detail || 'Failed to toggle todo');
    }
  };

  const handleStartEdit = (todo: Todo) => {
    setEditingId(todo.id);
    setEditingTitle(todo.title);
  };

  const handleCancelEdit = () => {
    setEditingId(null);
    setEditingTitle('');
  };

  const handleUpdateTodo = async (todoId: number) => {
    if (!token || !editingTitle.trim()) return;

    try {
      await todosApi.update(token, todoId, editingTitle.trim());
      setEditingId(null);
      setEditingTitle('');
      await loadTodos();
      setError('');
    } catch (err: any) {
      setError(err.error?.detail || 'Failed to update todo');
    }
  };

  const handleDeleteTodo = async (todoId: number) => {
    if (!token || !confirm('Are you sure you want to delete this todo?')) return;

    try {
      await todosApi.delete(token, todoId);
      await loadTodos();
      setError('');
    } catch (err: any) {
      setError(err.error?.detail || 'Failed to delete todo');
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-gray-600">Loading...</p>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">My Todos</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-gray-700">{user.email}</span>
              <button
                onClick={signout}
                className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
              >
                Sign Out
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-4xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        {error && (
          <div className="mb-4 rounded-md bg-red-50 p-4">
            <p className="text-sm text-red-800">{error}</p>
          </div>
        )}

        <div className="bg-white shadow rounded-lg p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Create New Todo</h2>
          <form onSubmit={handleCreateTodo} className="flex gap-2">
            <input
              type="text"
              value={newTodoTitle}
              onChange={(e) => setNewTodoTitle(e.target.value)}
              placeholder="Enter todo title..."
              className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              maxLength={500}
              required
            />
            <button
              type="submit"
              disabled={loading || !newTodoTitle.trim()}
              className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Adding...' : 'Add'}
            </button>
          </form>
        </div>

        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Your Todos ({todos.length})
          </h2>

          {todos.length === 0 ? (
            <p className="text-gray-500 text-center py-8">
              No todos yet. Create one above to get started!
            </p>
          ) : (
            <ul className="divide-y divide-gray-200">
              {todos.map((todo) => (
                <li key={todo.id} className="py-4">
                  {editingId === todo.id ? (
                    <div className="flex gap-2">
                      <input
                        type="text"
                        value={editingTitle}
                        onChange={(e) => setEditingTitle(e.target.value)}
                        className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                        maxLength={500}
                      />
                      <button
                        onClick={() => handleUpdateTodo(todo.id)}
                        className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 text-sm"
                      >
                        Save
                      </button>
                      <button
                        onClick={handleCancelEdit}
                        className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400 text-sm"
                      >
                        Cancel
                      </button>
                    </div>
                  ) : (
                    <div className="flex items-center gap-3">
                      <input
                        type="checkbox"
                        checked={todo.is_complete}
                        onChange={() => handleToggleTodo(todo.id)}
                        className="h-5 w-5 text-blue-600 rounded focus:ring-blue-500 cursor-pointer"
                      />
                      <span
                        className={`flex-1 ${
                          todo.is_complete
                            ? 'line-through text-gray-500'
                            : 'text-gray-900'
                        }`}
                      >
                        {todo.title}
                      </span>
                      <button
                        onClick={() => handleStartEdit(todo)}
                        className="px-3 py-1 text-sm text-blue-600 hover:bg-blue-50 rounded-md"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDeleteTodo(todo.id)}
                        className="px-3 py-1 text-sm text-red-600 hover:bg-red-50 rounded-md"
                      >
                        Delete
                      </button>
                    </div>
                  )}
                </li>
              ))}
            </ul>
          )}
        </div>
      </main>
    </div>
  );
}
