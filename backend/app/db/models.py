from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from app.db.db import Base


class Ad(Base):
    __tablename__ = "ads"

    id = Column(Integer, primary_key=True)
    ad_id = Column(String, unique=True, index=True)
    page_name = Column(String)
    headline = Column(Text)
    body = Column(Text)
    cta = Column(String)
    media_type = Column(String)
    image_url = Column(Text)

    # Scores calculados automaticamente no pipeline
    score = Column(Float, default=0)
    urgency_score = Column(Integer, default=0)
    trust_score = Column(Integer, default=0)
    speed_score = Column(Integer, default=0)
    accessibility_score = Column(Integer, default=0)
    analyzed_at = Column(DateTime, nullable=True)