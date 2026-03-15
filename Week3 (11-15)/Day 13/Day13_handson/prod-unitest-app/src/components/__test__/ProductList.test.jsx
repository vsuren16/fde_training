import { describe, test, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import ProductList from "../ProductList";
import axios from "axios";

vi.mock("axios");

describe("ProductList", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  test("1) API call is triggered on component load", async () => {
    axios.get.mockResolvedValueOnce({ data: [] });

    render(<ProductList />);

    expect(axios.get).toHaveBeenCalledTimes(1);
    expect(axios.get).toHaveBeenCalledWith("/products");

    await waitFor(() => {
      expect(screen.queryByRole("status")).not.toBeInTheDocument();
    });
  });

  test("2) Loading message is shown while data is fetched", () => {
    axios.get.mockReturnValueOnce(new Promise(() => {}));

    render(<ProductList />);

    expect(screen.getByRole("status")).toHaveTextContent("Loading...");
  });

  test("3) Product list is rendered after successful API response", async () => {
    axios.get.mockResolvedValueOnce({
      data: [
        { id: 1, name: "iPhone", price: 999, category: "Electronics" },
        { id: 2, name: "Shoes", price: 49.5, category: "Fashion" },
      ],
    });

    render(<ProductList />);

    expect(await screen.findByText("Products")).toBeInTheDocument();

    expect(screen.getByText("iPhone")).toBeInTheDocument();
    expect(screen.getByText("$999.00")).toBeInTheDocument();
    expect(screen.getByText("Electronics")).toBeInTheDocument();

    expect(screen.getByText("Shoes")).toBeInTheDocument();
    expect(screen.getByText("$49.50")).toBeInTheDocument();
    expect(screen.getByText("Fashion")).toBeInTheDocument();
  });

  test("4) Error message is displayed when API fails", async () => {
    axios.get.mockRejectedValueOnce(new Error("Network error"));

    render(<ProductList />);

    const alert = await screen.findByRole("alert");
    expect(alert).toHaveTextContent("Failed to load products.");
  });

  test("5) Empty product list message is shown when no data exists", async () => {
    axios.get.mockResolvedValueOnce({ data: [] });

    render(<ProductList />);

    expect(await screen.findByText("No products found.")).toBeInTheDocument();
  });
});
