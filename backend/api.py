from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db import SessionLocal
from database.models import Ad

app = FastAPI(title="Ad Intelligence API")

# CORS (ESSENCIAL pro frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = SessionLocal()


@app.get("/")
def root():
    return {"status": "ok", "message": "Ad Intelligence API running"}


# =========================
# ADS
# =========================
@app.get("/ads")
def get_ads(limit: int = 20, country: str = None, media_type: str = None):

    query = db.query(Ad)

    if country:
        query = query.filter(Ad.page_name.contains(country))

    if media_type:
        query = query.filter(Ad.media_type == media_type)

    ads = query.limit(limit).all()

    return [
        {
            "ad_id": a.ad_id,
            "page_name": a.page_name,
            "headline": a.headline,
            "body": a.body,
            "cta": a.cta,
            "cta_link": a.cta_link,
            "media_type": a.media_type,
            "image_url": a.image_url,
            "ocr_text": a.ocr_text
        }
        for a in ads
    ]


@app.get("/ads/{ad_id}")
def get_ad(ad_id: str):

    ad = db.query(Ad).filter(Ad.ad_id == ad_id).first()

    if not ad:
        return {"error": "not found"}

    return ad.__dict__


# =========================
# INSIGHTS (SEU DIFERENCIAL)
# =========================
@app.get("/insights/market")
def market_insights():

    ads = db.query(Ad).all()

    media = {}
    ctas = {}
    pages = {}

    for a in ads:

        media[a.media_type] = media.get(a.media_type, 0) + 1
        ctas[a.cta] = ctas.get(a.cta, 0) + 1
        pages[a.page_name] = pages.get(a.page_name, 0) + 1

    return {
        "total_ads": len(ads),
        "media_distribution": media,
        "top_ctas": sorted(ctas.items(), key=lambda x: x[1], reverse=True)[:10],
        "top_pages": sorted(pages.items(), key=lambda x: x[1], reverse=True)[:10],
    }