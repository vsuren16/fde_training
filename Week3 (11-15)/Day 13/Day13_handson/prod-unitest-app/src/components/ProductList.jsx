import { useEffect, useState } from "react";
import axios from "axios";

export default function ProductList() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let isMounted = true;

    async function fetchProducts() {
      try {
        setLoading(true);
        setError("");

        const res = await axios.get("/products"); // FastAPI: GET /products
        const data = Array.isArray(res.data) ? res.data : [];

        if (isMounted) setProducts(data);
      } catch (e) {
        if (isMounted) setError("Failed to load products.");
      } finally {
        if (isMounted) setLoading(false);
      }
    }

    fetchProducts();

    return () => {
      isMounted = false;
    };
  }, []);

  if (loading) return <div role="status">Loading...</div>;
  if (error) return <div role="alert">{error}</div>;

  if (!products.length) return <div>No products found.</div>;

  return (
    <div>
      <h1>Products</h1>
      <ul aria-label="product-list">
        {products.map((p) => (
          <li key={p.id ?? `${p.name}-${p.price}`}>
            <span>{p.name}</span>{" "}
            <span>${Number(p.price).toFixed(2)}</span>{" "}
            <span>{p.category}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
