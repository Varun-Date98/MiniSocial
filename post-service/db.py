# post-service/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import POST_DB_URL

engine = create_engine(POST_DB_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
