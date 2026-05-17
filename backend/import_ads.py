import json

from database.db import SessionLocal
from database.models import Ad


INPUT_FILE = "data/enriched_ads.json"

db = SessionLocal()


with open(INPUT_FILE, "r", encoding="utf-8") as f:
    ads = json.load(f)


inserted = 0

for item in ads:

    # evita duplicados
    exists = db.query(Ad).filter(
        Ad.ad_id == item.get("ad_id")
    ).first()

    if exists:
        continue

    ad = Ad(

        ad_id=item.get("ad_id"),
        page_name=item.get("page_name"),
        headline=item.get("headline"),
        body=item.get("body"),
        cta=item.get("cta"),
        cta_link=item.get("cta_link"),
        media_type=item.get("media_type"),
        image_url=item.get("image_url"),
        video_preview=item.get("video_preview"),
        ocr_text=item.get("ocr_text"),
        analysis=item.get("analysis")
    )

    db.add(ad)
    inserted += 1


db.commit()
db.close()

print(f"[🔥 IMPORTAÇÃO FINALIZADA 🔥] {inserted} novos ads inseridos")