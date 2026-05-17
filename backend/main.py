/* backend/routes/ads.py */
from fastapi import APIRouter, Depends, HTTPException
from models import Ad
from crud import get_ads
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/ads",
    tags=["ads"],
)

@router.get("/", response_model=List[Ad])
async def read_ads(skip: int = 0, limit: int = 100, db: Session = Depends(lambda: dependencias_db())):
    ads = get_ads(db, skip=skip, limit=limit)
    return ads

/* backend/models.py */
from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Ad(Base):
    __tablename__ = "ads"
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, index=True)
    thumbnail_url = Column(String, index=True)
    headline = Column(String, index=True)
    main_text = Column(String)
    cta = Column(String, index=True)
    active_since = Column(DateTime)
    page_name = Column(String, index=True)
    variant_count = Column(Integer)
    collected_at = Column(DateTime, default=datetime.utcnow)
    country = Column(String, index=True)
    category = Column(String, index=True)
    creative_strength_score = Column(Float)

/* backend/schemas.py */
from pydantic import BaseModel

class AdBase(BaseModel):
    headline: str
    main_text: str
    cta: str
    active_since: datetime.datetime
    page_name: str
    variant_count: int
    country: str
    category: str
    creative_strength_score: float = None

/* backend/crud.py */
from sqlalchemy.orm import Session
from models import Ad

def get_ads(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Ad).offset(skip).limit(limit).all()

/* backend/main.py */
from fastapi import FastAPI
from routes import ads

app = FastAPI()
app.include_router(ads.router)

/* backend/dependencias_db.py */
from fastapi import Depends
from sqlalchemy.orm import Session
from database import session_local, engine

from . import crud

def dependencias_db() -> Session:
    ctx = session_local.begin()
    db = Session(local_ctx=ctx)
    try:
        yield db
    finally:
        db.close()

/* backend/README.md */
# LATAM Creative Intelligence - Backend

## Overview
This repository contains the backend for the LATAM Creative Intelligence platform. It provides a FastAPI service with endpoints to manage ads data collected from Meta Ads Library and other sources. The system is built with Python, FastAPI, and PostgreSQL via Prisma ORM.

## Architecture
- **Routes**: `/ads` for CRUD operations on ad creative data.
- **Models**: `Ad` stores creative details and analysis scores.
- **CRUD**: Simple read endpoint to fetch ads.
- **Database**: PostgreSQL configured via `dependencias_db`.
- **Docker**: Ready for containerization.

## Setup
```bash
# Install dependencies
pip install fastapi uvicorn sqlalchemy[postgresql] prisma dotenv

# Run the app locally
uvicorn main:app --reload
```

## Deployment
Deploy to Railway, Render, or any containerized environment.

## License
MIT
