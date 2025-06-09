import React, { useState, useRef } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [downloadUrl, setDownloadUrl] = useState(null);
  const [error, setError] = useState("");

  // Add this line:
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setDownloadUrl(null);
    setError("");
  };

const handleUpload = async () => {
  if (!file) {
    setError("Please select a CSV file first.");
    return;
  }
  setLoading(true);
  setError("");
  setDownloadUrl(null);

  const formData = new FormData();
  formData.append("file", file);

  try {
    await fetch("https://ai-handbook.onrender.com/health");

    const response = await fetch("https://ai-handbook.onrender.com/analyze/", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.statusText}`);
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "final_enriched_leads.csv";
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);

    setFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = null;
    }
  } catch (err) {
    setError("Upload failed: " + err.message);
  } finally {
    setLoading(false);
  }
};

  return (
    <div className="app-container">
      <header className="app-header">AI SaaSquatch Leads Analyzer</header>

      <main className="app-main">
        <div className="left-panel">
          <div className="info-item">
            <span className="info-icon">1</span>
            <div>
              <p className="info-title">Scraping Leads</p>
              <p className="info-desc">Instantly gather targeted company and contact data from public sources.</p>
            </div>
          </div>
          <div className="info-item">
            <span className="info-icon">2</span>
            <div>
              <p className="info-title">Enrichment for Lead Details</p>
              <p className="info-desc">Get enriched profiles: emails, phones, LinkedIn, industry, revenue, and more.</p>
            </div>
          </div>
          <div className="info-item">
            <span className="info-icon">3</span>
            <div>
              <p className="info-title">AI-Powered Insights</p>
              <p className="info-desc">Get AI-powered insights with the lead score for better lead prioritization.</p>
            </div>
          </div>
          <div className="info-item">
            <span className="info-icon">4</span>
            <div>
              <p className="info-title">Save & Export Leads</p>
              <p className="info-desc">Save your leads to your dashboard and export to CSV or Excel for your workflow.</p>
            </div>
          </div>
          <div className="info-item">
            <span className="info-icon">5</span>
            <div>
              <p className="info-title">Enterprise Outreach Tools</p>
              <p className="info-desc">Cold call or email directly from the platform (for enterprise members).</p>
            </div>
          </div>
        </div>


        <div className="upload-card">
          <h2>Upload Your Lead List CSV</h2>

          <div className="file-upload-group">
            <input
              type="file"
              accept=".csv"
              onChange={handleFileChange}
              className="file-input"
              ref={fileInputRef}   // <-- Add this line
            />
          </div>

          <button onClick={handleUpload} disabled={loading} className="upload-button">
            {loading ? "Processing..." : "Upload & Analyze"}
          </button>

          {error && <p className="error-message">{error}</p>}

          {downloadUrl && (
            <p className="download-message">
              Processing complete!{" "}
              <a href={downloadUrl} download="final_enriched_leads.csv">
                Download Enriched CSV
              </a>
            </p>
          )}
        </div>
      </main>

      <footer className="app-footer">
        &copy; {new Date().getFullYear()} AI SaaSquatch Leads Analyzer
      </footer>
    </div>
  );
}

export default App;
