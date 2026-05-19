import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

def run_pipeline():
    print("🚀 PIPELINE START")

    # 1. Scraper — coleta HTML do Facebook Ads Library
    from app.services.scraper_service import run_scraper
    html = run_scraper()
    if not html:
        print("❌ Scraper retornou HTML vazio")
        return False

    # 2. Parser — extrai e normaliza ads do HTML
    from parsers.parser_pipeline import extract_ads_from_html
    from parsers.normalizer import normalize_ad
    raw_ads = extract_ads_from_html(html)
    print(f"[PIPELINE] {len(raw_ads)} ads extraídos")

    normalized = []
    for ad in raw_ads:
        try:
            normalized.append(normalize_ad(ad))
        except Exception as e:
            print(f"[PIPELINE] Erro ao normalizar: {e}")

    # Remove duplicados
    unique = {a["ad_id"]: a for a in normalized if a.get("ad_id")}
    ads = list(unique.values())
    print(f"[PIPELINE] {len(ads)} ads únicos")

    # 3. Análise automática de cada criativo
    from analyzers.creative_analyzer import analyze_creative_text
    from datetime import datetime

    def compute_score(a):
        return float(
            min(a["urgency_score"] * 15, 30) +
            min(a["trust_score"] * 20, 30) +
            min(a["speed_score"] * 15, 20) +
            min(a["accessibility_score"] * 10, 20)
        )

    for ad in ads:
        text = " ".join(filter(None, [
            ad.get("headline", ""),
            ad.get("body", ""),
            ad.get("cta", ""),
        ]))
        if text.strip():
            analysis = analyze_creative_text(text)
            ad["score"] = compute_score(analysis)
            ad["urgency_score"] = analysis["urgency_score"]
            ad["trust_score"] = analysis["trust_score"]
            ad["speed_score"] = analysis["speed_score"]
            ad["accessibility_score"] = analysis["accessibility_score"]
            ad["analyzed_at"] = datetime.utcnow()

    # 4. Storage — salva no banco (Render)
    from app.pipeline.storage import save_ads
    save_ads(ads)

    print("✅ PIPELINE DONE")
    return True