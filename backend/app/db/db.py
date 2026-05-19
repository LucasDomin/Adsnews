import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:Do30503!@localhost:5432/adintel")

engine = create_engine(
    DATABASE_URL,
    pool_size=2,
    max_overflow=3,
    pool_timeout=30,
    pool_pre_ping=True,
    pool_recycle=300,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
