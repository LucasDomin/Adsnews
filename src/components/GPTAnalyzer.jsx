import { useState } from "react";
import { analyzeAd } from "../api/api";

export default function GPTAnalyzer({ ad }) {
  const [result, setResult] = useState(null);

  async function handleAnalyze() {
    const res = await analyzeAd({
      headline: ad.headline,
      body: ad.body,
      cta: ad.cta,
    });

    setResult(res.data);
  }

  return (
    <div style={{ marginTop: 10 }}>
      <button onClick={handleAnalyze}>
        🤖 Analisar com GPT
      </button>

      {result && (
        <pre style={{ whiteSpace: "pre-wrap" }}>
          {JSON.stringify(result.analysis, null, 2)}
        </pre>
      )}
    </div>
  );
}