"""
app/pipeline/storage.py — salva ads no banco com análise automática.
"""
import sys, os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app.db.db import SessionLocal
from app.db.models import Ad
from analyzers.creative_analyzer import analyze_creative_text


def compute_score(a: dict) -> float:
    return float(
        min(a["urgency_score"] * 15, 30) +
        min(a["trust_score"] * 20, 30) +
        min(a["speed_score"] * 15, 20) +
        min(a["accessibility_score"] * 10, 20)
    )


def save_ads(ads: list[dict]):
    db = SessionLocal()
    saved = 0
    skipped = 0

    for ad in ads:
        try:
            # Análise automática do criativo
            text_parts = [
                ad.get("headline", ""),
                ad.get("body", ""),
                ad.get("cta", ""),
            ]
            full_text = " ".join(p for p in text_parts if p).strip()

            analysis = analyze_creative_text(full_text) if full_text else {}
            score = compute_score(analysis) if analysis else 0.0

            ad_id = ad.get("ad_id") or ad.get("id")
            if not ad_id:
                skipped += 1
                continue

            existing = db.query(Ad).filter(Ad.ad_id == str(ad_id)).first()

            if existing:
                # Atualiza se já existe
                existing.score = score
                existing.urgency_score = analysis.get("urgency_score", 0)
                existing.trust_score = analysis.get("trust_score", 0)
                existing.speed_score = analysis.get("speed_score", 0)
                existing.accessibility_score = analysis.get("accessibility_score", 0)
                existing.analyzed_at = datetime.utcnow()
            else:
                new_ad = Ad(
                    ad_id=str(ad_id),
                    page_name=ad.get("page_name", ""),
                    headline=ad.get("headline", ""),
                    body=ad.get("body", ""),
                    cta=ad.get("cta", ""),
                    media_type=ad.get("media_type", ""),
                    image_url=ad.get("image_url", ""),
                    score=score,
                    urgency_score=analysis.get("urgency_score", 0),
                    trust_score=analysis.get("trust_score", 0),
                    speed_score=analysis.get("speed_score", 0),
                    accessibility_score=analysis.get("accessibility_score", 0),
                    analyzed_at=datetime.utcnow(),
                )
                db.add(new_ad)
                saved += 1

        except Exception as e:
            print(f"[STORAGE] Erro ao salvar ad {ad.get('ad_id')}: {e}")
            continue

    db.commit()
    db.close()
    print(f"[STORAGE] ✅ {saved} novos ads salvos, {skipped} ignorados.")