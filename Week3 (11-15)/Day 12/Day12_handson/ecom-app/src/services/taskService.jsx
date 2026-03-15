import axios from "axios";

const api = axios.create({
  baseURL: "https://jsonplaceholder.typicode.com",
  timeout: 10000,
});

export async function getTasks(signal) {
  // Axios supports AbortController via `signal`
  const response = await api.get("/todos", { signal });
  return response.data;
}
