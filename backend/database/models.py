from sqlalchemy import Column, Integer, String, Text, JSON

from database.db import Base


class Ad(Base):

    __tablename__ = "ads"

    id = Column(Integer, primary_key=True, index=True)

    ad_id = Column(String, unique=True, index=True)

    page_name = Column(String)

    headline = Column(Text)

    body = Column(Text)

    cta = Column(String)

    cta_link = Column(Text)

    media_type = Column(String)

    image_url = Column(Text)

    video_preview = Column(Text)

    ocr_text = Column(Text)

    analysis = Column(JSON)