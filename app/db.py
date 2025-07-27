from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
import os

from dotenv import load_dotenv
load_dotenv()

# Load DB connection values from environment
db_user = os.getenv("DB_USER")
db_pass = quote_plus(os.getenv("DB_PASSWORD"))
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

db_uri = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

# 1. ✅ LangChain SQLDatabase (for generating SQL)
langchain_db = SQLDatabase.from_uri(db_uri)

# 2. ✅ SQLAlchemy Engine + Session (for executing SQL)
engine = create_engine(db_uri)
SessionLocal = sessionmaker(bind=engine)

# Optional: Dependency for FastAPI routes
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
