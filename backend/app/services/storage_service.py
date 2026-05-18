from sqlalchemy.orm import Session
from database.db import SessionLocal
from database.models import Ad


def run_storage(ads: list):
    print("[STORAGE] salvando no banco...")

    db: Session = SessionLocal()

    inserted = 0
    updated = 0

    try:
        for ad in ads:

            existing = db.query(Ad).filter(Ad.ad_id == ad.get("ad_id")).first()

            if existing:
                # UPDATE (evita duplicar)
                for key, value in ad.items():
                    setattr(existing, key, value)

                updated += 1

            else:
                new_ad = Ad(**ad)
                db.add(new_ad)
                inserted += 1

        db.commit()

        print(f"[STORAGE] inseridos: {inserted}")
        print(f"[STORAGE] atualizados: {updated}")

        return True

    except Exception as e:
        db.rollback()
        print(f"[STORAGE ERROR] {e}")
        return False

    finally:
        db.close()