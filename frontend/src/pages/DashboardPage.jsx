/**
 * DashboardPage — task CRUD with stats, list, and modal form.
 */

import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { getTasks, createTask, updateTask, deleteTask } from '../services/api';

/* ---- Task Modal ---- */

function TaskModal({ task, onClose, onSave }) {
  const isEdit = !!task;
  const [form, setForm] = useState({
    title: task?.title || '',
    description: task?.description || '',
    status: task?.status || 'pending',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  function onChange(e) {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      if (isEdit) {
        await updateTask(task.id, form);
      } else {
        await createTask(form);
      }
      onSave();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <h2 className="modal-title">{isEdit ? 'Edit Task' : 'New Task'}</h2>

        {error && <div className="alert alert-error">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Title</label>
            <input
              className="form-input"
              name="title"
              placeholder="Task title"
              value={form.title}
              onChange={onChange}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Description</label>
            <textarea
              className="form-textarea"
              name="description"
              placeholder="Optional description…"
              value={form.description}
              onChange={onChange}
            />
          </div>

          <div className="form-group">
            <label className="form-label">Status</label>
            <select
              className="form-select"
              name="status"
              value={form.status}
              onChange={onChange}
            >
              <option value="pending">Pending</option>
              <option value="in_progress">In Progress</option>
              <option value="completed">Completed</option>
            </select>
          </div>

          <div className="modal-actions">
            <button type="button" className="btn btn-outline" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? <span className="spinner" /> : isEdit ? 'Update' : 'Create'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

/* ---- Navbar ---- */

function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate('/login');
  }

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        📋 <span>TaskManager</span>
      </div>
      <div className="navbar-actions">
        <span className="navbar-user">{user?.email}</span>
        <span className="navbar-role">{user?.role}</span>
        <button className="btn btn-outline btn-sm" onClick={handleLogout}>
          Logout
        </button>
      </div>
    </nav>
  );
}

/* ---- Main Dashboard ---- */

export default function DashboardPage() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [modal, setModal] = useState({ open: false, task: null });
  const { user } = useAuth();

  const fetchTasks = useCallback(async () => {
    setLoading(true);
    try {
      const data = await getTasks();
      setTasks(data);
    } catch {
      // Token might be expired
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  async function handleDelete(id) {
    if (!confirm('Delete this task?')) return;
    try {
      await deleteTask(id);
      fetchTasks();
    } catch {
      // ignore
    }
  }

  function openCreate() {
    setModal({ open: true, task: null });
  }

  function openEdit(task) {
    setModal({ open: true, task });
  }

  function closeModal() {
    setModal({ open: false, task: null });
  }

  function handleSaved() {
    closeModal();
    fetchTasks();
  }

  // Stats
  const stats = {
    total: tasks.length,
    pending: tasks.filter((t) => t.status === 'pending').length,
    in_progress: tasks.filter((t) => t.status === 'in_progress').length,
    completed: tasks.filter((t) => t.status === 'completed').length,
  };

  return (
    <div className="app-container">
      <Navbar />

      <main className="main-content fade-in">
        {/* Header */}
        <div className="dashboard-header">
          <h1 className="dashboard-title">
            {user?.role === 'admin' ? 'All Tasks (Admin)' : 'My Tasks'}
          </h1>
          <button id="create-task-btn" className="btn btn-primary" onClick={openCreate}>
            + New Task
          </button>
        </div>

        {/* Stats */}
        <div className="stats-row">
          <div className="stat-card stat-total">
            <div className="stat-value">{stats.total}</div>
            <div className="stat-label">Total</div>
          </div>
          <div className="stat-card stat-pending">
            <div className="stat-value">{stats.pending}</div>
            <div className="stat-label">Pending</div>
          </div>
          <div className="stat-card stat-progress">
            <div className="stat-value">{stats.in_progress}</div>
            <div className="stat-label">In Progress</div>
          </div>
          <div className="stat-card stat-done">
            <div className="stat-value">{stats.completed}</div>
            <div className="stat-label">Completed</div>
          </div>
        </div>

        {/* Task list */}
        {loading ? (
          <div className="empty-state">
            <div className="spinner" style={{ width: 36, height: 36 }} />
          </div>
        ) : tasks.length === 0 ? (
          <div className="empty-state">
            <div className="empty-state-icon">📭</div>
            <div className="empty-state-text">No tasks yet</div>
            <div className="empty-state-sub">Click "+ New Task" to get started</div>
          </div>
        ) : (
          <div className="task-list">
            {tasks.map((task) => (
              <div className="card task-card" key={task.id}>
                <div className="task-info">
                  <div className="task-title">{task.title}</div>
                  {task.description && (
                    <div className="task-desc">{task.description}</div>
                  )}
                </div>
                <span className={`badge badge-${task.status}`}>
                  {task.status.replace('_', ' ')}
                </span>
                <div className="task-actions">
                  <button
                    className="btn btn-outline btn-sm"
                    onClick={() => openEdit(task)}
                  >
                    Edit
                  </button>
                  <button
                    className="btn btn-ghost btn-sm"
                    onClick={() => handleDelete(task.id)}
                  >
                    ✕
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>

      {/* Modal */}
      {modal.open && (
        <TaskModal
          task={modal.task}
          onClose={closeModal}
          onSave={handleSaved}
        />
      )}
    </div>
  );
}
