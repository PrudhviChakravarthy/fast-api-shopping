from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv, find_dotenv
from sqlalchemy.ext.declarative import declarative_base
import os

load_dotenv(find_dotenv())
db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
db_tablename = os.getenv("DB_DATABASE")
db_host = os.getenv("DB_HOST")
schema_name = os.getenv("SCHEMA_NAME")
database = f"postgresql://{db_username}:{db_password}@{db_host}/{db_tablename}"
engine = create_engine(database,connect_args={"options":f"-csearch_path={schema_name}"})

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally :
        db.close()

