from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv(override=True)

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_ROOT_USER = os.getenv("DB_ROOT_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

DATABASE_URL_ROOT = f"mysql+pymysql://{DB_ROOT_USER}:{DB_PASSWORD}@{DB_HOST}"
DATABASE_URL = f"mysql+pymysql://{DB_ROOT_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine_root = create_engine(DATABASE_URL_ROOT)
with engine_root.connect() as connection:
    connection.execute(text(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`"))
    
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()