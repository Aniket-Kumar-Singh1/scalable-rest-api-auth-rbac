"""
Database engine, session factory, and declarative Base.

- Reads DATABASE_URL from settings.
- Exposes `engine`, `SessionLocal`, `get_db()`, and `Base`.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # verify connections before handing them out
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    FastAPI dependency — yields a DB session and closes it after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()