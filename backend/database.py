import os

import dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

dotenv.load_dotenv(override=True)

DATABASE_URL = os.getenv("DATABASE_URL")
SQLITE3_URL = "sqlite:///./shorten_url.db"

URL = DATABASE_URL or SQLITE3_URL

if URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
