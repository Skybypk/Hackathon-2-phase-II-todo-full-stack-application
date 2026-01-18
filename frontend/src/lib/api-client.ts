/**
 * Gets the JWT token from localStorage
 */
export function getAuthToken(): string | null {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('access_token');
  }
  return null;
}

/**
 * Makes an authenticated API call to the backend
 */
export async function apiCall<T>(
  url: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getAuthToken();

  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
    ...options.headers,
  };

  // Determine if we're making a relative call to our backend
  const apiUrl = url.startsWith('http') ? url : `${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'}${url}`;

  const response = await fetch(apiUrl, {
    ...options,
    headers,
  });

  if (!response.ok) {
    throw new Error(`API call failed: ${response.status} ${response.statusText}`);
  }

  return response.json();
}

/**
 * Helper functions for task API calls
 */
export const taskApi = {
  getTasks: () => apiCall('/api/tasks'),
  createTask: (taskData: any) => apiCall('/api/tasks', {
    method: 'POST',
    body: JSON.stringify(taskData),
  }),
  updateTask: (id: string, taskData: any) => apiCall(`/api/tasks/${id}`, {
    method: 'PUT',
    body: JSON.stringify(taskData),
  }),
  deleteTask: (id: string) => apiCall(`/api/tasks/${id}`, {
    method: 'DELETE',
  }),
  toggleTaskCompletion: (id: string, completed: boolean) => apiCall(`/api/tasks/${id}/complete`, {
    method: 'PATCH',
    body: JSON.stringify({ completed }),
  }),
};