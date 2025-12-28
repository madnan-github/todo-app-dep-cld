"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useAuth } from "@/hooks/useAuth";
import { useTasks } from "@/hooks/useTasks";
import { formatDate, getPriorityColor } from "@/lib/utils";
import type { Task } from "@/types";

export default function DashboardPage() {
  const { user, isAuthenticated, isLoading: authLoading, signOut } = useAuth();
  const {
    tasks,
    isLoading: tasksLoading,
    fetchTasks,
    createTask,
    toggleComplete,
    deleteTask,
  } = useTasks();

  const [newTaskTitle, setNewTaskTitle] = useState("");
  const [isCreating, setIsCreating] = useState(false);
  const [filter, setFilter] = useState("all");
  const [search, setSearch] = useState("");

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      window.location.href = "/signin";
    }
  }, [authLoading, isAuthenticated]);

  useEffect(() => {
    if (isAuthenticated) {
      fetchTasks();
    }
  }, [isAuthenticated]);

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTaskTitle.trim()) return;

    setIsCreating(true);
    try {
      await createTask({
        title: newTaskTitle,
        priority: "medium",
      });
      setNewTaskTitle("");
    } finally {
      setIsCreating(false);
    }
  };

  const filteredTasks = tasks.filter((task) => {
    if (filter === "active") return !task.completed;
    if (filter === "completed") return task.completed;
    return true;
  });

  const searchedTasks = search
    ? filteredTasks.filter(
        (task) =>
          task.title.toLowerCase().includes(search.toLowerCase()) ||
          task.description?.toLowerCase().includes(search.toLowerCase())
      )
    : filteredTasks;

  if (authLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 dark:bg-gray-800 dark:border-gray-700">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-600 text-white font-bold">
              T
            </div>
            <span className="text-xl font-bold text-gray-900 dark:text-white">
              TaskFlow
            </span>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-sm text-gray-600 dark:text-gray-400">
              {user?.name || user?.email}
            </span>
            <Button variant="outline" size="sm" onClick={() => signOut()}>
              Sign Out
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        {/* Create Task Form */}
        <Card className="mb-8">
          <CardContent className="pt-6">
            <form onSubmit={handleCreateTask} className="flex gap-4">
              <Input
                placeholder="What needs to be done?"
                value={newTaskTitle}
                onChange={(e) => setNewTaskTitle(e.target.value)}
                className="flex-1"
                disabled={isCreating}
              />
              <Button type="submit" disabled={isCreating || !newTaskTitle.trim()}>
                {isCreating ? "Adding..." : "Add Task"}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Filters */}
        <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex gap-2">
            <Button
              variant={filter === "all" ? "default" : "outline"}
              size="sm"
              onClick={() => setFilter("all")}
            >
              All
            </Button>
            <Button
              variant={filter === "active" ? "default" : "outline"}
              size="sm"
              onClick={() => setFilter("active")}
            >
              Active
            </Button>
            <Button
              variant={filter === "completed" ? "default" : "outline"}
              size="sm"
              onClick={() => setFilter("completed")}
            >
              Completed
            </Button>
          </div>
          <Input
            placeholder="Search tasks..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="sm:w-64"
          />
        </div>

        {/* Task List */}
        {tasksLoading ? (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
        ) : searchedTasks.length === 0 ? (
          <Card>
            <CardContent className="py-12 text-center">
              <p className="text-gray-500 dark:text-gray-400">
                {search
                  ? "No tasks match your search"
                  : filter === "completed"
                  ? "No completed tasks"
                  : "No tasks yet. Create your first task above!"}
              </p>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-3">
            {searchedTasks.map((task) => (
              <TaskItem
                key={task.id}
                task={task}
                onToggleComplete={() => toggleComplete(task.id)}
                onDelete={() => deleteTask(task.id)}
              />
            ))}
          </div>
        )}

        {/* Task Count */}
        <div className="mt-6 text-sm text-gray-500 dark:text-gray-400">
          {tasks.filter((t) => !t.completed).length} tasks remaining
        </div>
      </main>
    </div>
  );
}

function TaskItem({
  task,
  onToggleComplete,
  onDelete,
}: {
  task: Task;
  onToggleComplete: () => void;
  onDelete: () => void;
}) {
  return (
    <Card className={task.completed ? "opacity-60" : ""}>
      <CardContent className="flex items-center gap-4 py-4">
        <input
          type="checkbox"
          checked={task.completed}
          onChange={onToggleComplete}
          className="h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
        />
        <div className="flex-1 min-w-0">
          <p
            className={`font-medium text-gray-900 dark:text-white truncate ${
              task.completed ? "line-through text-gray-500" : ""
            }`}
          >
            {task.title}
          </p>
          {task.description && (
            <p className="text-sm text-gray-500 dark:text-gray-400 truncate">
              {task.description}
            </p>
          )}
          <div className="mt-2 flex items-center gap-2">
            <Badge className={getPriorityColor(task.priority)}>
              {task.priority}
            </Badge>
            <span className="text-xs text-gray-400">
              {formatDate(task.created_at)}
            </span>
          </div>
        </div>
        <Button
          variant="ghost"
          size="sm"
          onClick={onDelete}
          className="text-red-600 hover:text-red-700 hover:bg-red-50"
        >
          <svg
            className="h-4 w-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
            />
          </svg>
        </Button>
      </CardContent>
    </Card>
  );
}
