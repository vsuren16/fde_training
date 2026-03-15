import { useState } from "react";
import "./App.css";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8010";

const sampleQuestions = [
  "What is RAG?",
  "How should chunking work?",
  "What should I monitor in a RAG app?"
];

export default function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("Your answer will appear here.");
  const [sources, setSources] = useState([]);
  const [mode, setMode] = useState("local");
  const [loading, setLoading] = useState(false);

  async function askQuestion(nextQuestion) {
    if (!nextQuestion.trim()) {
      setAnswer("Enter a question first.");
      setSources([]);
      return;
    }

    setLoading(true);
    setAnswer("Retrieving relevant documents...");

    try {
      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ question: nextQuestion })
      });

      const payload = await response.json();
      setAnswer(payload.answer || "No answer returned.");
      setSources(payload.sources || []);
      setMode(payload.mode || "local");
    } catch (error) {
      setAnswer("Unable to reach the backend. Make sure FastAPI is running on port 8010.");
      setSources([]);
      setMode("local");
    } finally {
      setLoading(false);
    }
  }

  function handleSubmit(event) {
    event.preventDefault();
    askQuestion(question);
  }

  return (
    <main className="page-shell">
      <section className="hero-card">
        <p className="eyebrow">React + FastAPI RAG Demo</p>
        <h1>Simple project structure for Git and Azure DevOps</h1>
        <p className="subtitle">
          This demo uses dummy data, local retrieval, and an optional OpenAI SDK path controlled from the root
          <code> .env </code>
          file.
        </p>
      </section>

      <section className="panel">
        <form onSubmit={handleSubmit} className="question-form">
          <label htmlFor="question">Ask a question</label>
          <div className="input-row">
            <input
              id="question"
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              placeholder="Example: How do I structure this for Azure DevOps?"
            />
            <button type="submit" disabled={loading}>
              {loading ? "Thinking..." : "Ask"}
            </button>
          </div>
        </form>

        <div className="chip-row">
          {sampleQuestions.map((item) => (
            <button
              key={item}
              type="button"
              className="chip"
              onClick={() => {
                setQuestion(item);
                askQuestion(item);
              }}
            >
              {item}
            </button>
          ))}
        </div>
      </section>

      <section className="panel results-panel">
        <div className="result-header">
          <h2>Answer</h2>
          <span className="mode-badge">Mode: {mode}</span>
        </div>
        <p className="answer-text">{answer}</p>

        <h2>Retrieved Sources</h2>
        <div className="source-grid">
          {sources.length ? (
            sources.map((source) => (
              <article className="source-card" key={source.id}>
                <h3>{source.title}</h3>
                <p>{source.content}</p>
                <span className="score">Score: {source.score}</span>
              </article>
            ))
          ) : (
            <p className="empty-state">No sources yet.</p>
          )}
        </div>
      </section>
    </main>
  );
}
