import { useState } from 'react';

export default function Home() {
  const [image, setImage] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleImageChange = (e) => {
    setImage(e.target.files[0]);
    setResult(null); // Clear previous result
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!image) return;

    const formData = new FormData();
    formData.append("image", image);
    setLoading(true);

    try {
      const res = await fetch("http://localhost:5000/process", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error("Upload failed", err);
      alert("Upload failed. Check server logs.");
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Car Plate OCR & Weather Detection</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" accept="image/*" onChange={handleImageChange} required />
        <button type="submit" style={{ marginLeft: '1rem' }}>Upload</button>
      </form>

      {loading && <p>Processing image...</p>}

      {result && (
        <div style={{ marginTop: '2rem' }}>
          <h2>Result</h2>
          <p><strong>License Plate:</strong> {result.plate}</p>
          <p><strong>Weather Condition:</strong> {result.weather}</p>
        </div>
      )}
    </div>
  );
}
