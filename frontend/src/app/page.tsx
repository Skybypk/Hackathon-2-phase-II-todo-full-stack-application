'use client';

import React, { useState, useEffect } from 'react';
import { authClient } from '../lib/auth-client';

export default function Home() {
  const [user, setUser] = useState<any>(null);
  const [tasks, setTasks] = useState<any[]>([]);
  const [newTask, setNewTask] = useState({ title: '', description: '' });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in using both authClient and localStorage token
    const checkAuthStatus = async () => {
      try {
        // First try with authClient
        const session = await authClient.getSession();
        if (session.data?.session) {
          setUser(session.data.user);
          fetchTasks();
        } else {
          // Check if we have a token in localStorage (fallback)
          const token = localStorage.getItem('access_token');
          if (token) {
            // Try to get user info using the token
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/auth/me`, {
              headers: {
                'Authorization': `Bearer ${token}`,
              },
            });

            if (response.ok) {
              const userData = await response.json();
              setUser(userData);
              fetchTasks();
            } else {
              // Token is invalid/expired
              localStorage.removeItem('access_token');
              setLoading(false);
            }
          } else {
            setLoading(false);
          }
        }
      } catch (error) {
        console.error('Error checking auth status:', error);
        setLoading(false);
      }
    };

    checkAuthStatus();
  }, []);

  const fetchTasks = async () => {
    try {
      const token = await getAuthToken();
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/tasks`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setTasks(data);
      }
    } catch (error) {
      console.error('Error fetching tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  const getAuthToken = async () => {
    // First try to get token from authClient
    const session = await authClient.getSession();
    if (session.data?.session?.token) {
      return session.data.session.token;
    }

    // Fallback to localStorage token
    return localStorage.getItem('access_token') || '';
  };

  const handleLogin = async () => {
    // Redirect to login page
    window.location.href = '/login';
  };

  const handleLogout = async () => {
    await authClient.signOut();
    // Also clear the localStorage token
    localStorage.removeItem('access_token');
    setUser(null);
    window.location.reload();
  };

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const token = await getAuthToken();
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/tasks`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(newTask),
      });

      if (response.ok) {
        const createdTask = await response.json();
        setTasks([createdTask, ...tasks]);
        setNewTask({ title: '', description: '' });
      }
    } catch (error) {
      console.error('Error creating task:', error);
    }
  };

  const handleToggleComplete = async (taskId: string, completed: boolean) => {
    try {
      const token = await getAuthToken();
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/tasks/${taskId}/complete`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ completed: !completed }),
      });

      if (response.ok) {
        const updatedTask = await response.json();
        setTasks(tasks.map(task =>
          task.id === taskId ? updatedTask : task
        ));
      }
    } catch (error) {
      console.error('Error toggling task completion:', error);
    }
  };

  const [editingTaskId, setEditingTaskId] = useState<string | null>(null);
  const [editingTaskData, setEditingTaskData] = useState({ title: '', description: '' });

  const startEditingTask = (task: any) => {
    setEditingTaskId(task.id);
    setEditingTaskData({ title: task.title, description: task.description || '' });
  };

  const cancelEditingTask = () => {
    setEditingTaskId(null);
    setEditingTaskData({ title: '', description: '' });
  };

  const saveEditedTask = async (taskId: string) => {
    try {
      const token = await getAuthToken();
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/tasks/${taskId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(editingTaskData),
      });

      if (response.ok) {
        const updatedTask = await response.json();
        setTasks(tasks.map(task =>
          task.id === taskId ? updatedTask : task
        ));
        setEditingTaskId(null);
        setEditingTaskData({ title: '', description: '' });
      }
    } catch (error) {
      console.error('Error saving edited task:', error);
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    try {
      const token = await getAuthToken();
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/tasks/${taskId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        setTasks(tasks.filter(task => task.id !== taskId));
      }
    } catch (error) {
      console.error('Error deleting task:', error);
    }
  };

  if (loading) {
    return <div className="flex justify-center items-center h-screen">Loading...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">Todo App</h1>
          {user ? (
            <div className="flex items-center space-x-4">
              <span className="text-gray-700">Welcome, {user.email}</span>
              <button
                onClick={handleLogout}
                className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-md"
              >
                Logout
              </button>
            </div>
          ) : (
            <button
              onClick={handleLogin}
              className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-md"
            >
              Login
            </button>
          )}
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        {!user ? (
          <div className="text-center py-12">
            <h2 className="text-xl text-gray-700 mb-4">Please log in to access your tasks</h2>
            <button
              onClick={handleLogin}
              className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-md"
            >
              Login
            </button>
          </div>
        ) : (
          <>
            <form onSubmit={handleCreateTask} className="mb-8 bg-white p-6 rounded-lg shadow">
              <h2 className="text-xl font-semibold mb-4">Create New Task</h2>
              <div className="grid grid-cols-1 gap-y-4">
                <input
                  type="text"
                  value={newTask.title}
                  onChange={(e) => setNewTask({...newTask, title: e.target.value})}
                  placeholder="Task title"
                  className="border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
                <textarea
                  value={newTask.description}
                  onChange={(e) => setNewTask({...newTask, description: e.target.value})}
                  placeholder="Task description (optional)"
                  className="border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  rows={3}
                />
                <button
                  type="submit"
                  className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-md w-full sm:w-auto sm:inline-block"
                >
                  Add Task
                </button>
              </div>
            </form>

            <div>
              <h2 className="text-xl font-semibold mb-4">Your Tasks</h2>
              {tasks.length === 0 ? (
                <p className="text-gray-500">No tasks yet. Create your first task!</p>
              ) : (
                <ul className="space-y-4">
                  {tasks.map((task) => (
                    <li
                      key={task.id}
                      className={`bg-white p-4 rounded-lg shadow ${
                        task.completed ? 'opacity-75' : ''
                      }`}
                    >
                      {editingTaskId === task.id ? (
                        // Edit mode
                        <div>
                          <input
                            type="text"
                            value={editingTaskData.title}
                            onChange={(e) => setEditingTaskData({...editingTaskData, title: e.target.value})}
                            className="w-full border border-gray-300 rounded-md px-3 py-2 mb-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="Task title"
                          />
                          <textarea
                            value={editingTaskData.description}
                            onChange={(e) => setEditingTaskData({...editingTaskData, description: e.target.value})}
                            className="w-full border border-gray-300 rounded-md px-3 py-2 mb-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="Task description (optional)"
                            rows={2}
                          />
                          <div className="flex space-x-2 mt-2">
                            <button
                              onClick={() => saveEditedTask(task.id)}
                              className="bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded-md text-sm"
                            >
                              Save
                            </button>
                            <button
                              onClick={cancelEditingTask}
                              className="bg-gray-500 hover:bg-gray-600 text-white px-3 py-1 rounded-md text-sm"
                            >
                              Cancel
                            </button>
                          </div>
                        </div>
                      ) : (
                        // View mode
                        <div className="flex justify-between items-start">
                          <div>
                            <h3 className={`font-medium ${task.completed ? 'line-through' : ''}`}>
                              {task.title}
                            </h3>
                            {task.description && (
                              <p className="text-gray-600 mt-1">{task.description}</p>
                            )}
                            <p className="text-sm text-gray-500 mt-2">
                              {new Date(task.created_at).toLocaleString()}
                              {task.completed && task.completed_at && (
                                <span> • Completed: {new Date(task.completed_at).toLocaleString()}</span>
                              )}
                            </p>
                          </div>
                          <div className="flex space-x-2">
                            <button
                              onClick={() => startEditingTask(task)}
                              className="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded-md text-sm"
                            >
                              Edit
                            </button>
                            <button
                              onClick={() => handleToggleComplete(task.id, task.completed)}
                              className={`${
                                task.completed
                                  ? 'bg-yellow-500 hover:bg-yellow-600'
                                  : 'bg-blue-500 hover:bg-blue-600'
                              } text-white px-3 py-1 rounded-md text-sm`}
                            >
                              {task.completed ? 'Undo' : 'Complete'}
                            </button>
                            <button
                              onClick={() => handleDeleteTask(task.id)}
                              className="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded-md text-sm"
                            >
                              Delete
                            </button>
                          </div>
                        </div>
                      )}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </>
        )}
      </main>
    </div>
  );
}