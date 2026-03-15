export const ROLE = {
  ADMIN: "Admin",
  DOCTOR: "Doctor",
  RECEPTIONIST: "Receptionist",
};

export const ROLE_ACCESS = {
  [ROLE.ADMIN]: {
    routes: ["/dashboard", "/patients", "/patients/:id", "/doctors", "/appointments", "/records/:patientId", "/profile"],
    nav: ["Dashboard", "Patients", "Doctors", "Appointments", "Records", "Profile"],
  },
  [ROLE.DOCTOR]: {
    routes: ["/dashboard", "/patients", "/patients/:id", "/records/:patientId", "/profile"],
    nav: ["Dashboard", "Patients", "Records", "Profile"],
  },
  [ROLE.RECEPTIONIST]: {
    routes: ["/dashboard", "/appointments", "/profile"],
    nav: ["Dashboard", "Appointments", "Profile"],
  },
};
