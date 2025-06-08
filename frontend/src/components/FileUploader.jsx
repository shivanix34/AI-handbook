import React, { useState } from 'react';
import axios from 'axios';

function FileUploader() {
  const [file, setFile] = useState(null);
  const [downloadUrl, setDownloadUrl] = useState(null);
  const [message, setMessage] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setMessage('Uploading and analyzing...');
    try {
      const response = await axios.post('http://127.0.0.1:8000/analyze/', formData, {
        responseType: 'blob',
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      setDownloadUrl(url);
      setMessage('Analysis complete. Download the result below.');
    } catch (error) {
      console.error(error);
      setMessage('Error during analysis');
    }
  };

  return (
    <div className="p-4 text-center">
      <input type="file" accept=".csv" onChange={handleFileChange} />
      <button onClick={handleUpload} className="ml-2 px-4 py-2 bg-blue-500 text-white rounded">
        Upload & Analyze
      </button>
      <p>{message}</p>
      {downloadUrl && (
        <a href={downloadUrl} download="final_enriched_leads.csv" className="text-blue-600 underline">
          Download Enriched CSV
        </a>
      )}
    </div>
  );
}

export default FileUploader;
