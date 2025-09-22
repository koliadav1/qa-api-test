from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

if os.getenv("TESTING") != "True":
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:1@db:5432/qa_db")

    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()