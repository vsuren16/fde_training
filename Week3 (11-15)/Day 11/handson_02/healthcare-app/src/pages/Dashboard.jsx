import React, { useEffect, useState } from "react";
import InfoCard from "../components/InfoCard";

const Dashboard = () => {
  const [patients, setPatients] = useState([]);
  const [doctors, setDoctors] = useState([]);
  const [appointments, setAppointments] = useState([]);

  useEffect(() => {
    // Demo data (simulate API fetch)
    setPatients([
      { id: 1, name: "Asha" },
      { id: 2, name: "Rahul" },
      { id: 3, name: "Meera" },
    ]);

    setDoctors([
      { id: 1, name: "Dr. Kumar", active: true },
      { id: 2, name: "Dr. Joseph", active: true },
      { id: 3, name: "Dr. Priya", active: false },
    ]);

    setAppointments([
      { id: 101, date: "2026-02-16" },
      { id: 102, date: "2026-02-16" },
      { id: 103, date: "2026-02-17" },
    ]);
  }, []);

  const today = new Date().toISOString().slice(0, 10);

  const totalPatients = patients.length;
  const activeDoctors = doctors.filter(d => d.active).length;
  const todaysAppointments = appointments.filter(a => a.date === today).length;

  return (
    <div>
      <h3 className="mb-4">Dashboard Overview</h3>

      <div className="row">
        <InfoCard
          title="Total Patients"
          value={totalPatients}
          subtitle="Registered Patients"
        />

        <InfoCard
          title="Active Doctors"
          value={activeDoctors}
          subtitle="Currently Available"
        />

        <InfoCard
          title="Today's Appointments"
          value={todaysAppointments}
          subtitle={`Date: ${today}`}
        />
      </div>
    </div>
  );
};

export default Dashboard;
