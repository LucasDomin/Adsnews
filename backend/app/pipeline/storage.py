import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from datetime import datetime
from app.db.db import SessionLocal
from app.db.models import Ad

def save_ads(ads: list):
    db = SessionLocal()
    saved = 0
    updated = 0
    try:
        for ad in ads:
            ad_id = str(ad.get("ad_id", "")).strip()
            if not ad_id:
                continue
            fields = {
                "page_name":           ad.get("page_name", ""),
                "headline":            ad.get("headline", ""),
                "body":                ad.get("body", ""),
                "cta":                 ad.get("cta", ""),
                "media_type":          ad.get("media_type", ""),
                "image_url":           ad.get("image_url") or ad.get("video_preview", ""),
                "score":               ad.get("score", 0.0),
                "urgency_score":       ad.get("urgency_score", 0),
                "trust_score":         ad.get("trust_score", 0),
                "speed_score":         ad.get("speed_score", 0),
                "accessibility_score": ad.get("accessibility_score", 0),
                "analyzed_at":         ad.get("analyzed_at", datetime.utcnow()),
            }
            existing = db.query(Ad).filter(Ad.ad_id == ad_id).first()
            if existing:
                for k, v in fields.items():
                    setattr(existing, k, v)
                updated += 1
            else:
                db.add(Ad(ad_id=ad_id, **fields))
                saved += 1
        db.commit()
        print(f"[STORAGE] {saved} novos, {updated} atualizados.")
    except Exception as e:
        db.rollback()
        print(f"[STORAGE] Erro: {e}")
    finally:
        db.close()
