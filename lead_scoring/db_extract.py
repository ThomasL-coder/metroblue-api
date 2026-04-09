import os
import pandas as pd
from sqlalchemy import create_engine


DEFAULT_QUERY = """
SELECT
    l.id,
    l.name,
    l.source,
    l.course_service,
    l.gender,
    l.location,
    l.phone,
    l.stage,
    l.referral_id,
    l.notes,
    l.created_at,
    l.contacted_at,
    r.name AS referral_name,
    c.id AS client_id
FROM leads l
LEFT JOIN referrals r ON l.referral_id = r.id
LEFT JOIN clients c ON l.id = c.lead_id
"""



def get_engine():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError(
            "DATABASE_URL is not set. Example: mysql+pymysql://user:pass@host:3306/dbname"
        )
    return create_engine(database_url)



def extract_lead_data(query: str = DEFAULT_QUERY) -> pd.DataFrame:
    engine = get_engine()
    return pd.read_sql(query, engine)


if __name__ == "__main__":
    df = extract_lead_data()
    print(df.head())
    print(f"Rows: {len(df)}")
