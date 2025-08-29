from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///lib/db/app.db"

engine = create_engine(DATABASE_URL, echo=True)  # echo=True shows SQL queries

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)

def get_session():
    """Return a new SQLAlchemy session."""
    return SessionLocal()


def init_db():
    """Create all tables (runs only if they don’t already exist)."""
    from lib.db import models 
    Base.metadata.create_all(bind=engine)
