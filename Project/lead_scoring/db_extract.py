
import pandas as pd
from sqlalchemy import text

from app.db import engine


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


def extract_lead_data(query: str = DEFAULT_QUERY) -> pd.DataFrame:
    with engine.connect() as conn:
        return pd.read_sql(text(query), conn)
