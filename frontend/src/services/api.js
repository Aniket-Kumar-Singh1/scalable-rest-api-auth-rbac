/**
 * API service — handles all HTTP requests to the backend.
 */

const BASE = '/api/v1';

async function request(url, options = {}) {
  const token = localStorage.getItem('token');

  const headers = {
    'Content-Type': 'application/json',
    ...(token && { Authorization: `Bearer ${token}` }),
    ...options.headers,
  };

  const res = await fetch(`${BASE}${url}`, { ...options, headers });

  // Try parsing JSON (may be empty on 204 etc.)
  let data;
  try {
    data = await res.json();
  } catch {
    data = null;
  }

  if (!res.ok) {
    const message = data?.detail || `Request failed (${res.status})`;
    throw new Error(message);
  }

  return data;
}

/* ---- Auth ---- */

export async function registerUser(payload) {
  return request('/auth/register', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function loginUser(email, password) {
  // Use form-encoded body for OAuth2PasswordRequestForm compatibility
  const body = new URLSearchParams({ username: email, password });
  const res = await fetch(`${BASE}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body,
  });

  const data = await res.json();
  if (!res.ok) throw new Error(data?.detail || 'Login failed');
  return data;
}

/* ---- Tasks ---- */

export async function getTasks() {
  return request('/tasks/');
}

export async function getTask(id) {
  return request(`/tasks/${id}`);
}

export async function createTask(payload) {
  return request('/tasks/', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function updateTask(id, payload) {
  return request(`/tasks/${id}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  });
}

export async function deleteTask(id) {
  return request(`/tasks/${id}`, { method: 'DELETE' });
}
