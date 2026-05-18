from app.db.db import SessionLocal
from app.db.models import Ad


def save_ads(ads: list):
    db = SessionLocal()

    try:
        for ad in ads:

            existing = db.query(Ad).filter(Ad.ad_id == ad["ad_id"]).first()

            if existing:
                for k, v in ad.items():
                    setattr(existing, k, v)
            else:
                db.add(Ad(**ad))

        db.commit()

    except Exception as e:
        db.rollback()
        print("[STORAGE ERROR]", e)

    finally:
        db.close()