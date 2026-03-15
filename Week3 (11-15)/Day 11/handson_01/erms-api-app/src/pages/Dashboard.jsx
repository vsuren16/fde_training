import React, { useEffect, useState } from "react";
import StatCard from "../components/StatCard";

const Dashboard = ({ employees, departments, projects }) => {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    totalEmployees: 0,
    totalDepartments: 0,
    activeProjects: 0,
  });

  useEffect(() => {
    // simulate API call
    setLoading(true);

    const timer = setTimeout(() => {
      const activeProjectsCount = projects.filter((p) => p.isActive).length;

      setStats({
        totalEmployees: employees.length,
        totalDepartments: departments.length,
        activeProjects: activeProjectsCount,
      });

      setLoading(false);
    }, 800);

    return () => clearTimeout(timer);
  }, [employees, departments, projects]);

  return (
    <div>
      <h2 className="mb-4">Dashboard</h2>

      {loading ? (
        <div className="alert alert-info">Loading dashboard data...</div>
      ) : (
        <div className="row g-3">
          <div className="col-12 col-md-4">
            <StatCard title="Total Employees" value={stats.totalEmployees} />
          </div>
          <div className="col-12 col-md-4">
            <StatCard title="Total Departments" value={stats.totalDepartments} />
          </div>
          <div className="col-12 col-md-4">
            <StatCard title="Active Projects" value={stats.activeProjects} />
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
