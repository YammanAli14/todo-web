"use client";

import { useState, useEffect, useCallback } from "react";
import { api } from "@/lib/api";
import { TaskItem } from "./TaskItem";
import { TaskForm } from "./TaskForm";
import type { Task } from "@/types";

export function TaskList() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  const loadTasks = useCallback(async () => {
    try {
      const data = await api.getTasks();
      setTasks(data);
      setError("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load tasks");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadTasks();
  }, [loadTasks]);

  const handleCreate = async (title: string) => {
    const newTask = await api.createTask({ title });
    setTasks((prev) => [...prev, newTask]);
  };

  const handleToggle = async (id: number) => {
    const updated = await api.toggleTask(id);
    setTasks((prev) =>
      prev.map((t) => (t.id === id ? updated : t))
    );
  };

  const handleUpdate = async (id: number, title: string) => {
    const updated = await api.updateTask(id, { title });
    setTasks((prev) =>
      prev.map((t) => (t.id === id ? updated : t))
    );
  };

  const handleDelete = async (id: number) => {
    await api.deleteTask(id);
    setTasks((prev) => prev.filter((t) => t.id !== id));
  };

  if (isLoading) {
    return (
      <div className="text-center py-8 text-gray-600">Loading tasks...</div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <p className="text-red-600 mb-4">{error}</p>
        <button
          onClick={loadTasks}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Retry
        </button>
      </div>
    );
  }

  const completedCount = tasks.filter((t) => t.is_complete).length;
  const totalCount = tasks.length;

  return (
    <div>
      <TaskForm onSubmit={handleCreate} />

      {totalCount > 0 && (
        <div className="mb-4 text-sm text-gray-600">
          {completedCount} of {totalCount} tasks completed
        </div>
      )}

      {tasks.length === 0 ? (
        <div className="text-center py-12 text-gray-500">
          <p className="text-lg">No tasks yet</p>
          <p className="text-sm mt-2">Add a task above to get started</p>
        </div>
      ) : (
        <ul className="space-y-3">
          {tasks.map((task) => (
            <TaskItem
              key={task.id}
              task={task}
              onToggle={handleToggle}
              onUpdate={handleUpdate}
              onDelete={handleDelete}
            />
          ))}
        </ul>
      )}
    </div>
  );
}
