from fastapi import APIRouter
from app.db.db import SessionLocal
from app.db.models import Ad

router = APIRouter()


@router.get("/summary")
def summary():

    db = SessionLocal()
    ads = db.query(Ad).all()

    total = len(ads)

    media = {}
    pages = {}

    for a in ads:
        media[a.media_type] = media.get(a.media_type, 0) + 1
        pages[a.page_name] = pages.get(a.page_name, 0) + 1

    top_pages = sorted(pages.items(), key=lambda x: x[1], reverse=True)[:10]

    return {
        "total_ads": total,
        "media_distribution": media,
        "top_pages": top_pages
    }