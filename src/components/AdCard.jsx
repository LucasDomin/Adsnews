import GPTAnalyzer from "./GPTAnalyzer";

export default function AdCard({ ad }) {
  return (
    <div style={{
      border: "1px solid #ddd",
      padding: 15,
      borderRadius: 10
    }}>
      <h3>{ad.page_name}</h3>

      <p><b>Headline:</b> {ad.headline}</p>
      <p><b>Body:</b> {ad.body}</p>
      <p><b>CTA:</b> {ad.cta}</p>

      {ad.image_url && (
        <img src={ad.image_url} style={{ width: "100%", borderRadius: 8 }} />
      )}

      <GPTAnalyzer ad={ad} />
    </div>
  );
}