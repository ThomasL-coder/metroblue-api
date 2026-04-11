
import os
from sqlalchemy import create_engine

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL is not set. Example: mysql+pymysql://user:pass@host:3306/dbname"
    )

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)
