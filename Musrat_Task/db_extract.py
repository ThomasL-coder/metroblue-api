from sqlalchemy import create_engine
import pandas as pd


DB_HOST = "127.0.0.1"
DB_PORT = "3306"
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "metroblue"

def get_engine():
    connection_string = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    return create_engine(connection_string)


def extract_lead_data() -> pd.DataFrame:
    """
    Extract lead data joined with clients and referrals.
    Target can be derived from stage='Paid' or client existence.
    """
    query = """
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

    engine = get_engine()
    df = pd.read_sql(query, engine)
    return df


if __name__ == "__main__":
    df = extract_lead_data()
    print(df.head())
    print(f"Rows: {len(df)}")