import React, { createContext, useMemo, useState } from "react";

export const DataContext = createContext();

const seedPatients = [
  { id: 1, name: "Asha", age: 29 },
  { id: 2, name: "Rahul", age: 41 },
  { id: 3, name: "Meera", age: 35 },
];

const seedRecords = [
  { id: 501, patientId: 1, date: "2026-02-10", diagnosis: "Viral Fever", notes: "Rest + fluids", doctor: "Dr. Kumar" },
  { id: 502, patientId: 1, date: "2026-02-16", diagnosis: "Follow-up", notes: "Improving", doctor: "Dr. Kumar" },
  { id: 503, patientId: 2, date: "2026-02-12", diagnosis: "BP Check", notes: "Monitor weekly", doctor: "Dr. Joseph" },
];

const DataProvider = ({ children }) => {
  const [patients] = useState(seedPatients);
  const [records, setRecords] = useState(seedRecords);

  const addRecord = (newRecord) => {
    setRecords((prev) => [newRecord, ...prev]);
  };

  const value = useMemo(
    () => ({ patients, records, addRecord }),
    [patients, records]
  );

  return <DataContext.Provider value={value}>{children}</DataContext.Provider>;
};

export default DataProvider;
