import { useEffect, useState } from "react";
import AdCard from "../components/AdCard";
import { getAds, getSummary } from "../api/api";

export default function Dashboard() {
  const [ads, setAds] = useState([]);
  const [summary, setSummary] = useState(null);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getAds(), getSummary()])
      .then(([adsRes, summaryRes]) => {
        setAds(adsRes.data);
        setSummary(summaryRes.data);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const filtered = ads.filter(ad =>
    (ad.page_name || "").toLowerCase().includes(search.toLowerCase()) ||
    (ad.headline || "").toLowerCase().includes(search.toLowerCase()) ||
    (ad.body || "").toLowerCase().includes(search.toLowerCase())
  );

  if (loading) {
    return <div style={styles.loading}>🔄 Carregando Ads...</div>;
  }

  // Top media type
  const topMedia = summary?.media_distribution
    ? Object.entries(summary.media_distribution).sort((a, b) => b[1] - a[1])[0]
    : null;

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
      </div>

      {/* MÉTRICAS */}
      {summary && (
        <div style={styles.metricsRow}>
          <div style={styles.metricCard}>
            <div style={styles.metricValue}>{summary.total_ads}</div>
            <div style={styles.metricLabel}>Total de Anúncios</div>
          </div>

          <div style={styles.metricCard}>
            <div style={styles.metricValue}>
              {Object.keys(summary.media_distribution || {}).length}
            </div>
            <div style={styles.metricLabel}>Tipos de Mídia</div>
          </div>

          {topMedia && (
            <div style={styles.metricCard}>
              <div style={styles.metricValue}>{topMedia[0]}</div>
              <div style={styles.metricLabel}>Mídia Mais Comum ({topMedia[1]})</div>
            </div>
          )}

          <div style={styles.metricCard}>
            <div style={styles.metricValue}>
              {(summary.top_pages || []).length}
            </div>
            <div style={styles.metricLabel}>Top Pages Rastreadas</div>
          </div>
        </div>
      )}

      {/* TOP PAGES */}
      {summary?.top_pages?.length > 0 && (
        <div style={styles.section}>
          <h2 style={styles.sectionTitle}>🏆 Top Páginas</h2>
          <div style={styles.topPagesRow}>
            {summary.top_pages.map(([page, count], i) => (
              <div key={i} style={styles.pageChip}>
                <span style={styles.pageRank}>#{i + 1}</span>
                <span style={styles.pageName}>{page || "—"}</span>
                <span style={styles.pageCount}>{count} ads</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* DISTRIBUIÇÃO DE MÍDIA */}
      {summary?.media_distribution && (
        <div style={styles.section}>
          <h2 style={styles.sectionTitle}>📦 Distribuição por Mídia</h2>
          <div style={styles.topPagesRow}>
            {Object.entries(summary.media_distribution).map(([type, count], i) => (
              <div key={i} style={{ ...styles.pageChip, background: "#1a2a1a" }}>
                <span style={styles.pageName}>{type || "desconhecido"}</span>
                <span style={styles.pageCount}>{count}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* STATS BAR */}
      <div style={styles.statsBar}>
        Exibindo {filtered.length} de {ads.length} anúncios
      </div>

      {/* GRID DE ADS */}
      <div style={styles.grid}>
        {filtered.map((ad, i) => (
          <AdCard key={ad.ad_id || i} ad={ad} />
        ))}
      </div>

    </div>
  );
}

const styles = {
  container: {
    background: "#0f0f0f",
    minHeight: "100vh",
    padding: 24,
    color: "#fff",
    fontFamily: "'Segoe UI', sans-serif",
  },
  header: {
    marginBottom: 24,
  },
  title: {
    fontSize: 28,
    fontWeight: 700,
    marginBottom: 12,
    letterSpacing: "-0.5px",
  },
  search: {
    width: "100%",
    padding: "12px 16px",
    borderRadius: 8,
    border: "1px solid #333",
    background: "#1c1c1c",
    color: "#fff",
    fontSize: 14,
    outline: "none",
    boxSizing: "border-box",
  },
  metricsRow: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(180px, 1fr))",
    gap: 12,
    marginBottom: 24,
  },
  metricCard: {
    background: "#1c1c1c",
    border: "1px solid #2a2a2a",
    borderRadius: 10,
    padding: "16px 20px",
    textAlign: "center",
  },
  metricValue: {
    fontSize: 28,
    fontWeight: 700,
    color: "#4ade80",
    lineHeight: 1.2,
  },
  metricLabel: {
    fontSize: 12,
    color: "#888",
    marginTop: 4,
  },
  section: {
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: 600,
    marginBottom: 10,
    color: "#ccc",
  },
  topPagesRow: {
    display: "flex",
    flexWrap: "wrap",
    gap: 8,
  },
  pageChip: {
    background: "#1c1c1c",
    border: "1px solid #2a2a2a",
    borderRadius: 20,
    padding: "6px 14px",
    display: "flex",
    alignItems: "center",
    gap: 8,
    fontSize: 13,
  },
  pageRank: {
    color: "#4ade80",
    fontWeight: 700,
    fontSize: 11,
  },
  pageName: {
    color: "#ddd",
  },
  pageCount: {
    color: "#666",
    fontSize: 11,
  },
  statsBar: {
    fontSize: 13,
    color: "#666",
    marginBottom: 16,
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(320px, 1fr))",
    gap: 16,
  },
  loading: {
    background: "#0f0f0f",
    color: "#fff",
    height: "100vh",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: 18,
  },
};