from .database import SessionLocal
from typing import Generator

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
