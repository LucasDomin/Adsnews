from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os

from openai import OpenAI

from database.db import SessionLocal
from database.models import Ad

# -----------------------
# INIT OPENAI CLIENT
# -----------------------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(title="Ad Intelligence API")

# -----------------------
# CORS
# -----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# HEALTH CHECK
# -----------------------
@app.get("/")
def health():
    return {
        "status": "ok",
        "message": "Ad Intelligence API running"
    }

# -----------------------
# ADS
# -----------------------
@app.get("/ads")
def get_ads(limit: int = 100):
    db = SessionLocal()
    ads = db.query(Ad).order_by(Ad.id.desc()).limit(limit).all()

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
            "video_preview": a.video_preview,
            "country": getattr(a, "country", None),
        }
        for a in ads
    ]

# -----------------------
# INSIGHTS
# -----------------------
@app.get("/insights/summary")
def insights():
    db = SessionLocal()
    ads = db.query(Ad).all()

    media = {}
    pages = {}

    for a in ads:
        media[a.media_type] = media.get(a.media_type, 0) + 1
        pages[a.page_name] = pages.get(a.page_name, 0) + 1

    return {
        "total_ads": len(ads),
        "media_distribution": media,
        "top_pages": sorted(pages.items(), key=lambda x: x[1], reverse=True)[:10]
    }

# -----------------------
# INPUT MODEL
# -----------------------
class AdInput(BaseModel):
    headline: Optional[str] = None
    body: Optional[str] = None
    cta: Optional[str] = None

# -----------------------
# GPT FUNCTION (AQUI ESTÁ O QUE VOCÊ PEDIU)
# -----------------------
def call_gpt_api(payload):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert in marketing, ads analysis and conversion copywriting. "
                        "Analyze ads and return structured insights."
                    )
                },
                {
                    "role": "user",
                    "content": f"""
Analyze this ad:

Headline: {payload.get('headline')}
Body: {payload.get('body')}
CTA: {payload.get('cta')}

Return:
- emotion (urgency, trust, curiosity, etc)
- conversion_score (0-10)
- strengths
- weaknesses
- improvement suggestions
"""
                }
            ],
            temperature=0.7
        )

        return {
            "result": response.choices[0].message.content
        }

    except Exception as e:
        return {
            "error": str(e)
        }

# -----------------------
# GPT ANALYZE ENDPOINT
# -----------------------
@app.post("/ai/analyze-ad")
def analyze_ad(data: AdInput):

    payload = {
        "headline": data.headline or "",
        "body": data.body or "",
        "cta": data.cta or ""
    }

    return call_gpt_api(payload)

# -----------------------
# OPTIONAL: GENERATE AD
# -----------------------
@app.post("/ai/generate-ad")
def generate_ad(data: dict):
    return call_gpt_api(data)