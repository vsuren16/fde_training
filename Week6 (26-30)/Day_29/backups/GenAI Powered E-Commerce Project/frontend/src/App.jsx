import { useEffect, useMemo, useState } from "react";

const API_BASE = "/api";

const FALLBACK_IMAGE =
  "data:image/svg+xml;utf8," +
  encodeURIComponent(`
  <svg xmlns='http://www.w3.org/2000/svg' width='600' height='600'>
    <rect width='100%' height='100%' fill='#f1f5f9'/>
    <text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle'
      fill='#64748b' font-family='Arial' font-size='22'>
      No Image
    </text>
  </svg>
`);

function sanitizeUrl(u) {
  if (u == null) return null;
  let s = String(u).trim();

  // remove wrapping quotes: "https://..." or ""https://...""
  // repeat trimming quotes until clean
  while (s.startsWith('"') && s.endsWith('"') && s.length > 2) {
    s = s.slice(1, -1).trim();
  }

  // also handle weird double quotes at start/end
  s = s.replace(/^"+/, "").replace(/"+$/, "").trim();

  return s || null;
}


function uniq(arr) {
  const out = [];
  const seen = new Set();
  for (const x of arr) {
    const s = sanitizeUrl(x);
    if (!s) continue;
    if (!seen.has(s)) {
      seen.add(s);
      out.push(s);
    }
  }
  return out;
}

function pick(obj, keys) {
  for (const k of keys) {
    const v = obj?.[k];
    if (v !== undefined && v !== null && v !== "") return v;
  }
  return undefined;
}

function toNumberPrice(priceRaw) {
  if (typeof priceRaw === "number") return priceRaw;

  if (typeof priceRaw === "string") {
    const cleaned = priceRaw.replace(/[^0-9.]/g, "");
    return cleaned ? Number(cleaned) : null;
  }

  // priceRaw can be an object (Mongo: { final_price, currency, ... })
  if (priceRaw && typeof priceRaw === "object") {
    const candidate =
      priceRaw.final_price ?? // ✅ your Mongo key
      priceRaw.value ??
      priceRaw.amount ??
      priceRaw.price ??
      priceRaw.current ??
      priceRaw.min ??
      priceRaw.max ??
      (priceRaw.price?.value ?? null) ??
      (priceRaw.current?.value ?? null) ??
      null;

    if (typeof candidate === "number") return candidate;

    if (candidate !== null && candidate !== undefined) {
      const cleaned = String(candidate).replace(/[^0-9.]/g, "");
      return cleaned ? Number(cleaned) : null;
    }
  }

  return null;
}

function normalizeProduct(p) {
  // IDs in your project could be product_id or _id; keep both options
  const id = pick(p, ["product_id", "_id", "id", "asin", "sku", "itemId"]);

  // Title/name in your Mongo looks like product_name typically (adjust if needed)
  const title =
    pick(p, [
      "product_name",
      "name",
      "title",
      "product_title",
      "item_name",
      "productName",
      "short_title",
    ]) ?? "Untitled product";

  const brand = pick(p, ["brand", "brand_name", "manufacturer", "brandName"]);

  const rating = Number(
    pick(p, ["rating", "avg_rating", "average_rating", "stars"]) ?? 0
  );

  // ✅ PRICE: parse Mongo object
  const priceNum = toNumberPrice(p?.price ?? pick(p, ["final_price", "sale_price", "current_price"]));

  // Build gallery images (main_image + images[])
  const gallery = uniq([
    p?.main_image,
    ...(Array.isArray(p?.images) ? p.images : []),
  ]);

  const images = gallery.length ? gallery : [FALLBACK_IMAGE];

  // ✅ IMAGE: USE MONGO FIELDS
  // Mongo fields you showed:
  // - main_image: "https://..."
  // - images: ["https://...", ...]
// ✅ IMAGE: USE MONGO FIELDS (main_image first, then images[0])
  let image = pick(p, [
    "main_image",
    "image_url",
    "imageUrl",
    "image",
    "thumbnail",
    "thumbnailUrl",
  ]);

  if (!image && Array.isArray(p?.images) && p.images.length) image = p.images[0];

  // If image is object like {url:"..."} (rare)
  if (image && typeof image === "object") {
    image = image.url ?? image.src ?? image.href ?? image.link ?? null;
  }

  // ✅ sanitize quotes/whitespace from Mongo
  image = sanitizeUrl(image);

  if (!window.__img_once) {
  window.__img_once = true;
  console.log("RAW main_image:", p?.main_image);
  console.log("RAW images[0]:", Array.isArray(p?.images) ? p.images[0] : null);
  console.log("SANITIZED image:", image);
  }

  // Only accept real URLs; otherwise fallback
  if (
    typeof image !== "string" ||
    !(image.startsWith("http://") || image.startsWith("https://"))
  ) {
    image = FALLBACK_IMAGE;
  }

  const deliveryEligible = Boolean(
    pick(p, [
      "delivery_eligible",
      "deliveryAvailable",
      "is_deliverable",
      "shipping_available",
      "deliveryAvailableFlag",
      "isShippingAvailable",
    ])
  );

  return {
    ...p,
    __ui: {
    id,
    title,
    brand,
    rating,
    priceNum,
    image,      // main
    images,     // gallery list ✅
    deliveryEligible,
  },
  };
}

function cx(...s) {
  return s.filter(Boolean).join(" ");
}

function StarRating({ value = 0 }) {
  const v = Math.max(0, Math.min(5, Number(value) || 0));
  const full = Math.floor(v);
  return (
    <div className="flex items-center gap-1">
      <div className="flex">
        {Array.from({ length: 5 }).map((_, i) => {
          const filled = i < full;
          return (
            <span
              key={i}
              className={cx("text-sm", filled ? "text-amber-500" : "text-slate-300")}
            >
              ★
            </span>
          );
        })}
      </div>
      <span className="text-xs text-slate-500">{v.toFixed(1)}</span>
    </div>
  );
}

function Header({ query, setQuery, onSearch }) {
  return (
    <header className="sticky top-0 z-40 border-b bg-white/90 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center gap-4 px-4 py-3">
        <div className="flex items-center gap-2">
          <div className="grid h-9 w-9 place-items-center rounded-xl bg-slate-900 font-bold text-white">
            G
          </div>
          <div className="leading-tight">
            <div className="font-semibold">GenAI Store</div>
            <div className="text-xs text-slate-500">Search • Insights • Chat</div>
          </div>
        </div>

        <form
          className="flex flex-1 items-center gap-2"
          onSubmit={(e) => {
            e.preventDefault();
            onSearch();
          }}
        >
          <div className="relative w-full">
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search products (e.g., running shoes, protein bar, yoga pants)…"
              className="w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-2.5 pr-24 text-sm outline-none focus:border-slate-300 focus:ring-4 focus:ring-slate-100"
            />
            <button
              type="submit"
              className="absolute right-2 top-1/2 -translate-y-1/2 rounded-lg bg-white px-3 py-1.5 text-sm font-medium text-slate-700 hover:bg-slate-100"
            >
              Search
            </button>
          </div>
        </form>

        <div className="hidden items-center gap-2 md:flex">
          <button className="rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm hover:bg-slate-50">
            Orders
          </button>
          <button className="rounded-xl bg-slate-900 px-3 py-2 text-sm text-white hover:bg-slate-800">
            Sign in
          </button>
        </div>
      </div>
    </header>
  );
}

function Filters({ filters, setFilters }) {
  const set = (k, v) => setFilters((p) => ({ ...p, [k]: v }));

  return (
    <aside className="hidden w-72 shrink-0 lg:block">
      <div className="rounded-2xl border bg-white p-4 shadow-soft">
        <div className="flex items-center justify-between">
          <h3 className="font-semibold">Filters</h3>
          <button
            onClick={() =>
              setFilters({ minPrice: "", maxPrice: "", minRating: 0, deliveryOnly: false })
            }
            className="text-xs text-slate-500 hover:text-slate-700"
          >
            Reset
          </button>
        </div>

        <div className="mt-4 space-y-4">
          <div>
            <div className="text-sm font-medium">Price</div>
            <div className="mt-2 grid grid-cols-2 gap-2">
              <input
                value={filters.minPrice}
                onChange={(e) => set("minPrice", e.target.value)}
                placeholder="Min"
                className="rounded-xl border bg-slate-50 px-3 py-2 text-sm outline-none focus:ring-4 focus:ring-slate-100"
              />
              <input
                value={filters.maxPrice}
                onChange={(e) => set("maxPrice", e.target.value)}
                placeholder="Max"
                className="rounded-xl border bg-slate-50 px-3 py-2 text-sm outline-none focus:ring-4 focus:ring-slate-100"
              />
            </div>
          </div>

          <div>
            <div className="text-sm font-medium">Rating</div>
            <input
              type="range"
              min="0"
              max="5"
              step="0.5"
              value={filters.minRating}
              onChange={(e) => set("minRating", Number(e.target.value))}
              className="mt-2 w-full"
            />
            <div className="text-xs text-slate-500">Min: {filters.minRating}</div>
          </div>

          <label className="flex items-center gap-2 text-sm">
            <input
              type="checkbox"
              checked={filters.deliveryOnly}
              onChange={(e) => set("deliveryOnly", e.target.checked)}
            />
            Delivery available
          </label>
        </div>
      </div>
    </aside>
  );
}

function ProductCard({ p, onSelect }) {
  const ui = p.__ui ?? {};
  const title = ui.title ?? "Untitled product";
  const brand = ui.brand ?? "";
  const rating = ui.rating ?? 0;
  const image = ui.image ?? FALLBACK_IMAGE;
  const priceNum = ui.priceNum;

  return (
    <button
      onClick={() => onSelect(p)}
      className="group rounded-2xl border bg-white p-3 text-left shadow-soft transition hover:-translate-y-0.5 hover:shadow-md"
    >
      <div className="aspect-square overflow-hidden rounded-xl bg-slate-100">
        <img
          src={image}
          alt={title}
          className="h-full w-full object-cover transition group-hover:scale-[1.03]"
          loading="lazy"
          onError={(e) => {
            e.currentTarget.src = FALLBACK_IMAGE;
          }}
        />
      </div>

      <div className="mt-3 space-y-1">
        <div className="line-clamp-2 text-sm font-medium">{title}</div>
        <div className="text-xs text-slate-700">{brand}</div>

        <div className="flex items-center justify-between pt-1">
          <div className="text-base font-semibold text-slate-900">
            {typeof priceNum === "number" && !Number.isNaN(priceNum) ? (
              `$${priceNum.toFixed(2)}`
            ) : (
              <span className="text-slate-500">Price unavailable</span>
            )}
          </div>
          <StarRating value={rating} />
        </div>

        <div className="flex gap-2 pt-2">
          {ui.deliveryEligible && (
            <span className="rounded-full bg-emerald-50 px-2 py-1 text-xs font-medium text-emerald-700">
              Delivery
            </span>
          )}
        </div>
      </div>
    </button>
  );
}

function ProductGrid({ items, onSelect, loading }) {
  if (loading) {
    return (
      <div className="grid grid-cols-2 gap-4 md:grid-cols-3 xl:grid-cols-4">
        {Array.from({ length: 8 }).map((_, i) => (
          <div key={i} className="h-72 animate-pulse rounded-2xl border bg-white" />
        ))}
      </div>
    );
  }

  if (!items?.length) {
    return (
      <div className="rounded-2xl border bg-white p-8 text-center text-sm text-slate-600 shadow-soft">
        No results. Try a broader query (e.g., “running shoes”, “protein bar”).
      </div>
    );
  }

  return (
    <div className="grid grid-cols-2 gap-4 md:grid-cols-3 xl:grid-cols-4">
      {items.map((p) => (
        <ProductCard key={p?.__ui?.id ?? p?._id ?? p?.id ?? Math.random()} p={p} onSelect={onSelect} />
      ))}
    </div>
  );
}

function DetailDrawer({ product, onClose, onAskChat }) {
  const open = !!product;
  if (!open) return null;

  const ui = product?.__ui ?? {};

  const title = ui.title ?? "Product";
  const priceNum = ui.priceNum;
  const rating = ui.rating ?? 0;
  const brand = ui.brand ?? "";
  const productId = ui.id ?? null;

  const desc =
    product?.description ??
    product?.short_description ??
    product?.long_description ??
    "";

  const gallery = ui.images?.length ? ui.images : [ui.image ?? FALLBACK_IMAGE];

  const [activeImg, setActiveImg] = useState(gallery[0]);

  useEffect(() => {
    setActiveImg(gallery[0]);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [productId]); // reset when new product selected

  return (
    <div className="fixed inset-0 z-50">
      <div className="absolute inset-0 bg-black/30" onClick={onClose} />

      <div className="absolute right-0 top-0 h-full w-full max-w-xl bg-white shadow-xl">
        <div className="flex items-center justify-between border-b px-5 py-4">
          <div className="font-semibold">Product details</div>
          <button
            onClick={onClose}
            className="rounded-xl px-3 py-2 text-sm hover:bg-slate-100"
          >
            Close
          </button>
        </div>

        <div className="h-[calc(100%-65px)] overflow-auto space-y-5 p-5">
          {/* ✅ Image gallery */}
          <div className="space-y-3">
            <div className="aspect-square overflow-hidden rounded-2xl bg-slate-100">
              <img
                src={activeImg}
                alt={title}
                className="h-full w-full object-cover"
                onError={(e) => {
                  e.currentTarget.src = FALLBACK_IMAGE;
                }}
              />
            </div>

            {gallery.length > 1 && (
              <div className="flex gap-2 overflow-x-auto pb-1">
                {gallery.map((src, idx) => {
                  const isActive = src === activeImg;
                  return (
                    <button
                      key={`${src}-${idx}`}
                      onClick={() => setActiveImg(src)}
                      className={`shrink-0 overflow-hidden rounded-xl border ${
                        isActive
                          ? "border-slate-900 ring-2 ring-slate-200"
                          : "border-slate-200"
                      }`}
                      title={`Image ${idx + 1}`}
                    >
                      <img
                        src={src}
                        alt={`Thumbnail ${idx + 1}`}
                        className="h-16 w-16 object-cover"
                        loading="lazy"
                        onError={(e) => {
                          e.currentTarget.src = FALLBACK_IMAGE;
                        }}
                      />
                    </button>
                  );
                })}
              </div>
            )}
          </div>

          <div>
            <div className="text-lg font-semibold">{title}</div>
            {brand && <div className="text-sm text-slate-500">{brand}</div>}
          </div>

          <div className="flex items-center justify-between">
            <div className="text-2xl font-bold">
              {typeof priceNum === "number" && !Number.isNaN(priceNum)
                ? `$${priceNum.toFixed(2)}`
                : "—"}
            </div>
            <StarRating value={rating} />
          </div>

          {desc && <p className="text-sm leading-relaxed text-slate-600">{desc}</p>}

          <div className="flex gap-2">
            <button
              onClick={() => onAskChat?.("Is this product good?")}
              className="flex-1 rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm font-semibold text-slate-900 hover:bg-slate-50"
            >
              Ask: Is it good?
            </button>
            <button
              onClick={() => onAskChat?.("What do people say about this product?")}
              className="flex-1 rounded-xl border px-4 py-2.5 text-sm font-medium hover:bg-slate-50"
            >
              Ask: Reviews
            </button>
          </div>

          <div className="space-y-1 rounded-2xl border bg-slate-50 p-4 text-sm">
            <div className="font-medium">Quick facts</div>
            <div>
              Product ID:{" "}
              <span className="font-mono text-slate-800">{productId ?? "—"}</span>
            </div>
            <div>
              Delivery:{" "}
              <span className="text-slate-800">
                {ui.deliveryEligible ? "Available" : "Unknown"}
              </span>
            </div>
            <div>
              Ingredients:{" "}
              <span className="text-slate-800">
                {product?.ingredients ? "Available" : "Unknown"}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function ChatWidget({ productId, defaultOpen = false }) {
  const [open, setOpen] = useState(defaultOpen);
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([
    { role: "assistant", content: "Hi! Ask about this product (reviews, delivery, ingredients, quality)." },
  ]);
  const [loading, setLoading] = useState(false);

  const ask = async (text) => {
    const q = (text ?? question).trim();
    if (!q) return;

    if (!productId) {
      setMessages((m) => [...m, { role: "assistant", content: "Select a product first so I can answer accurately." }]);
      return;
    }

    setMessages((m) => [...m, { role: "user", content: q }]);
    setQuestion("");
    setLoading(true);

    try {
      const res = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ product_id: String(productId), message: q }),
      });

      if (!res.ok) {
        let err;
        try {
          err = await res.json();
        } catch {
          err = { detail: await res.text() };
        }
        setMessages((m) => [...m, { role: "assistant", content: `Error (${res.status}): ${JSON.stringify(err)}` }]);
        return;
      }

      const data = await res.json();
      const answer = data?.answer ?? data?.assistant_message ?? data?.response ?? "No answer returned.";
      setMessages((m) => [...m, { role: "assistant", content: answer }]);
    } catch (e) {
      setMessages((m) => [...m, { role: "assistant", content: `Something went wrong: ${String(e?.message ?? e)}` }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed bottom-4 right-4 z-50 w-[360px] max-w-[calc(100vw-2rem)]">
      {!open ? (
        <button
          onClick={() => setOpen(true)}
          className="ml-auto flex items-center gap-2 rounded-full bg-slate-900 px-4 py-3 text-sm font-medium text-white shadow-lg hover:bg-slate-800"
          style={{ backgroundColor: "#0f172a", color: "#fff" }} // ✅ fallback if Tailwind missing
        >
          💬 Product Chat
          {productId ? (
            <span className="rounded-full bg-white/15 px-2 py-0.5 text-xs">
              ID: {String(productId).slice(-6)}
            </span>
          ) : null}
        </button>
      ) : (
        <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-xl">
          {/* ✅ Header */}
          <div
            className="flex items-center justify-between px-4 py-3"
            style={{ backgroundColor: "#0f172a", color: "#fff" }} // ✅ guaranteed black bg + white text
          >
            <div>
              <div className="text-sm font-semibold" style={{ color: "#fff" }}>
                Product Chat
              </div>
              <div className="text-xs" style={{ color: "#e2e8f0" }}>
                {productId ? `Context: ${productId}` : "Select a product for best answers"}
              </div>
            </div>

            <button
              onClick={() => setOpen(false)}
              className="rounded-lg px-2 py-1 text-sm"
              style={{ color: "#fff" }}
              aria-label="Minimize chat"
              title="Minimize"
            >
              —
            </button>
          </div>

          {/* Messages */}
          <div className="h-72 space-y-2 overflow-auto px-4 py-3">
            {messages.map((m, i) => (
              <div
                key={i}
                className={cx(
                  "max-w-[85%] rounded-2xl px-3 py-2 text-sm",
                  m.role === "user"
                    ? "ml-auto bg-slate-900 text-white"
                    : "bg-slate-100 text-slate-900"
                )}
              >
                {m.content}
              </div>
            ))}
            {loading && <div className="text-xs text-slate-500">Thinking…</div>}
          </div>

          {/* Input */}
          <div className="border-t border-slate-200 p-3">
            <form
              className="flex gap-2"
              onSubmit={(e) => {
                e.preventDefault();
                ask();
              }}
            >
              <input
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Ask about reviews, delivery, ingredients…"
                className="flex-1 rounded-xl border border-slate-300 bg-slate-50 px-3 py-2 text-sm text-slate-900 placeholder:text-slate-500 outline-none focus:ring-4 focus:ring-slate-100"
              />
              <button
                type="submit"
                className="rounded-xl bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-800 disabled:opacity-50"
                style={{ backgroundColor: "#0f172a", color: "#fff" }} // ✅ fallback
                disabled={loading}
              >
                Ask
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default function App() {
  const [query, setQuery] = useState("running");
  const [items, setItems] = useState([]);
  const [selected, setSelected] = useState(null);
  const [loading, setLoading] = useState(false);

  const [filters, setFilters] = useState({
    minPrice: "",
    maxPrice: "",
    minRating: 0,
    deliveryOnly: false,
  });

  const selectedId = selected?.__ui?.id ?? null;

  // Filters should use normalized fields
  const filteredItems = useMemo(() => {
    const minP = filters.minPrice === "" ? null : Number(filters.minPrice);
    const maxP = filters.maxPrice === "" ? null : Number(filters.maxPrice);
    const minR = Number(filters.minRating || 0);

    return (items || []).filter((p) => {
      const price = Number(p?.__ui?.priceNum ?? NaN);
      const rating = Number(p?.__ui?.rating ?? 0);
      const deliveryEligible = Boolean(p?.__ui?.deliveryEligible);

      if (minP != null && !Number.isNaN(price) && price < minP) return false;
      if (maxP != null && !Number.isNaN(price) && price > maxP) return false;
      if (rating < minR) return false;
      if (filters.deliveryOnly && !deliveryEligible) return false;

      return true;
    });
  }, [items, filters]);

  const search = async () => {
    const q = query.trim();
    if (!q) return;

    setLoading(true);
    setSelected(null);

    try {
      const res = await fetch(`${API_BASE}/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query: q,
          limit: 20,
          include_insights: false,
        }),
      });

      if (!res.ok) {
        const errText = await res.text();
        console.error("Search failed:", res.status, errText);
        setItems([]);
        return;
      }

      const data = await res.json();

      const results =
        Array.isArray(data) ? data :
        Array.isArray(data?.results) ? data.results :
        Array.isArray(data?.items) ? data.items :
        Array.isArray(data?.products) ? data.products :
        [];

      setItems(results.map(normalizeProduct));
    } catch (e) {
      console.error("Search error:", e);
      setItems([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    search();
    // eslint-disable-next-line
  }, []);

  const askFromDrawer = (text) => {
    alert(`Open Product Chat (bottom-right) and ask:\n\n${text}`);
  };

  return (
    <div className="min-h-screen">
      <Header query={query} setQuery={setQuery} onSearch={search} />

      <main className="mx-auto grid max-w-7xl grid-cols-1 gap-6 px-4 py-6 lg:grid-cols-[288px_1fr]">
        <Filters filters={filters} setFilters={setFilters} />

        <section className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-sm text-slate-500">Results</div>
              <div className="text-xl font-semibold">{filteredItems.length} items</div>
            </div>

            <div className="hidden items-center gap-2 md:flex">
              <button className="rounded-xl border bg-white px-3 py-2 text-sm hover:bg-slate-50">
                Sort: Relevance
              </button>
              <button className="rounded-xl border bg-white px-3 py-2 text-sm hover:bg-slate-50">
                View: Grid
              </button>
            </div>
          </div>

          <ProductGrid items={filteredItems} loading={loading} onSelect={setSelected} />
        </section>
      </main>

      <DetailDrawer product={selected} onClose={() => setSelected(null)} onAskChat={askFromDrawer} />

      <ChatWidget productId={selectedId} />
    </div>
  );
}