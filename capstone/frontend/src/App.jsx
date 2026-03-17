import { useEffect, useState } from "react";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8010/api/v1";
const API_ORIGIN = new URL(API_BASE).origin;

// ─── Priority config ────────────────────────────────────────────────────────
const PRIORITY = {
  1: { label: "Critical", color: "#ef4444", bg: "#fef2f2", border: "#fecaca", glow: "rgba(239,68,68,0.15)", bar: "#ef4444" },
  2: { label: "High",     color: "#f97316", bg: "#fff7ed", border: "#fed7aa", glow: "rgba(249,115,22,0.15)", bar: "#f97316" },
  3: { label: "Medium",   color: "#eab308", bg: "#fefce8", border: "#fde68a", glow: "rgba(234,179,8,0.15)",  bar: "#eab308" },
  4: { label: "Low",      color: "#22c55e", bg: "#f0fdf4", border: "#bbf7d0", glow: "rgba(34,197,94,0.15)",  bar: "#22c55e" },
  5: { label: "Minimal",  color: "#3b82f6", bg: "#eff6ff", border: "#bfdbfe", glow: "rgba(59,130,246,0.15)", bar: "#3b82f6" },
};

// ─── SVG Icons ───────────────────────────────────────────────────────────────
const Icons = {
  Search:        () => <svg width="15" height="15" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>,
  Database:      () => <svg width="15" height="15" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>,
  Zap:           () => <svg width="15" height="15" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>,
  Route:         () => <svg width="15" height="15" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>,
  Shield:        () => <svg width="15" height="15" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>,
  Ticket:        () => <svg width="14" height="14" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="M2 9a3 3 0 0 1 0 6v2a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-2a3 3 0 0 1 0-6V7a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"/><path d="M13 5v2M13 17v2M13 11v2"/></svg>,
  FileText:      () => <svg width="14" height="14" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>,
  ChevronRight:  () => <svg width="12" height="12" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24"><polyline points="9 18 15 12 9 6"/></svg>,
  CheckCircle:   () => <svg width="15" height="15" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>,
  AlertTriangle: () => <svg width="15" height="15" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="m10.29 3.86-8.43 14.63A1 1 0 0 0 2.74 20h16.52a1 1 0 0 0 .88-1.51L11.71 3.86a1 1 0 0 0-1.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>,
  Layers:        () => <svg width="15" height="15" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>,
  Spinner:       () => <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" style={{animation:"iq-spin .8s linear infinite"}}><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83" strokeLinecap="round"/></svg>,
  Activity:      () => <svg width="14" height="14" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>,
};

// ─── Sub-components ──────────────────────────────────────────────────────────
function PriorityChip({ value }) {
  if (!value) return <span className="iq-chip iq-chip-neutral">—</span>;
  const p = PRIORITY[value] || { label: `P${value}`, color: "#64748b", bg: "#f1f5f9", border: "#e2e8f0" };

  return (
    <span className="iq-chip" style={{ background: p.bg, color: p.color, border: `1px solid ${p.border}` }}>
      <span className="iq-chip-dot" style={{ background: p.color }} />
      P{value} · {p.label}
    </span>
  );
}

function PriorityBar({ value }) {
  if (!value) return null;
  const p = PRIORITY[value];
  const width = ((6 - value) / 5) * 100;
  return (
    <div className="iq-pbar-track">
      <div className="iq-pbar-fill" style={{ width: `${width}%`, background: p?.bar || "#94a3b8" }} />
    </div>
  );
}

function MetricCard({ icon, label, value, sub, accent, isEmpty }) {
  return (
    <div className="iq-metric" style={{ "--accent": accent }}>
      <div className="iq-metric-bar" />
      <div className="iq-metric-icon">{icon}</div>
      <div className="iq-metric-body">
        <div className="iq-metric-label">{label}</div>
        <div className={`iq-metric-value ${isEmpty ? "iq-metric-empty" : ""}`}>{value}</div>
        {sub && <div className="iq-metric-sub">{sub}</div>}
      </div>
    </div>
  );
}

function StatTile({ label, value, accent }) {
  return (
    <div className="iq-stat" style={{ "--accent": accent }}>
      <div className="iq-stat-glow" style={{ background: accent }} />
      <div className="iq-stat-top-bar" style={{ background: accent }} />
      <div className="iq-stat-value">{value}</div>
      <div className="iq-stat-label">{label}</div>
    </div>
  );
}

function adminStatusTone(value) {
  const normalized = String(value || "").toLowerCase();
  if (
    normalized.includes("connected") ||
    normalized.includes("enabled") ||
    normalized.includes("loaded") ||
    normalized.includes("mongo-backed")
  ) {
    return "iq-admin-strong-ok";
  }
  if (
    normalized.includes("not reachable") ||
    normalized.includes("not configured") ||
    normalized.includes("disconnected") ||
    normalized.includes("disabled")
  ) {
    return "iq-admin-strong-bad";
  }
  return "";
}

function formatJudgeStatus(status) {
  if (!status || status === "not_run") return "—";
  return status.charAt(0).toUpperCase() + status.slice(1);
}

// ─── App ─────────────────────────────────────────────────────────────────────
function formatApiError(error) {
  if (!error) return "Request failed.";
  if (typeof error === "string") return error;
  if (Array.isArray(error)) {
    return error
      .map((item) => {
        if (typeof item === "string") return item;
        if (item?.msg) return item.msg;
        return JSON.stringify(item);
      })
      .join(" ");
  }
  if (typeof error === "object") {
    if (error.detail) return formatApiError(error.detail);
    if (error.message) return String(error.message);
  }
  return "Request failed.";
}

export default function App() {
  const [query,        setQuery]        = useState("");
  const [result,       setResult]       = useState(null);
  const [status,       setStatus]       = useState("Checking dataset status…");
  const [loading,      setLoading]      = useState(false);
  const [datasetReady, setDatasetReady] = useState(false);
  const [categoryFilter, setCategoryFilter] = useState("");
  const [teamFilter, setTeamFilter] = useState("");
  const [filterOptions, setFilterOptions] = useState({ categories: [], teams: [] });
  const [activeTab,    setActiveTab]    = useState("results");
  const [showAdminPanel, setShowAdminPanel] = useState(false);
  const [adminUsername, setAdminUsername] = useState("");
  const [adminPassword, setAdminPassword] = useState("");
  const [adminToken, setAdminToken] = useState(sessionStorage.getItem("incidentiq_admin_token") || "");
  const [adminData, setAdminData] = useState(null);
  const [adminError, setAdminError] = useState("");
  const [adminSignupMode, setAdminSignupMode] = useState(false);
  const [adminNotice, setAdminNotice] = useState("");

  useEffect(() => {
    (async () => {
      try {
        const res  = await fetch(`${API_BASE}/incidents/ingestion/status`);
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Unable to check ingestion status");
        const ready = data.documents_in_mongo > 0;
        setDatasetReady(ready);
        if (ready) {
          const metadataRes = await fetch(`${API_BASE}/incidents/metadata/options`);
          const metadata = await metadataRes.json();
          if (metadataRes.ok) {
            setFilterOptions(metadata);
          }
        }
        setStatus(ready
          ? `Dataset ready — ${data.documents_in_mongo.toLocaleString()} documents indexed.`
          : "Dataset not loaded. Initialize before searching.");
      } catch {
        setStatus(`Backend unreachable at ${API_ORIGIN}.`);
      }
    })();
  }, []);

  async function fetchAdminObservability(token = adminToken) {
    if (!token) return;
    setAdminError("");
    const res = await fetch(`${API_BASE}/admin/observability`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Unable to load admin observability");
    setAdminData(data);
  }

  async function handleAdminLogin() {
    setAdminError("");
    setAdminNotice("");
    try {
      const res = await fetch(`${API_BASE}/admin/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: adminUsername, password: adminPassword }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(formatApiError(data));
      sessionStorage.setItem("incidentiq_admin_token", data.access_token);
      setAdminToken(data.access_token);
      await fetchAdminObservability(data.access_token);
    } catch (e) {
      setAdminError(formatApiError(e.message || e));
    }
  }

  async function handleAdminSignup() {
    setAdminError("");
    setAdminNotice("");
    try {
      const headers = { "Content-Type": "application/json" };
      if (adminToken) {
        headers.Authorization = `Bearer ${adminToken}`;
      }
      const res = await fetch(`${API_BASE}/admin/signup`, {
        method: "POST",
        headers,
        body: JSON.stringify({ username: adminUsername, password: adminPassword }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(formatApiError(data));
      setAdminNotice("Admin account saved in Mongo with a hashed password. You can log in with these credentials.");
      setAdminSignupMode(false);
    } catch (e) {
      setAdminError(formatApiError(e.message || e));
    }
  }

  async function runIngestion() {
    setLoading(true); setStatus("Running ingestion and indexing…");
    try {
      const res  = await fetch(`${API_BASE}/incidents/ingestion/load`, { method: "POST" });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Ingestion failed");
      setDatasetReady(data.documents_in_mongo > 0);
      const metadataRes = await fetch(`${API_BASE}/incidents/metadata/options`);
      const metadata = await metadataRes.json();
      if (metadataRes.ok) {
        setFilterOptions(metadata);
      }
      setStatus(`Ingestion complete — ${data.documents_in_mongo} docs · ${data.vectors_in_chroma} vectors · ${data.vector_mode}`);
    } catch (e) { setStatus(e.message); }
    finally     { setLoading(false); }
  }

  async function runSearch() {
    setLoading(true); setStatus("Searching incidents…");
    if (!query.trim()) {
      setLoading(false);
      setStatus(
        hasMetadataFilter
          ? "Select filters if you want, but add a short incident description before searching."
          : "Enter a short incident description before running search."
      );
      return;
    }
    const filters = {};
    if (categoryFilter) filters.category = categoryFilter;
    if (teamFilter) filters.team = teamFilter;
    const payload = {
      query, top_k: 5,
      filters: Object.keys(filters).length ? filters : null,
    };
    try {
      const res  = await fetch(`${API_BASE}/incidents/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(formatApiError(data));
      setResult(data);
      setActiveTab("results");
      setStatus(
        data.response_mode === "llm_fallback"
          ? "Internal evidence was not sufficiently relevant. OpenAI fallback guidance is active."
          : data.degraded
            ? "Degraded mode — fallback guidance active."
            : `Search complete — ${data.incidents?.length || 0} incidents retrieved.`
      );
    } catch (e) { setStatus(formatApiError(e)); }
    finally     { setLoading(false); }
  }

  async function downloadLogs() {
    try {
      const res = await fetch(`${API_BASE}/admin/logs/download`, {
        headers: { Authorization: `Bearer ${adminToken}` },
      });
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Unable to download logs");
      }
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const anchor = document.createElement("a");
      anchor.href = url;
      anchor.download = adminData?.log_file_path?.split("/").pop() || "application.log";
      anchor.click();
      window.URL.revokeObjectURL(url);
      setAdminNotice("Log download started.");
    } catch (e) {
      setAdminError(e.message);
    }
  }

  const incidentCount  = result?.incidents?.length || 0;
  const triagePriority = result?.triage_priority;
  const triageConfig   = triagePriority ? PRIORITY[triagePriority] : null;
  const judgeStatus    = result?.judge_status || "not_run";
  const judgeScore     = result?.judge_score;
  const judgeReason    = result?.judge_reason;
  const responseMode   = result?.response_mode || "grounded";
  const responseNotice = result?.response_notice;
  const judgeAccent    = judgeStatus === "approved"
    ? "#22c55e"
    : judgeStatus === "degraded"
      ? "#f97316"
      : judgeStatus === "blocked"
        ? "#ef4444"
        : "#94a3b8";
  const judgeValue     = judgeStatus === "not_run"
    ? "—"
    : `${formatJudgeStatus(judgeStatus)}${judgeScore !== null && judgeScore !== undefined ? ` · ${judgeScore.toFixed(2)}` : ""}`;
  const fixAccuracy    = result?.predicted_fix_accuracy;
  const resolutionTime = result?.predicted_resolution_time_hours;
  const handoffPath    = result?.handoff_path?.join(" → ");
  const hasQuery = query.trim().length > 0;
  const hasMetadataFilter = Boolean(categoryFilter || teamFilter);
  const filterGuidance = !hasQuery && hasMetadataFilter
    ? "Filters narrow the search scope, but you still need a short incident description before running search."
    : hasQuery && hasMetadataFilter
      ? `Search will be limited to ${categoryFilter || "all categories"}${teamFilter ? ` and team ${teamFilter}` : ""}.`
      : "Describe the issue in plain language. Optionally narrow results by category or owning team.";

  return (
    <>
      <style>{CSS}</style>
      <div className="iq-shell">

        {/* ═══ NAV ═══ */}
        <nav className="iq-nav">
          <div className="iq-nav-brand">
            <div className="iq-nav-logo"><Icons.Shield /></div>
            <div>
              <div className="iq-nav-name">IncidentIQ</div>
              <div className="iq-nav-sub">Knowledge Base · RAG-Powered</div>
            </div>
          </div>

          <div className="iq-nav-breadcrumb">
            <span className="iq-crumb">IT Support</span>
            <Icons.ChevronRight />
            <span className="iq-crumb iq-crumb-active">Incident Search</span>
          </div>

          <div className="iq-nav-right">
            <div className={`iq-ds-pill ${datasetReady ? "iq-ds-ready" : "iq-ds-warn"}`}>
              <span className="iq-ds-dot" />
              {datasetReady ? "Dataset Ready" : "Not Initialized"}
            </div>
            <button
              className="iq-admin-btn"
              onClick={async () => {
                setShowAdminPanel(true);
                if (adminToken) {
                  try {
                    await fetchAdminObservability(adminToken);
                  } catch (e) {
                    setAdminError(e.message);
                  }
                }
                setAdminNotice("");
              }}
            >
              <Icons.Shield /> Admin
            </button>
          </div>
        </nav>

        {/* ═══ BODY ═══ */}
        <div className="iq-body">

          {/* ── SIDEBAR ── */}
          <aside className="iq-sidebar">

            {/* Search card */}
            <div className="iq-card">
              <div className="iq-card-hd">
                <div className="iq-card-hd-left">
                  <div className="iq-card-icon"><Icons.Search /></div>
                  <span className="iq-card-title">New Search</span>
                </div>
                <span className={`iq-status-chip ${loading ? "iq-chip-working" : "iq-chip-idle"}`}>
                  {loading ? <><Icons.Spinner /> Working…</> : "● Ready"}
                </span>
              </div>

              <label className="iq-label">Describe the Incident</label>
              <textarea
                className="iq-textarea"
                value={query}
                onChange={e => setQuery(e.target.value)}
                placeholder="e.g. Remote users are denied VPN access after successful authentication. What should we check first?"
                rows={5}
              />

              <div className="iq-filter-grid">
                <div>
                  <label className="iq-filter-label">Category</label>
                  <select className="iq-sel" value={categoryFilter} onChange={e => setCategoryFilter(e.target.value)}>
                    <option value="">All categories</option>
                    {filterOptions.categories.map(option => (
                      <option key={option} value={option}>{option}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="iq-filter-label">Team</label>
                  <select className="iq-sel" value={teamFilter} onChange={e => setTeamFilter(e.target.value)}>
                    <option value="">All teams</option>
                    {filterOptions.teams.map(option => (
                      <option key={option} value={option}>{option}</option>
                    ))}
                  </select>
                </div>
              </div>
              <div className="iq-filter-guidance">{filterGuidance}</div>

              <div className="iq-action-stack">
                {!datasetReady && (
                  <button className="iq-btn iq-btn-ghost" onClick={runIngestion} disabled={loading}>
                    {loading ? <Icons.Spinner /> : <Icons.Database />} Initialize Dataset
                  </button>
                )}
                <button className="iq-btn iq-btn-primary" onClick={runSearch} disabled={loading}>
                  {loading ? <Icons.Spinner /> : <Icons.Search />} Run Hybrid Search
                </button>
              </div>

              <div className="iq-statusbar">
                <span className={`iq-led ${loading ? "iq-led-amber" : "iq-led-green"}`} />
                <span className="iq-statusmsg">{status}</span>
              </div>
              {result?.degraded && (
                <div className="iq-degraded-explainer">
                  {responseMode === "llm_fallback"
                    ? "The internal knowledge base did not contain sufficiently relevant evidence for this query, so the assistant routed the request to an AI model for best-effort guidance."
                    : "Degraded mode means the system fell back to a safer summary because OpenAI generation, grounding confidence, or vector-backed reasoning was not strong enough."}
                  {responseMode === "llm_fallback" && (
                    <div className="iq-validation-warning">*Validate the suggested steps before applying</div>
                  )}
                </div>
              )}
            </div>

            {/* Resolution summary */}
            <div className={`iq-resolution ${result?.degraded ? "iq-resolution-degraded" : ""}`}>
              <div className="iq-resolution-hd">
                <div className="iq-resolution-icon">
                  {result?.degraded ? <Icons.AlertTriangle /> : <Icons.CheckCircle />}
                </div>
                <div>
                  <div className="iq-resolution-title">
                    {responseMode === "llm_fallback"
                      ? "LLM Fallback Guidance"
                      : result?.degraded
                        ? "Fallback Guidance"
                        : "Grounded Resolution Summary"}
                  </div>
                  {result?.degraded && (
                    <span className="iq-degraded-tag">
                      {responseMode === "llm_fallback" ? "LLM Fallback" : "Degraded Mode"}
                    </span>
                  )}
                </div>
              </div>
              {responseNotice && (
                <div className="iq-response-notice">
                  <div>{responseNotice}</div>
                  {responseMode === "llm_fallback" && (
                    <div className="iq-validation-warning">*Validate the suggested steps before applying</div>
                  )}
                </div>
              )}
              <p className="iq-resolution-body">
                {result?.resolution_summary
                  || "Grounded resolution guidance will appear here after a successful search, synthesised from historical incident patterns."}
              </p>
              {judgeReason && (
                <div className="iq-judge-note">
                  <div className="iq-judge-note-label">Judge rationale</div>
                  <div className="iq-judge-note-body">{judgeReason}</div>
                </div>
              )}
              {judgeScore !== null && judgeScore !== undefined && (
                <div className="iq-judge-note">
                  <div className="iq-judge-note-label">Judge score</div>
                  <div className="iq-judge-note-body">
                    {judgeScore.toFixed(2)} means the grounding checker found strong overlap between the answer, your query, and the retrieved evidence. It is a groundedness/relevance score, not a pure model confidence score.
                  </div>
                </div>
              )}
              {result?.root_cause_summary && (
                <div className="iq-judge-note">
                  <div className="iq-judge-note-label">Root cause analysis</div>
                  <div className="iq-judge-note-body">{result.root_cause_summary}</div>
                </div>
              )}
            </div>

          </aside>

          {/* ── MAIN ── */}
          <main className="iq-main">

            {/* Stat tiles */}
            <div className="iq-stat-row iq-stat-row-main">
              <StatTile label="Incidents Retrieved" value={incidentCount || "—"}                             accent="#6366f1" />
              <StatTile label="Triage Priority"     value={triagePriority ? `P${triagePriority}` : "—"}     accent={triageConfig?.color || "#94a3b8"} />
              <StatTile label="Escalation Target"   value={result?.route_to || "—"}                          accent="#0ea5e9" />
              <StatTile label="Judge Verdict"       value={formatJudgeStatus(judgeStatus)}                   accent={judgeAccent} />
              <StatTile label="Fix Accuracy"        value={fixAccuracy !== null && fixAccuracy !== undefined ? `${(fixAccuracy * 100).toFixed(0)}%` : "—"} accent="#22c55e" />
              <StatTile label="Resolution ETA"      value={resolutionTime !== null && resolutionTime !== undefined ? `${resolutionTime.toFixed(1)}h` : "—"} accent="#f97316" />
            </div>

            {/* Tabs */}
            <div className="iq-tabbar">
              <button className={`iq-tab ${activeTab==="results"  ? "iq-tab-active" : ""}`} onClick={() => setActiveTab("results")}>
                <Icons.Layers /> Retrieved Evidence
                {incidentCount > 0 && <span className="iq-tab-badge">{incidentCount}</span>}
              </button>
              <button className={`iq-tab ${activeTab==="insights" ? "iq-tab-active" : ""}`} onClick={() => setActiveTab("insights")}>
                <Icons.Activity /> Resolution Insights
              </button>
            </div>

            {/* ── Results tab ── */}
            {activeTab === "results" && (
              <div className="iq-results-scroll">
                {incidentCount === 0 ? (
                  <div className="iq-empty">
                    <div className="iq-empty-icon"><Icons.Search /></div>
                    <div className="iq-empty-title">No incidents retrieved yet</div>
                    <div className="iq-empty-body">Initialize the dataset, describe an incident in plain language, then run a hybrid search to surface similar historical records.</div>
                  </div>
                ) : (
                  <div className="iq-results-list">
                    {result.incidents.map((inc, i) => {
                      const p = PRIORITY[inc.priority];
                      return (
                        <article
                          key={inc.incident_id}
                          className="iq-card iq-result-card"
                          style={{ "--p-color": p?.color || "#e2e8f0", "--p-glow": p?.glow || "transparent" }}
                        >
                          <div className="iq-result-stripe" style={{ background: p?.color || "#e2e8f0" }} />
                          <div className="iq-result-body">

                            {/* Top row */}
                            <div className="iq-result-toprow">
                              <div className="iq-result-id">
                                <Icons.Ticket /><span>{inc.incident_id}</span>
                              </div>
                              <div className="iq-result-badges">
                                <PriorityChip value={inc.priority} />
                                <span className="iq-chip iq-chip-rank">#{i + 1}</span>
                              </div>
                            </div>

                            {/* Priority bar */}
                            {inc.priority && (
                              <div className="iq-pbar-row">
                                <span className="iq-pbar-lbl">Severity</span>
                                <PriorityBar value={inc.priority} />
                                <span className="iq-pbar-tag" style={{color: p?.color}}>{p?.label}</span>
                              </div>
                            )}

                            <h4 className="iq-result-title">{inc.title || "Historical Incident Pattern"}</h4>
                            <p  className="iq-result-text">{inc.description || inc.incident_text}</p>
                            {(inc.category || inc.status || inc.team) && (
                              <p className="iq-result-text" style={{ marginTop: "-4px", color: "#64748b" }}>
                                {[inc.category, inc.status, inc.team].filter(Boolean).join(" · ")}
                              </p>
                            )}

                            {inc.resolution_notes && (
                              <div className="iq-resnote">
                                <div className="iq-resnote-hd"><Icons.FileText /> Resolution Note</div>
                                <p className="iq-resnote-body">{inc.resolution_notes}</p>
                              </div>
                            )}
                          </div>
                        </article>
                      );
                    })}
                  </div>
                )}
              </div>
            )}

            {/* ── Insights tab ── */}
            {activeTab === "insights" && (
              <div className="iq-insights-pane">
                {!result ? (
                  <div className="iq-empty">
                    <div className="iq-empty-icon"><Icons.Activity /></div>
                    <div className="iq-empty-title">No analysis available</div>
                    <div className="iq-empty-body">Run a search to generate triage insights and resolution guidance.</div>
                  </div>
                ) : (
                  <>
                    <div className="iq-insight-banner">
                      <div className="iq-insight-banner-item">
                        <span className="iq-insight-banner-label">Escalation path</span>
                        <span className="iq-insight-banner-value">{handoffPath || "Not available"}</span>
                      </div>
                      <div className="iq-insight-banner-item">
                        <span className="iq-insight-banner-label">Judge verdict</span>
                        <span className="iq-insight-banner-value">{judgeValue}</span>
                      </div>
                    </div>

                    {result.resolution_summary && (
                      <div className="iq-resolution">
                        <div className="iq-resolution-hd">
                          <div className="iq-resolution-icon"><Icons.CheckCircle /></div>
                          <div className="iq-resolution-title">Full Resolution Summary</div>
                        </div>
                        <p className="iq-resolution-body" style={{fontSize:14, lineHeight:1.8}}>{result.resolution_summary}</p>
                      </div>
                    )}

                    {result?.troubleshooting_validation && (
                      <div className="iq-resolution">
                        <div className="iq-resolution-hd">
                          <div className="iq-resolution-icon"><Icons.Shield /></div>
                          <div className="iq-resolution-title">Troubleshooting Validation</div>
                        </div>
                        <p className="iq-resolution-body">
                          {result.troubleshooting_validation.status} · score {result.troubleshooting_validation.score.toFixed(2)}
                        </p>
                        <p className="iq-resolution-body">{result.troubleshooting_validation.reason}</p>
                      </div>
                    )}

                    {result?.agent_messages?.length > 0 && (
                      <div className="iq-resolution">
                        <div className="iq-resolution-hd">
                          <div className="iq-resolution-icon"><Icons.Route /></div>
                          <div className="iq-resolution-title">Agent Handoff Messages</div>
                        </div>
                        {result.agent_messages.map((message, index) => (
                          <p key={`${message.from_agent}-${message.to_agent}-${index}`} className="iq-resolution-body">
                            {message.from_agent} → {message.to_agent}: {message.message}
                          </p>
                        ))}
                      </div>
                    )}
                  </>
                )}
              </div>
            )}

          </main>
        </div>
      </div>

      {showAdminPanel && (
        <div className="iq-admin-overlay" onClick={() => setShowAdminPanel(false)}>
          <div className="iq-admin-panel" onClick={e => e.stopPropagation()}>
            <div className="iq-admin-head">
              <div>
                <div className="iq-admin-title">Admin / Observability</div>
                <div className="iq-admin-sub">Trace access, runtime diagnostics, and admin controls</div>
              </div>
              <div className={`iq-admin-trace-badge ${adminData?.langsmith?.connected ? "iq-admin-trace-on" : "iq-admin-trace-off"}`}>
                {adminData?.langsmith?.connected ? "Trace Connected" : adminData?.tracing_enabled ? "Trace Configured" : "Trace Disabled"}
              </div>
              <button className="iq-admin-close" onClick={() => setShowAdminPanel(false)}>×</button>
            </div>

            {!adminToken ? (
              <div className="iq-admin-form">
                <div className="iq-admin-auth-toggle">
                  <button className={`iq-admin-auth-btn ${!adminSignupMode ? "iq-admin-auth-btn-active" : ""}`} onClick={() => setAdminSignupMode(false)}>
                    Login
                  </button>
                  <button className={`iq-admin-auth-btn ${adminSignupMode ? "iq-admin-auth-btn-active" : ""}`} onClick={() => setAdminSignupMode(true)}>
                    Sign up
                  </button>
                </div>
                <label className="iq-filter-label">Username</label>
                <input className="iq-admin-input" value={adminUsername} onChange={e => setAdminUsername(e.target.value)} />
                <label className="iq-filter-label">Password</label>
                <input className="iq-admin-input" type="password" value={adminPassword} onChange={e => setAdminPassword(e.target.value)} />
                <button className="iq-btn iq-btn-primary" onClick={adminSignupMode ? handleAdminSignup : handleAdminLogin}>
                  <Icons.Shield /> {adminSignupMode ? "Create Admin" : "Login"}
                </button>
                <div className="iq-admin-helper">
                  {adminSignupMode
                    ? "Admin credentials are stored in Mongo as hashed secrets. Create the first admin here, then use those credentials to log in."
                    : "Log in with an existing Mongo-backed admin account, or switch to Sign up to create the first admin."}
                </div>
                {adminNotice && <div className="iq-admin-success">{adminNotice}</div>}
                {adminError && <div className="iq-admin-error">{adminError}</div>}
              </div>
            ) : (
              <div className="iq-admin-body">
                <div className="iq-admin-actions">
                  <button
                    className="iq-btn iq-btn-ghost"
                    onClick={() => adminData?.langsmith_project_url && window.open(adminData.langsmith_project_url, "_blank")}
                    disabled={!adminData?.langsmith_project_url}
                  >
                    View run diagnostics
                  </button>
                  <button className="iq-btn iq-btn-ghost" onClick={() => fetchAdminObservability(adminToken)}>
                    Refresh status
                  </button>
                  <button className="iq-btn iq-btn-ghost" onClick={downloadLogs}>
                    Download logs
                  </button>
                </div>

                {adminData && (
                  <>
                  <div className="iq-admin-grid">
                    <div className="iq-admin-item"><span>Admin Auth</span><strong className={adminStatusTone(adminData.persisted_admins ? "Mongo-backed" : "Signup required")}>{adminData.persisted_admins ? "Mongo-backed" : "Signup required"}</strong></div>
                    <div className="iq-admin-item">
                      <span>MongoDB Connectivity</span>
                      <strong className={adminStatusTone(adminData.mongo.connected ? "Connected" : adminData.mongo.configured ? "Not reachable" : "Not configured")}>{adminData.mongo.connected ? "Connected" : adminData.mongo.configured ? "Not reachable" : "Not configured"}</strong>
                      {adminData.mongo.detail && <small>{adminData.mongo.detail}</small>}
                    </div>
                    <div className="iq-admin-item">
                      <span>Tracing</span>
                      <strong className={adminStatusTone(adminData.tracing_enabled ? "Enabled" : "Disabled")}>{adminData.tracing_enabled ? "Enabled" : "Disabled"}</strong>
                    </div>
                    <div className="iq-admin-item">
                      <span>LangSmith Connectivity</span>
                      <strong className={adminStatusTone(adminData.langsmith.connected ? "Connected" : adminData.langsmith.configured ? "Not reachable" : "Not configured")}>{adminData.langsmith.connected ? "Connected" : adminData.langsmith.configured ? "Not reachable" : "Not configured"}</strong>
                      {adminData.langsmith.detail && <small>{adminData.langsmith.detail}</small>}
                    </div>
                    <div className="iq-admin-item">
                      <span>Vector Index</span>
                      <strong>{adminData.vector_store_count} vectors loaded</strong>
                      <small>{adminData.keyword_index_loaded ? "Keyword index loaded." : "Keyword index not loaded."}</small>
                    </div>
                    <div className="iq-admin-item">
                      <span>Chroma Connectivity</span>
                      <strong className={adminStatusTone(adminData.chroma.connected ? "Connected" : adminData.chroma.configured ? "Not reachable" : "Not configured")}>{adminData.chroma.connected ? "Connected" : adminData.chroma.configured ? "Not reachable" : "Not configured"}</strong>
                      <small>{adminData.chroma.connected ? "Chroma collection is reachable." : adminData.chroma.detail}</small>
                    </div>
                    <div className="iq-admin-item">
                      <span>OpenAI Connectivity</span>
                      <strong className={adminStatusTone(adminData.openai.connected ? "Connected" : adminData.openai.configured ? "Not reachable" : "Not configured")}>{adminData.openai.connected ? "Connected" : adminData.openai.configured ? "Not reachable" : "Not configured"}</strong>
                      {adminData.openai.detail && <small>{adminData.openai.detail}</small>}
                    </div>
                    <div className="iq-admin-item"><span>Logs</span><strong>{adminData.log_file_path}</strong></div>
                  </div>

                  </>
                )}

                {adminNotice && <div className="iq-admin-success">{adminNotice}</div>}
                <button
                  className="iq-btn iq-btn-ghost"
                  onClick={() => {
                    sessionStorage.removeItem("incidentiq_admin_token");
                    setAdminToken("");
                    setAdminData(null);
                    setAdminError("");
                    setAdminNotice("");
                    setAdminSignupMode(false);
                  }}
                >
                  Logout
                </button>
                {adminError && <div className="iq-admin-error">{adminError}</div>}
              </div>
            )}
          </div>
        </div>
      )}
    </>
  );
}

// ─── CSS ─────────────────────────────────────────────────────────────────────
const CSS = `
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;0,9..40,800&family=JetBrains+Mono:wght@500;600&display=swap');

@keyframes iq-spin       { to { transform: rotate(360deg); } }
@keyframes iq-fadeup     { from { opacity:0; transform:translateY(8px); } to { opacity:1; transform:translateY(0); } }
@keyframes iq-pulse-dot  { 0%,100%{opacity:.6;} 50%{opacity:1;} }

*, *::before, *::after { box-sizing:border-box; margin:0; padding:0; }
body { margin:0; }

.iq-shell {
  min-height:100vh;
  background:#eef0f4;
  font-family:'DM Sans',system-ui,sans-serif;
  color:#0f172a;
}

/* ── NAV ── */
.iq-nav {
  height:62px;
  background:#0f172a;
  display:flex; align-items:center; justify-content:space-between;
  padding:0 28px;
  position:sticky; top:0; z-index:200;
  box-shadow:0 1px 0 rgba(255,255,255,.05), 0 4px 24px rgba(0,0,0,.35);
}
.iq-nav-brand { display:flex; align-items:center; gap:12px; }
.iq-nav-logo {
  width:36px; height:36px; border-radius:10px; flex-shrink:0;
  background:linear-gradient(135deg,#3b82f6 0%,#6366f1 100%);
  display:flex; align-items:center; justify-content:center; color:#fff;
  box-shadow:0 0 0 1px rgba(255,255,255,.1), 0 4px 14px rgba(99,102,241,.45);
}
.iq-nav-name { font-size:15px; font-weight:800; color:#f8fafc; letter-spacing:-.4px; line-height:1.2; }
.iq-nav-sub  { font-size:10.5px; color:#475569; font-weight:500; margin-top:1px; }
.iq-nav-breadcrumb { display:flex; align-items:center; gap:8px; }
.iq-crumb { font-size:12.5px; color:#475569; font-weight:500; }
.iq-crumb-active { color:#94a3b8; }
.iq-nav-right { display:flex; align-items:center; gap:14px; }
.iq-admin-btn {
  display:inline-flex; align-items:center; gap:7px;
  background:rgba(255,255,255,.06); color:#e2e8f0; border:1px solid rgba(255,255,255,.1);
  border-radius:8px; padding:7px 12px; font:inherit; font-size:12.5px; font-weight:700; cursor:pointer;
}
.iq-admin-btn:hover { background:rgba(255,255,255,.1); }
.iq-ds-pill {
  display:flex; align-items:center; gap:8px;
  padding:5px 13px; border-radius:20px; font-size:12px; font-weight:600;
}
.iq-ds-ready { background:rgba(34,197,94,.1); color:#4ade80; border:1px solid rgba(34,197,94,.2); }
.iq-ds-warn  { background:rgba(245,158,11,.1); color:#fbbf24; border:1px solid rgba(245,158,11,.2); }
.iq-ds-dot   { width:7px; height:7px; border-radius:50%; animation:iq-pulse-dot 2s ease infinite; }
.iq-ds-ready .iq-ds-dot { background:#4ade80; box-shadow:0 0 6px #4ade80; }
.iq-ds-warn  .iq-ds-dot { background:#fbbf24; box-shadow:0 0 6px #fbbf24; }

/* ── BODY ── */
.iq-body {
  display:grid;
  grid-template-columns:368px 1fr;
  gap:20px;
  padding:24px;
  max-width:1500px;
  margin:0 auto;
  align-items:start;
}

/* ── SIDEBAR ── */
.iq-sidebar {
  display:flex;
  flex-direction:column;
  gap:14px;
  position:sticky;
  top:82px;
  max-height:calc(100vh - 98px);
  overflow-y:auto;
  padding-right:4px;
}

/* ── CARD ── */
.iq-card {
  background:#fff; border-radius:16px; border:1px solid #e2e8f0;
  padding:22px;
  box-shadow:0 1px 3px rgba(0,0,0,.04), 0 6px 18px rgba(0,0,0,.04);
  animation:iq-fadeup .3s ease both;
}
.iq-card-hd { display:flex; align-items:center; justify-content:space-between; margin-bottom:20px; }
.iq-card-hd-left { display:flex; align-items:center; gap:10px; }
.iq-card-icon {
  width:32px; height:32px; border-radius:8px; flex-shrink:0;
  background:linear-gradient(135deg,#eff6ff,#dbeafe);
  display:flex; align-items:center; justify-content:center; color:#3b82f6;
}
.iq-card-title { font-size:14px; font-weight:700; color:#0f172a; }
.iq-status-chip {
  display:inline-flex; align-items:center; gap:5px;
  font-size:11.5px; font-weight:600; padding:4px 11px; border-radius:20px;
}
.iq-chip-idle    { background:#f0fdf4; color:#16a34a; border:1px solid #bbf7d0; }
.iq-chip-working { background:#fff7ed; color:#ea580c; border:1px solid #fed7aa; }

/* ── FORM ── */
.iq-label {
  display:block; font-size:11px; font-weight:700; color:#64748b;
  text-transform:uppercase; letter-spacing:.7px; margin-bottom:8px;
}
.iq-filter-label { font-size:11px; font-weight:600; color:#94a3b8; margin-bottom:5px; display:block; }
.iq-textarea {
  width:100%; border:1.5px solid #e2e8f0; border-radius:10px;
  padding:12px 14px; font-size:13.5px; color:#0f172a;
  background:#f8fafc; resize:vertical; outline:none;
  font-family:inherit; margin-bottom:20px; line-height:1.65;
  transition:border-color .15s, box-shadow .15s, background .15s;
}
.iq-textarea:focus { border-color:#6366f1; box-shadow:0 0 0 3px rgba(99,102,241,.1); background:#fff; }
.iq-textarea::placeholder { color:#cbd5e1; }
.iq-filter-grid { display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:10px; }
.iq-filter-guidance {
  font-size:11.5px;
  color:#64748b;
  line-height:1.55;
  background:#f8fafc;
  border:1px solid #e2e8f0;
  border-radius:8px;
  padding:10px 12px;
  margin-bottom:14px;
}
.iq-sel {
  width:100%; border:1.5px solid #e2e8f0; border-radius:8px;
  padding:8px 32px 8px 11px; font-size:13px; color:#0f172a;
  background:#f8fafc url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='11' height='11' viewBox='0 0 24 24' fill='none' stroke='%2394a3b8' stroke-width='2.5'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E") no-repeat right 10px center;
  appearance:none; outline:none; cursor:pointer; font-family:inherit;
  transition:border-color .15s;
}
.iq-sel:focus { border-color:#6366f1; }

/* ── BUTTONS ── */
.iq-action-stack { display:flex; flex-direction:column; gap:8px; }
.iq-btn {
  display:flex; align-items:center; justify-content:center; gap:7px;
  padding:11px 18px; border-radius:10px; font-size:13.5px; font-weight:700;
  border:none; cursor:pointer; width:100%; font-family:inherit;
  transition:all .18s;
}
.iq-btn-primary {
  background:linear-gradient(135deg,#3b82f6,#6366f1);
  color:#fff;
  box-shadow:0 2px 10px rgba(99,102,241,.35), 0 1px 0 rgba(255,255,255,.1) inset;
  letter-spacing:-.1px;
}
.iq-btn-primary:hover:not(:disabled) { box-shadow:0 6px 20px rgba(99,102,241,.5); transform:translateY(-1px); }
.iq-btn-ghost  { background:#fff; color:#6366f1; border:1.5px solid #c7d2fe; }
.iq-btn-ghost:hover:not(:disabled) { background:#eef2ff; }
.iq-btn:disabled { opacity:.5; cursor:not-allowed !important; transform:none !important; box-shadow:none !important; }

/* ── STATUS BAR ── */
.iq-statusbar {
  display:flex; align-items:flex-start; gap:9px; margin-top:14px;
  padding:10px 13px; background:#f8fafc; border:1px solid #f1f5f9; border-radius:8px;
}
.iq-led { width:8px; height:8px; border-radius:50%; flex-shrink:0; margin-top:3px; }
.iq-led-green { background:#22c55e; box-shadow:0 0 0 3px rgba(34,197,94,.2); }
.iq-led-amber { background:#f59e0b; box-shadow:0 0 0 3px rgba(245,158,11,.2); animation:iq-pulse-dot 1s ease infinite; }
.iq-statusmsg { font-size:12px; color:#64748b; line-height:1.55; }
.iq-degraded-explainer {
  margin-top:10px;
  font-size:11.5px;
  color:#b45309;
  line-height:1.55;
  background:#fffbeb;
  border:1px solid #fde68a;
  border-radius:8px;
  padding:10px 12px;
}

/* ── METRIC CARDS ── */
.iq-metrics-stack { display:flex; flex-direction:column; gap:10px; }
.iq-metric {
  background:#fff; border-radius:14px; border:1px solid #e2e8f0;
  padding:15px 17px; display:flex; align-items:center; gap:13px;
  overflow:hidden; position:relative;
  box-shadow:0 1px 3px rgba(0,0,0,.03);
  animation:iq-fadeup .35s ease both;
}
.iq-metric-bar {
  position:absolute; left:0; top:0; bottom:0; width:4px;
  background:var(--accent,#94a3b8); border-radius:4px 0 0 4px;
}
.iq-metric-icon {
  width:38px; height:38px; border-radius:10px; flex-shrink:0;
  background:color-mix(in srgb, var(--accent,#94a3b8) 10%, white);
  color:var(--accent,#94a3b8);
  display:flex; align-items:center; justify-content:center;
  border:1px solid color-mix(in srgb, var(--accent,#94a3b8) 20%, white);
}
.iq-metric-label { font-size:10.5px; font-weight:700; color:#94a3b8; text-transform:uppercase; letter-spacing:.6px; margin-bottom:3px; }
.iq-metric-value { font-size:14px; font-weight:700; color:#0f172a; margin-bottom:2px; }
.iq-metric-empty { color:#cbd5e1; font-style:italic; font-weight:500; }
.iq-metric-sub   { font-size:11.5px; color:#94a3b8; }

/* ── RESOLUTION CARD ── */
.iq-resolution {
  background:#fff; border-radius:14px; border:1px solid #e2e8f0;
  padding:18px; box-shadow:0 1px 3px rgba(0,0,0,.03);
  animation:iq-fadeup .4s ease both;
}
.iq-sidebar .iq-resolution {
  max-height:calc(100vh - 420px);
  overflow-y:auto;
}
.iq-resolution-degraded { border-color:#fed7aa; background:#fffbf5; }
.iq-resolution-hd   { display:flex; align-items:center; gap:10px; margin-bottom:12px; }
.iq-resolution-icon {
  width:30px; height:30px; border-radius:8px; flex-shrink:0;
  background:linear-gradient(135deg,#dbeafe,#e0e7ff); color:#6366f1;
  display:flex; align-items:center; justify-content:center;
}
.iq-resolution-degraded .iq-resolution-icon { background:#ffedd5; color:#ea580c; }
.iq-resolution-title { font-size:11.5px; font-weight:700; color:#0f172a; text-transform:uppercase; letter-spacing:.5px; }
.iq-degraded-tag {
  display:inline-block; margin-top:3px;
  font-size:10px; font-weight:600; color:#ea580c;
  background:#ffedd5; border:1px solid #fed7aa; padding:1px 7px; border-radius:4px;
}
.iq-resolution-body { font-size:12.5px; color:#475569; line-height:1.7; }
.iq-response-notice {
  margin-bottom:12px;
  padding:10px 12px;
  border-radius:8px;
  background:#fff7ed;
  border:1px solid #fed7aa;
  color:#9a3412;
  font-size:11.5px;
  line-height:1.6;
}
.iq-validation-warning {
  margin-top:8px;
  color:#dc2626;
  font-size:11.5px;
  font-weight:700;
  line-height:1.5;
}
.iq-judge-note {
  margin-top:12px;
  padding-top:12px;
  border-top:1px solid #e2e8f0;
}
.iq-judge-note-label {
  font-size:10.5px;
  font-weight:700;
  color:#94a3b8;
  text-transform:uppercase;
  letter-spacing:.6px;
  margin-bottom:5px;
}
.iq-judge-note-body { font-size:12px; color:#64748b; line-height:1.65; }

/* ── STAT TILES ── */
.iq-stat-row { display:grid; gap:12px; margin-bottom:18px; animation:iq-fadeup .2s ease both; }
.iq-stat-row-main { grid-template-columns:repeat(6,1fr); }
.iq-stat {
  background:#fff; border-radius:14px; border:1px solid #e2e8f0;
  min-height:118px;
  padding:18px 16px; text-align:center; position:relative; overflow:hidden;
  box-shadow:0 1px 3px rgba(0,0,0,.04);
  transition:transform .15s, box-shadow .15s;
  display:flex; flex-direction:column; justify-content:center; align-items:center;
}
.iq-stat:hover { transform:translateY(-2px); box-shadow:0 8px 24px rgba(0,0,0,.09); }
.iq-stat-top-bar { position:absolute; top:0; left:0; right:0; height:3px; }
.iq-stat-glow {
  position:absolute; bottom:-20px; left:50%; transform:translateX(-50%);
  width:70px; height:40px; border-radius:50%;
  opacity:.18; filter:blur(18px); pointer-events:none;
}
.iq-stat-value {
  font-size:28px; font-weight:800; color:#0f172a; line-height:1.1; margin-bottom:6px;
  font-family:'JetBrains Mono', monospace; letter-spacing:-1px;
  min-height:58px;
  display:flex; align-items:center; justify-content:center;
  text-transform:uppercase;
  text-wrap:balance;
  word-break:break-word;
  overflow-wrap:anywhere;
  max-width:100%;
  font-size:clamp(20px, 2vw, 28px);
}
.iq-stat-label { font-size:10.5px; font-weight:700; color:#94a3b8; text-transform:uppercase; letter-spacing:.6px; }

/* ── TABS ── */
.iq-tabbar {
  display:flex; gap:2px;
  background:#fff; border-radius:12px 12px 0 0;
  border:1px solid #e2e8f0; border-bottom:none;
  padding:6px 6px 0;
}
.iq-tab {
  display:flex; align-items:center; gap:7px;
  padding:10px 18px; border-radius:8px 8px 0 0;
  font-size:13px; font-weight:600; color:#64748b;
  border:none; background:transparent; cursor:pointer;
  font-family:inherit; margin-bottom:-1px; border-bottom:2px solid transparent;
  transition:color .15s;
}
.iq-tab:hover:not(.iq-tab-active) { color:#0f172a; }
.iq-tab-active { color:#6366f1; background:#f5f3ff; border-bottom:2px solid #6366f1; }
.iq-tab-badge {
  background:#6366f1; color:#fff; font-size:10.5px; font-weight:700;
  padding:2px 7px; border-radius:20px;
}

/* ── RESULTS ── */
.iq-results-scroll {
  background:#fff; border:1px solid #e2e8f0; border-top:none;
  border-radius:0 0 14px 14px;
  max-height:calc(100vh - 250px); overflow-y:auto; padding:16px;
}
.iq-results-list { display:flex; flex-direction:column; gap:14px; padding-bottom:8px; }

.iq-result-card {
  display:flex; flex-direction:row;
  border-radius:12px; border:1.5px solid #e8ecf2; overflow:hidden;
  cursor:default; padding:0;
  transition:border-color .18s, box-shadow .18s, transform .15s;
  animation:iq-fadeup .25s ease both;
}
.iq-result-card:hover {
  border-color:var(--p-color,#6366f1);
  box-shadow:0 0 0 3px var(--p-glow,rgba(99,102,241,.12)), 0 4px 18px rgba(0,0,0,.07);
  transform:translateY(-1px);
}
.iq-result-stripe { width:5px; flex-shrink:0; min-height:100%; }
.iq-result-body   { padding:17px 20px; flex:1; }
.iq-result-toprow {
  display:flex; align-items:center; justify-content:space-between;
  gap:8px; flex-wrap:wrap; margin-bottom:10px;
}
.iq-result-id {
  display:flex; align-items:center; gap:6px;
  font-size:11.5px; font-weight:600; color:#64748b;
  font-family:'JetBrains Mono',monospace;
}
.iq-result-badges { display:flex; align-items:center; gap:6px; flex-wrap:wrap; }

.iq-pbar-row   { display:flex; align-items:center; gap:9px; margin-bottom:11px; }
.iq-pbar-lbl   { font-size:10.5px; font-weight:600; color:#94a3b8; width:52px; flex-shrink:0; }
.iq-pbar-track { flex:1; height:5px; background:#f1f5f9; border-radius:99px; overflow:hidden; }
.iq-pbar-fill  { height:100%; border-radius:99px; transition:width .5s cubic-bezier(.4,0,.2,1); }
.iq-pbar-tag   { font-size:10.5px; font-weight:700; width:48px; text-align:right; flex-shrink:0; }

.iq-result-title { font-size:14px; font-weight:700; color:#0f172a; margin-bottom:7px; }
.iq-result-text  { font-size:13px; color:#475569; line-height:1.65; margin-bottom:13px; }

.iq-resnote {
  background:#fafbff; border:1px solid #e2e8f0;
  border-radius:9px; padding:12px 14px;
  border-left:3px solid #6366f1;
}
.iq-resnote-hd {
  display:flex; align-items:center; gap:7px;
  font-size:10.5px; font-weight:700; color:#6366f1;
  text-transform:uppercase; letter-spacing:.5px; margin-bottom:7px;
}
.iq-resnote-body { font-size:12.5px; color:#334155; line-height:1.65; }

/* ── CHIPS ── */
.iq-chip {
  display:inline-flex; align-items:center; gap:5px;
  font-size:11px; font-weight:600; padding:3px 9px; border-radius:6px;
}
.iq-chip-dot    { width:6px; height:6px; border-radius:50%; flex-shrink:0; }
.iq-chip-neutral{ background:#f1f5f9; color:#475569; border:1px solid #e2e8f0; }
.iq-chip-rank   { background:#0f172a; color:#f8fafc; font-family:'JetBrains Mono',monospace; font-size:10.5px; }

/* ── EMPTY STATE ── */
.iq-empty { padding:56px 32px; text-align:center; }
.iq-empty-icon {
  width:52px; height:52px; border-radius:14px;
  background:linear-gradient(135deg,#f1f5f9,#e8ecf2); color:#94a3b8;
  display:flex; align-items:center; justify-content:center;
  margin:0 auto 18px;
}
.iq-empty-title { font-size:16px; font-weight:700; color:#0f172a; margin-bottom:8px; }
.iq-empty-body  { font-size:13px; color:#64748b; max-width:360px; margin:0 auto; line-height:1.65; }

/* ── INSIGHTS PANE ── */
.iq-insights-pane {
  background:#fff; border:1px solid #e2e8f0; border-top:none;
  border-radius:0 0 14px 14px; padding:20px;
  display:flex; flex-direction:column; gap:16px;
  max-height:calc(100vh - 250px);
  overflow-y:auto;
}
.iq-insight-banner {
  display:grid;
  grid-template-columns:1.4fr 1fr;
  gap:12px;
}
.iq-insight-banner-item {
  background:#f8fafc;
  border:1.5px solid #e2e8f0;
  border-radius:12px;
  padding:16px 18px;
}
.iq-insight-banner-label {
  display:block;
  font-size:10.5px;
  font-weight:700;
  color:#94a3b8;
  text-transform:uppercase;
  letter-spacing:.6px;
  margin-bottom:8px;
}
.iq-insight-banner-value {
  display:block;
  font-size:18px;
  font-weight:800;
  color:#0f172a;
  line-height:1.35;
  text-transform:uppercase;
}

/* ── SCROLLBAR ── */
.iq-results-scroll::-webkit-scrollbar,
.iq-insights-pane::-webkit-scrollbar,
.iq-sidebar::-webkit-scrollbar,
.iq-sidebar .iq-resolution::-webkit-scrollbar { width:5px; }
.iq-results-scroll::-webkit-scrollbar-track,
.iq-insights-pane::-webkit-scrollbar-track,
.iq-sidebar::-webkit-scrollbar-track,
.iq-sidebar .iq-resolution::-webkit-scrollbar-track { background:transparent; }
.iq-results-scroll::-webkit-scrollbar-thumb,
.iq-insights-pane::-webkit-scrollbar-thumb,
.iq-sidebar::-webkit-scrollbar-thumb,
.iq-sidebar .iq-resolution::-webkit-scrollbar-thumb { background:#e2e8f0; border-radius:99px; }
.iq-results-scroll::-webkit-scrollbar-thumb:hover,
.iq-insights-pane::-webkit-scrollbar-thumb:hover,
.iq-sidebar::-webkit-scrollbar-thumb:hover,
.iq-sidebar .iq-resolution::-webkit-scrollbar-thumb:hover { background:#cbd5e1; }

.iq-admin-overlay {
  position:fixed; inset:0; background:rgba(15,23,42,.45); display:flex; justify-content:flex-end; z-index:500;
}
.iq-admin-panel {
  width:420px; max-width:100%; height:100%; background:#fff; padding:22px; box-shadow:-12px 0 40px rgba(0,0,0,.18);
  display:flex; flex-direction:column; gap:18px; overflow-y:auto;
}
.iq-admin-head { display:flex; align-items:flex-start; justify-content:space-between; gap:16px; }
.iq-admin-title { font-size:18px; font-weight:800; color:#0f172a; }
.iq-admin-sub { font-size:12px; color:#64748b; margin-top:4px; }
.iq-admin-trace-badge {
  padding:6px 10px; border-radius:999px; font-size:11px; font-weight:700; white-space:nowrap;
  border:1px solid #e2e8f0;
}
.iq-admin-trace-on { background:#f0fdf4; color:#15803d; border-color:#bbf7d0; }
.iq-admin-trace-off { background:#f8fafc; color:#64748b; }
.iq-admin-close {
  width:32px; height:32px; border-radius:8px; border:1px solid #e2e8f0; background:#fff; cursor:pointer; font-size:20px;
}
.iq-admin-form, .iq-admin-body { display:flex; flex-direction:column; gap:12px; }
.iq-admin-auth-toggle { display:flex; gap:8px; margin-bottom:4px; }
.iq-admin-auth-btn {
  flex:1; border:1px solid #e2e8f0; background:#f8fafc; color:#64748b; border-radius:10px; padding:9px 12px; font:inherit; font-weight:700; cursor:pointer;
}
.iq-admin-auth-btn-active { background:#eef2ff; color:#4f46e5; border-color:#c7d2fe; }
.iq-admin-input {
  width:100%; border:1.5px solid #e2e8f0; border-radius:10px; padding:10px 12px; font:inherit; outline:none; background:#f8fafc;
}
.iq-admin-input:focus { border-color:#6366f1; box-shadow:0 0 0 3px rgba(99,102,241,.1); background:#fff; }
.iq-admin-actions { display:grid; grid-template-columns:1fr 1fr; gap:10px; }
.iq-admin-grid { display:grid; grid-template-columns:1fr 1fr; gap:10px; }
.iq-admin-item {
  background:#f8fafc; border:1px solid #e2e8f0; border-radius:10px; padding:12px;
}
.iq-admin-item span { display:block; font-size:10.5px; text-transform:uppercase; letter-spacing:.5px; color:#94a3b8; margin-bottom:6px; }
.iq-admin-item strong { display:block; font-size:12.5px; line-height:1.5; color:#0f172a; word-break:break-word; }
.iq-admin-strong-ok { color:#15803d !important; }
.iq-admin-strong-bad { color:#dc2626 !important; }
.iq-admin-item small { display:block; margin-top:6px; font-size:11px; line-height:1.45; color:#64748b; word-break:break-word; }
.iq-admin-helper { font-size:12px; line-height:1.6; color:#64748b; background:#f8fafc; border:1px solid #e2e8f0; padding:11px 12px; border-radius:10px; }
.iq-admin-success { font-size:12px; color:#166534; background:#f0fdf4; border:1px solid #bbf7d0; padding:10px 12px; border-radius:8px; }
.iq-admin-error { font-size:12px; color:#b91c1c; background:#fef2f2; border:1px solid #fecaca; padding:10px 12px; border-radius:8px; }
`;
