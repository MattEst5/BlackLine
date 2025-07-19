from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()  

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("DATABASE_URL is not set in .env file.")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base = declarative_base()

from app.models import incident

Base.metadata.create_all(bind=engine)