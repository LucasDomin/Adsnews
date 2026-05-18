import { useEffect, useState } from "react";

export default function Dashboard() {
  const [ads, setAds] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/ads")
      .then(res => res.json())
      .then(data => {
        setAds(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  const filtered = ads.filter(ad =>
    (ad.page_name || "").toLowerCase().includes(search.toLowerCase()) ||
    (ad.headline || "").toLowerCase().includes(search.toLowerCase()) ||
    (ad.body || "").toLowerCase().includes(search.toLowerCase())
  );

  if (loading) {
    return (
      <div style={styles.loading}>
        🔄 Carregando Ads...
      </div>
    );
  }

  return (
    <div style={styles.container}>
      
      {/* HEADER */}
      <div style={styles.header}>
        <h1 style={styles.title}>📊 AdSpy BigSpy Dashboard</h1>

        <input
          style={styles.search}
          placeholder="Buscar anúncios, páginas, headlines..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />

        <div style={styles.stats}>
          Total: {filtered.length} anúncios
        </div>
      </div>

      {/* GRID */}
      <div style={styles.grid}>
        {filtered.map((ad, i) => (
          <div key={i} style={styles.card}>
            
            <div style={styles.page}>
              🏢 {ad.page_name}
            </div>

            <h3 style={styles.headline}>
              {ad.headline}
            </h3>

            <p style={styles.body}>
              {ad.body}
            </p>

            <div style={styles.footer}>
              <span>🎯 {ad.cta}</span>
              <span>📦 {ad.media_type}</span>
            </div>

          </div>
        ))}
      </div>

    </div>
  );
}

const styles = {
  container: {
    background: "#0f0f0f",
    minHeight: "100vh",
    padding: 20,
    color: "#fff",
    fontFamily: "Arial"
  },

  header: {
    marginBottom: 20
  },

  title: {
    marginBottom: 10
  },

  search: {
    width: "100%",
    padding: 12,
    borderRadius: 8,
    border: "none",
    outline: "none",
    marginBottom: 10
  },

  stats: {
    opacity: 0.7,
    fontSize: 14
  },

  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(320px, 1fr))",
    gap: 15
  },

  card: {
    background: "#1c1c1c",
    padding: 15,
    borderRadius: 12,
    border: "1px solid #2a2a2a"
  },

  page: {
    fontSize: 12,
    opacity: 0.7,
    marginBottom: 5
  },

  headline: {
    marginBottom: 8
  },

  body: {
    fontSize: 14,
    opacity: 0.85
  },

  footer: {
    marginTop: 10,
    display: "flex",
    justifyContent: "space-between",
    fontSize: 12,
    opacity: 0.6
  },

  loading: {
    background: "#0f0f0f",
    color: "#fff",
    height: "100vh",
    display: "flex",
    alignItems: "center",
    justifyContent: "center"
  }
};