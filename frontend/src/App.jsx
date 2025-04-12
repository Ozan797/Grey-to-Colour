import { useState, useRef } from "react";
import "./App.css";

function App() {
  const [original, setOriginal] = useState(null);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeIndex, setActiveIndex] = useState(0);
  const lastFile = useRef(null);

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    lastFile.current = file;
    setOriginal(URL.createObjectURL(file));
    setLoading(true);
    setResults([]);
    setActiveIndex(0);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:8000/api/colourise-image", {
        method: "POST",
        body: formData,
      });

      if (res.ok) {
        const data = await res.json();
        await new Promise((resolve) => setTimeout(resolve, 500));
        setResults(data.images);
      } else {
        alert("Error colourising image.");
      }
    } catch (err) {
      alert("Error connecting to backend.");
    }

    setLoading(false);
  };

  const prevImage = () => {
    setActiveIndex((prev) => Math.max(prev - 1, 0));
  };

  const nextImage = () => {
    setActiveIndex((prev) => Math.min(prev + 1, results.length - 1));
  };

  return (
    <div className="container">
      <h1>🎨 Grey to Colour</h1>

      <div
        className="dropzone"
        onDragOver={(e) => e.preventDefault()}
        onDrop={(e) => {
          e.preventDefault();
          const file = e.dataTransfer.files[0];
          if (file) handleUpload({ target: { files: [file] } });
        }}
        onClick={() => document.getElementById("fileInput").click()}
      >
        <p>📁 Drag and drop an image here, or click to upload</p>
        <input
          id="fileInput"
          type="file"
          accept="image/*"
          style={{ display: "none" }}
          onChange={handleUpload}
        />
      </div>

      {original && (
        <div className="image-grid">
          <div>
            <h2>Original</h2>
            <img src={original} alt="Original" />
          </div>
        </div>
      )}

      {loading && <div className="spinner" />}

      {results.length > 0 && !loading && (
        <div className="carousel-wrapper">
          <h2>Variation {activeIndex + 1}</h2>
          <div className="carousel">
            <button className="nav-button" onClick={prevImage} disabled={activeIndex === 0}>‹</button>
            <img src={results[activeIndex]} alt={`Variation ${activeIndex + 1}`} />
            <button className="nav-button" onClick={nextImage} disabled={activeIndex === results.length - 1}>›</button>
          </div>
        </div>
      )}

      {results.length > 0 && !loading && (
        <div className="feedback-form">
          <h3>Feedback</h3>
          <textarea placeholder="Tell us what you think..." />
          <button onClick={() => alert("Feedback submitted (not saved)")}>Submit</button>
        </div>
      )}
    </div>
  );
}

export default App;