import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL is not set. Example: mysql+pymysql://user:pass@host:3306/dbname"
    )

if not DATABASE_URL.startswith("mysql+pymysql://"):
    raise ValueError("DATABASE_URL must start with mysql+pymysql://")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)
