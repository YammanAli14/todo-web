"use client";

import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { TaskList } from "@/components/tasks/TaskList";
import { useAuth } from "@/components/auth/AuthProvider";

export default function TasksPage() {
  const { user } = useAuth();

  return (
    <ProtectedRoute>
      <div className="max-w-2xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">My Tasks</h1>
          {user && (
            <p className="text-gray-600 mt-1">Logged in as {user.email}</p>
          )}
        </div>
        <TaskList />
      </div>
    </ProtectedRoute>
  );
}
