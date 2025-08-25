import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState("");

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post('/api/extract', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setResult(JSON.stringify(res.data, null, 2));
    } catch (error) {
      setResult("Error: " + error.message);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>OCR Extractor</h2>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload & Extract</button>
      <pre>{result}</pre>
    </div>
  );
}

export default App;
