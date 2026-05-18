from fastapi import APIRouter
from app.db.db import SessionLocal
from app.db.models import Ad

router = APIRouter()


@router.get("/")
def get_ads():

    db = SessionLocal()

    ads = db.query(Ad).order_by(Ad.id.desc()).limit(50).all()

    return [
        {
            "ad_id": a.ad_id,
            "headline": a.headline,
            "page_name": a.page_name,
            "media_type": a.media_type,
            "score": a.score,
        }
        for a in ads
    ]