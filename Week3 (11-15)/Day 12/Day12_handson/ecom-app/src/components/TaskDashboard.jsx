import { useEffect, useState } from "react";
import { getTasks } from "../services/taskservice";
import "./TaskDashboard.css";

export default function TaskDashboard() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const controller = new AbortController();

    async function fetchTasks() {
      try {
        setLoading(true);
        setError("");

        const data = await getTasks(controller.signal);
        setTasks(Array.isArray(data) ? data : []);
      } catch (err) {
        // Ignore abort errors
        if (err?.name !== "CanceledError" && err?.name !== "AbortError") {
          setError(err?.message || "Failed to fetch tasks.");
        }
      } finally {
        setLoading(false);
      }
    }

    fetchTasks();

    // Fetch only once on mount, cleanup on unmount
    return () => controller.abort();
  }, []);

  return (
    <div className="tm-page">
      <header className="tm-header">
        <h1>Task Management Dashboard</h1>
        <p className="tm-sub">Tasks from JSONPlaceholder (/todos)</p>
      </header>

      {loading && <div className="tm-status">Loading tasks…</div>}

      {!loading && error && (
        <div className="tm-status tm-error">
          <strong>Error:</strong> {error}
        </div>
      )}

      {!loading && !error && (
        <div className="tm-card">
          <table className="tm-table">
            <thead>
              <tr>
                <th style={{ width: "90px" }}>User ID</th>
                <th>Task Title</th>
                <th style={{ width: "140px" }}>Status</th>
              </tr>
            </thead>
            <tbody>
              {tasks.map((t) => {
                const statusLabel = t.completed ? "Completed" : "Pending";
                return (
                  <tr key={t.id}>
                    <td>{t.userId}</td>
                    <td className="tm-title">{t.title}</td>
                    <td>
                      <span
                        className={`tm-badge ${
                          t.completed ? "tm-badge--done" : "tm-badge--pending"
                        }`}
                      >
                        {statusLabel}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>

          {tasks.length === 0 && (
            <div className="tm-empty">No tasks found.</div>
          )}
        </div>
      )}
    </div>
  );
}
