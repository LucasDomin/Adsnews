from sqlalchemy import Column, Integer, String, Text, Float
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

    score = Column(Float, default=0)