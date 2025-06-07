import { useState, useEffect, useRef } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";

function App() {
  const [company, setCompany] = useState("");
  const [url, setUrl] = useState("");
  const [freePlan, setFreePlan] = useState(true);
  const [loading, setLoading] = useState(false);
  const [summary, setSummary] = useState("");
  const [displayedSummary, setDisplayedSummary] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const summaryRef = useRef<HTMLDivElement | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setMessage("");
    setSummary("");
    setDisplayedSummary("");

    try {
      const res = await axios.post("http://localhost:8000/run", {
        company,
        url,
        free_plan: freePlan,
      });
      setMessage(res.data.message);
      setSummary(res.data.summary);
    } catch (err: any) {
      setError(err.response?.data?.error || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!summary) return;

    const words = summary.split(" ");
    let index = 0;

    const interval = setInterval(() => {
      if (index >= words.length) {
        clearInterval(interval);
        return;
      }

      setDisplayedSummary((prev) => {
        const updated = prev + (index > 0 ? " " : "") + words[index];
        setTimeout(() => {
          summaryRef.current?.scrollTo({
            top: summaryRef.current.scrollHeight,
            behavior: "smooth",
          });
        }, 0);
        return updated;
      });

      index++;
    }, 30); // Adjust typing speed here

    return () => clearInterval(interval);
  }, [summary]);

  return (
    <div className="container-fluid bg-light py-5 px-3 min-vh-100 w-100">
      <div className="row">
   
        <div className="col-md-4 mb-4">
          <form onSubmit={handleSubmit} className="bg-white p-4 rounded shadow-sm">
            <h1 className="h4 text-center mb-3">Company Summary Generator</h1>

            <div className="mb-3">
              <input
                type="text"
                value={company}
                onChange={(e) => setCompany(e.target.value)}
                placeholder="Company Name"
                required
                className="form-control"
              />
            </div>

            <div className="mb-3">
              <input
                type="url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="Company URL"
                required
                className="form-control"
              />
            </div>

            <div className="form-check mb-3">
              <input
                className="form-check-input"
                type="checkbox"
                checked={freePlan}
                onChange={() => setFreePlan(!freePlan)}
                id="freePlanCheck"
              />
              <label className="form-check-label" htmlFor="freePlanCheck">
                Use Free Plan (LLaMA3)
              </label>
            </div>

            <button type="submit" className="btn btn-primary w-100" disabled={loading}>
              {loading ? "Generating..." : "Generate Summary"}
            </button>

            {error && <div className="alert alert-danger mt-3">{error}</div>}
            {message && <div className="alert alert-success mt-3">{message}</div>}
          </form>
        </div>

      
        <div className="col-md-8">
          <div
            ref={summaryRef}
            className="bg-white p-4 rounded shadow-sm h-100 overflow-auto"
            style={{ maxHeight: "75vh" }}
          >
            <h5 className="mb-3">Generated Summary</h5>

            {loading ? (
              <div className="d-flex justify-content-center align-items-center" style={{ height: "100%" }}>
                <div className="spinner-border text-primary" role="status">
                  <span className="visually-hidden">Loading...</span>
                </div>
              </div>
            ) : displayedSummary ? (
              <ReactMarkdown>{displayedSummary}</ReactMarkdown>
            ) : (
              <p className="text-muted">Summary will appear here after generation.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
