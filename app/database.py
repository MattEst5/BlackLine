from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from app.core.settings import settings  

DATABASE_URL = settings.DATABASE_URL

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

from app.models import incident, user, department

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)