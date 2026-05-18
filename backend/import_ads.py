import json
from database.db import SessionLocal
from database.models import Ad

FILE_PATH = "data/normalized/ads_normalized.json"


def load_ads():
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_to_db():
    db = SessionLocal()
    ads = load_ads()

    inserted = 0
    skipped = 0

    for ad in ads:
        existing = db.query(Ad).filter(Ad.ad_id == ad["ad_id"]).first()

        if existing:
            skipped += 1
            continue

        new_ad = Ad(
            ad_id=ad.get("ad_id"),
            page_name=ad.get("page_name"),
            headline=ad.get("headline"),
            body=ad.get("body"),
            cta=ad.get("cta"),
            cta_link=ad.get("cta_link"),
            media_type=ad.get("media_type"),
            image_url=ad.get("image_url"),
            video_preview=ad.get("video_preview"),
            country=ad.get("country", None),
            ocr_text=ad.get("ocr_text", "")
        )

        db.add(new_ad)
        inserted += 1

    db.commit()
    db.close()

    print(f"[🔥 IMPORTAÇÃO FINALIZADA]")
    print(f"[+] Inseridos: {inserted}")
    print(f"[=] Ignorados (duplicados): {skipped}")


if __name__ == "__main__":
    save_to_db()