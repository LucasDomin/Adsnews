import { useEffect, useState } from "react";
import axios from "axios";

export default function App() {
  const [ads, setAds] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/ads")
      .then(res => {
        setAds(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) return <h2 style={{ padding: 20 }}>Carregando ads...</h2>;

  return (
    <div style={{
      padding: 20,
      fontFamily: "Arial",
      background: "#0f0f0f",
      minHeight: "100vh",
      color: "#fff"
    }}>
      <h1>📊 AdSpy Dashboard</h1>

      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))",
        gap: 20,
        marginTop: 20
      }}>
        {ads.map((ad, index) => (
          <div key={index} style={{
            background: "#1c1c1c",
            padding: 15,
            borderRadius: 10
          }}>
            <h3>{ad.page_name}</h3>
            <p>{ad.headline}</p>
            <p style={{ opacity: 0.7 }}>{ad.body}</p>

            <div style={{
              marginTop: 10,
              fontSize: 12,
              color: "#aaa"
            }}>
              {ad.media_type}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}