import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",       // important for DOM testing
    globals: true,              // allows using describe/test without importing
    setupFiles: "./src/setupTests.js",
  },
});
