# FDE Simulation Exercise
## Designing an AI-Powered E-Commerce Search System

## Section 2 - Problem Breakdown

### 2.1 Technical Risks
- **Embedding drift:** Product language changes over time (new brands/features), but embedding quality may decay if models and training assumptions are not refreshed.
- **Stale index risk:** Inventory and price updates can lag behind vector index refresh cycles, causing unavailable products to rank highly.
- **Latency and reliability risk:** Multi-stage retrieval (dense + sparse + re-rank + generation) can violate SLA under peak traffic.
- **Re-ranking regression risk:** A new re-ranker or weight tuning can silently reduce relevance quality.
- **Hallucination risk:** LLM may fabricate product attributes or recommend products not in retrieved context.
- **Data quality risk:** Missing metadata (category, brand, stock status) creates retrieval and filtering failures.
- **Model version risk:** Uncontrolled model/prompt changes create inconsistent behavior and hard-to-debug incidents.

### 2.2 Business Risks
- **Conversion loss:** Irrelevant recommendations reduce click-through and add-to-cart rates.
- **Revenue leakage:** Wrong ranking can hide high-margin or high-intent products.
- **Brand trust erosion:** Repeated incorrect answers reduce customer confidence and repeat purchase behavior.
- **Operational cost increase:** More support tickets and manual escalations due to bad recommendations.
- **Legal/compliance exposure:** Recommending restricted or discontinued products can trigger consumer protection and advertising compliance issues.

### 2.3 User Experience Risks
- **Low relevance frustration:** Customer cannot find suitable products despite clear intent.
- **Inconsistent answers:** Similar queries produce different recommendations without clear reason.
- **Overconfident explanations:** System sounds certain when evidence is weak.
- **Filter confusion:** Price/category constraints are ignored or inconsistently applied.
- **Poor fallback behavior:** No helpful refinement guidance when retrieval confidence is low.

### 2.4 Monitoring Gaps (No Evaluation Pipeline)
- **Silent regressions:** Quality can drop after model/prompt/index updates with no detection.
- **No root-cause visibility:** Teams cannot separate retrieval failures from generation failures.
- **No release gate:** Changes move to production without score-based validation.
- **No trend tracking:** Performance drift over weeks is missed.
- **No accountability:** Inability to prove what the system knew and why it answered in a specific way.

---

## Section 3 - Architecture Design

### 3.1 High-Level Pipeline Design (Step-by-Step)
1. **Catalog ingestion:** Pull product catalog, inventory, pricing, policy flags, and metadata from source systems.
2. **Normalization and validation:** Standardize attributes, remove malformed records, enforce schema checks.
3. **Embedding generation:** Create embeddings for title, description, and key attributes.
4. **Indexing layer:** Store vectors in vector DB and lexical fields in BM25-capable search index.
5. **Query understanding:** Parse intent, extract entities, and normalize filters (price/category/brand/availability/region).
6. **Hybrid retrieval:** Run dense semantic retrieval + sparse lexical retrieval; union and deduplicate candidates.
7. **Hard filtering:** Apply strict compliance and catalog constraints (in-stock, legal region, category, price bounds).
8. **Re-ranking:** Re-rank top-N candidates with a cross-encoder/LLM re-ranker for final relevance ordering.
9. **RAG context assembly:** Build evidence context from top products, including product IDs/SKUs and factual fields only.
10. **Guardrailed generation:** LLM generates recommendations and explanations with citation requirements and refusal rules.
11. **LLM-as-Judge evaluation:** Judge model scores relevance, faithfulness, completeness; outputs `EvaluationRecord`.
12. **Logging and monitoring:** Persist all trace events, scores, latency, and business metrics to dashboards and audit store.

### 3.2 Retrieval Strategy
- **Semantic retrieval:** Use embedding-based ANN search over product vectors; optimize recall in top-K.
- **Re-ranking:** Apply cross-encoder or LLM re-ranker on merged candidate set (e.g., top 100 -> top 20).
- **Filtering:** Enforce hard filters before final response:
  - price range
  - category/brand constraints
  - in-stock and region/legal constraints
- **Hybrid scoring approach:** Weighted blend of dense score, sparse score, and rerank score for robust relevance.

### 3.3 Hallucination Prevention Strategy
- **Grounding constraint:** LLM may only recommend products present in assembled context.
- **Citation requirement:** Every recommendation must include citation to product ID/SKU.
- **Schema-constrained output:** Response must conform to `GroundedResponse` structure.
- **Confidence gating:** If retrieval confidence is low, return safe fallback and ask clarifying question.
- **Policy filter guardrail:** Block discontinued/restricted products before generation.
- **Post-generation validator:** Reject answers with unknown product IDs or unsupported claims.

### 3.4 Evaluation Strategy
- **Measure relevance:** Offline golden dataset scored with NDCG@10, Recall@K, MRR.
- **Detect regression:** CI/CD release gate compares candidate model/prompt to production baseline.
- **Compare prompts:** A/B test prompt versions with fixed retrieval and judge scoring.
- **Track performance over time:** Dashboard tracks quality, hallucination, latency, cost, and conversion trends daily/weekly.
- **Human calibration loop:** Weekly human audit sample calibrates LLM-as-Judge drift.

---

## Section 4 - Stress Test (D: Legal Requires Full Traceability)

### 4.1 Identify Impact
- Affected components:
  - Orchestration layer (must attach lineage IDs end-to-end)
  - Logging schema (must capture all decision artifacts)
  - Storage architecture (immutable, queryable audit logs)
  - Compliance workflow (retention, access controls, legal replay)

### 4.2 Mitigation Plan
- Introduce a mandatory `request_id` + `trace_id` propagated across all services.
- Persist an **evidence bundle** per response:
  - user query + filters
  - retrieved candidate IDs + retrieval scores
  - re-ranker inputs/outputs
  - prompt template version/hash
  - model and model version
  - final answer + citations
  - judge scores
- Use immutable/WORM-style audit storage with retention policy.
- Add replay endpoint for legal/compliance to reconstruct full decision path.
- Enforce deployment block if trace completeness checks fail.

### 4.3 Logging & Investigation (First Metrics to Inspect)
- **Trace completeness rate** (% responses with full evidence bundle)
- **Missing citation rate** (% responses with uncited recommendations)
- **Version mismatch rate** (logged model/prompt mismatch with deployment manifest)
- **Policy-violation recommendation rate** (restricted/discontinued item leak-through)
- **Audit replay success rate** (% requests fully reconstructable)

---

## Section 5 - Business Impact Justification

### 5.1 Revenue Improvement
- Better relevance improves product discovery and reduces search abandonment.
- Higher ranking quality increases CTR and add-to-cart rates.
- Conversational explanations improve confidence and purchase completion.
- Measured outcome target: conversion uplift from search sessions (A/B validated).

### 5.2 Operational Risk Reduction
- Hallucination guardrails reduce false recommendations and compliance incidents.
- Full traceability enables faster legal response and incident triage.
- Monitoring plus release gates prevent silent quality regressions.
- Structured fallbacks reduce customer support burden from incorrect AI answers.

### 5.3 Faster Experimentation
- Modular pipeline lets teams swap retriever/reranker/prompt independently.
- Automated evaluation shortens experiment cycles and reduces manual QA bottlenecks.
- Versioned prompts/models with judge scoring enable safe, rapid iteration.
- Canary and A/B rollout patterns reduce blast radius of failed experiments.

---

## Section 6 - Evaluation Metrics Definition (KPIs)

### KPI 1: NDCG@10 (Relevance Quality)
- **Measurement method:** Offline golden set scored per query; weighted average NDCG@10.
- **Alert threshold:** Drop >5% vs 14-day baseline or absolute <0.78.
- **Monitoring frequency:** Daily batch + pre-release gate.

### KPI 2: Grounded Citation Rate
- **Measurement method:** % generated recommendations that map to retrieved product IDs/SKUs.
- **Alert threshold:** <99.5% grounded outputs.
- **Monitoring frequency:** Real-time stream with hourly rollups.

### KPI 3: Hallucination Rate
- **Measurement method:** % responses containing non-catalog or unsupported claims (validator + judge + human sample).
- **Alert threshold:** >0.5% for any 24-hour window.
- **Monitoring frequency:** Continuous; daily compliance report.

### KPI 4: P95 End-to-End Latency
- **Measurement method:** P95 latency from query receipt to final response.
- **Alert threshold:** >1200 ms sustained for 15 minutes.
- **Monitoring frequency:** Real-time dashboard and pager alerting.

### KPI 5: Search-to-Purchase Conversion Uplift
- **Measurement method:** A/B comparison of conversion rate in search-origin sessions.
- **Alert threshold:** No uplift after 2-week experiment or negative trend >2%.
- **Monitoring frequency:** Weekly experiment review.

### KPI 6: Cost per Search Query
- **Measurement method:** (Model inference + retrieval infra + reranker cost) / total search queries.
- **Alert threshold:** >15% increase week-over-week without quality gain.
- **Monitoring frequency:** Daily FinOps report.

### KPI 7: Trace Completeness Rate
- **Measurement method:** % responses with complete `AuditEvent` payload and replayable lineage.
- **Alert threshold:** <99.9%.
- **Monitoring frequency:** Real-time plus daily audit summary.

---

## Section 7 - Modular Thinking Reflection

### Why is modular orchestration important for FDE deployments?
Modular orchestration isolates retrieval, ranking, generation, and evaluation so teams can improve one stage without destabilizing the whole system. It supports faster debugging, safer rollouts, and clearer ownership boundaries.

### Why should evaluation be automated?
Manual review does not scale and misses silent regressions. Automated evaluation creates objective release gates, continuous quality tracking, and faster iteration cycles.

### What is the danger of relying only on demos?
Demos hide edge cases, traffic variance, and long-tail failures. A system that looks good in a controlled demo can fail in production due to drift, latency, and compliance issues.

### What would you change if the system scaled to 1 million products?
- Move to high-performance ANN indexing with sharding.
- Use incremental embedding/index updates for near real-time catalog changes.
- Add tiered retrieval (coarse recall -> fine rerank) for cost/latency control.
- Partition indexes by locale/category and use caching for frequent intents.
- Strengthen observability for per-shard quality and latency hotspots.

---

## Section 8 - Executive Pitch (3 Minutes)

### 1) Problem
Our current keyword search misses user intent, causing poor relevance, lost conversion, and no measurable control over AI quality.

### 2) Architecture
We propose a multi-stage AI search stack: hybrid retrieval (semantic + keyword), strict filtering, re-ranking, grounded RAG generation, and judge-based evaluation.

### 3) Risk Controls
Hallucination is constrained by citation-required generation, schema validation, and policy filters. Legal traceability is guaranteed through immutable audit logs with full decision lineage.

### 4) Evaluation and KPIs
We will monitor NDCG@10, hallucination rate, grounded citation rate, latency, conversion uplift, cost/query, and trace completeness. Releases are gated by offline + online evaluation.

### 5) Business Value
Expected outcomes are higher conversion and revenue from improved relevance, lower operational and legal risk, and faster experimentation through modular architecture and automated evaluation.

### 6) Rollout Plan
Shadow mode -> canary -> A/B testing -> full rollout, with rollback triggers tied to KPI thresholds.

---

## Public APIs / Interfaces / Types (Reference)

```ts
type SearchRequest = {
  query: string;
  filters?: {
    category?: string;
    min_price?: number;
    max_price?: number;
    brand?: string;
    in_stock?: boolean;
  };
  user_context?: {
    locale: string;
    device: "web" | "mobile";
    segment?: string;
  };
};

type CandidateItem = {
  product_id: string;
  title: string;
  price: number;
  availability: "in_stock" | "out_of_stock" | "discontinued";
  retrieval_scores: { dense: number; sparse: number };
  rerank_score: number;
};

type GroundedResponse = {
  answer_text: string;
  recommended_products: string[];
  citations: string[]; // product IDs/SKUs
  confidence: number;
};

type EvaluationRecord = {
  request_id: string;
  timestamp: string;
  prompt_version: string;
  model_version: string;
  scores: {
    relevance: number;
    faithfulness: number;
    completeness: number;
    overall: number;
  };
  business_metrics?: {
    ctr?: number;
    add_to_cart?: number;
    conversion?: number;
  };
};

type AuditEvent = {
  request_id: string;
  trace_id: string;
  query: string;
  filters: Record<string, unknown>;
  retrieved_candidates: Array<{ product_id: string; dense: number; sparse: number }>;
  reranked_candidates: Array<{ product_id: string; rerank_score: number }>;
  prompt_hash: string;
  model_version: string;
  response: GroundedResponse;
  judge_scores: EvaluationRecord["scores"];
};
```

---

## Test Cases and Scenarios
- Happy path: Relevant query returns grounded products with valid citations.
- No-match path: Low-confidence retrieval triggers safe fallback and query refinement.
- Conflicting filters: Strict precedence resolves conflict with clear user message.
- Discontinued product present in corpus: Blocked by availability/compliance filter.
- Prompt regression: Eval gate catches 20% quality drop and blocks release.
- Legal replay: Compliance can reconstruct end-to-end decision for any request ID.
- 10x traffic drill: System meets SLA using scaling + degraded-but-safe response mode.
