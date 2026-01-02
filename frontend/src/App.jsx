import { useState, useRef } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [uploadedVideoUrl, setUploadedVideoUrl] = useState(null);
  const [segmentedVideoUrl, setSegmentedVideoUrl] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setUploadedVideoUrl(URL.createObjectURL(selectedFile));
      setSegmentedVideoUrl(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("https://xyz9843-video-segmentation-backend.hf.space/segment", formData, {
        responseType: 'blob',
      });

      const url = URL.createObjectURL(new Blob([response.data]));
      setSegmentedVideoUrl(url);
    } catch (error) {
      console.error("Error uploading:", error);
      alert("Error processing video. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <header>
        <h1>VideoSegment AI</h1>
        <p className="subtitle">Instant precision background removal for your videos</p>
      </header>

      <main>
        <div className="card">
          <div className="upload-area" onClick={() => fileInputRef.current.click()}>
            <input
              type="file"
              accept="video/*"
              onChange={handleFileChange}
              className="file-input"
              ref={fileInputRef}
            />
            <div className="upload-content">
              {file ? (
                <p>Selected: <strong>{file.name}</strong></p>
              ) : (
                <p>Click or drag to upload a video</p>
              )}
            </div>
          </div>

          <div className="button-group">
            <button onClick={handleUpload} disabled={loading || !file}>
              {loading ? "Processing Video..." : "Segment Now"}
            </button>
          </div>
        </div>

        {loading && (
          <div className="loader-container">
            <div className="spinner"></div>
            <div className="loading-text">OUR AI IS WORKING ITS MAGIC...</div>
          </div>
        )}

        {(uploadedVideoUrl || segmentedVideoUrl) && !loading && (
          <div className="video-grid">
            {uploadedVideoUrl && (
              <div className="video-wrapper">
                <h3>Original Video</h3>
                <video controls src={uploadedVideoUrl}></video>
              </div>
            )}

            {segmentedVideoUrl ? (
              <div className="video-wrapper">
                <h3>Segmented Video</h3>
                <video controls src={segmentedVideoUrl}></video>
                <div style={{ position: 'absolute', bottom: '15px', right: '20px' }}>
                  <a href={segmentedVideoUrl} download="segmented.mp4" className="download-btn">
                    Download
                  </a>
                </div>
              </div>
            ) : file && (
              <div className="video-wrapper placeholder">
                <h3>Output Preview</h3>
                <p style={{ color: 'var(--text-dim)' }}>Process your video to see result</p>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;