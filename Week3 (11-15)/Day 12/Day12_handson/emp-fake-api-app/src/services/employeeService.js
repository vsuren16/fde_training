import axios from "axios";

const API_URL = "https://jsonplaceholder.typicode.com/users";

export const getEmployees = async () => {
  const res = await axios.get(API_URL);

  // Normalize to only required fields
  return res.data.map((u) => ({
    id: u.id,
    name: u.name,
    email: u.email,
    phone: u.phone,
    companyName: u.company?.name || "N/A",
  }));
};
