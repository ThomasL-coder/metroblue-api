import pandas as pd
import numpy as np

TOP_N_LOCATIONS = 10


def build_features(df: pd.DataFrame):
    df = df.copy()

    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
    df["contacted_at"] = pd.to_datetime(df["contacted_at"], errors="coerce")
    now = pd.Timestamp.now()

    df["converted"] = np.where(df["stage"].fillna("").str.lower() == "paid", 1, 0)

    df["has_location"] = df["location"].notna().astype(int)
    df["has_phone"] = df["phone"].notna().astype(int)
    df["has_referral"] = df["referral_id"].notna().astype(int)
    df["has_notes"] = df["notes"].notna().astype(int)
    df["notes_length"] = df["notes"].fillna("").str.len()

    df["days_since_created"] = (now - df["created_at"]).dt.days.fillna(-1)
    df["days_since_contacted"] = (now - df["contacted_at"]).dt.days.fillna(-1)
    df["contact_speed"] = (df["contacted_at"] - df["created_at"]).dt.days.fillna(-1)

    df["created_day_of_week"] = df["created_at"].dt.dayofweek.fillna(-1)
    df["created_month"] = df["created_at"].dt.month.fillna(-1)

    referral_counts = df["referral_id"].value_counts(dropna=True).to_dict()
    df["referral_lead_count"] = df["referral_id"].map(referral_counts).fillna(0)

    df["gender"] = df["gender"].fillna("Unknown")
    df["gender"] = df["gender"].replace(
        {
            "Male": "Male",
            "Female": "Female",
            "male": "Male",
            "female": "Female"
        }
    )

    df["location"] = df["location"].fillna("Unknown")
    top_locations = df["location"].value_counts().head(TOP_N_LOCATIONS).index
    df["location_grouped"] = df["location"].apply(
        lambda x: x if x in top_locations else "Other"
    )

    df["source"] = df["source"].fillna("Unknown")
    df["course_service"] = df["course_service"].fillna("Unknown")

    feature_df = df[
        [
            "source",
            "course_service",
            "gender",
            "location_grouped",
            "has_location",
            "has_phone",
            "has_referral",
            "referral_lead_count",
            "days_since_contacted",
            "days_since_created",
            "contact_speed",
            "notes_length",
            "has_notes",
            "created_day_of_week",
            "created_month",
        ]
    ]

    X = pd.get_dummies(
        feature_df,
        columns=["source", "course_service", "gender", "location_grouped"],
        drop_first=False
    )

    y = df["converted"]

    return X, y, df


def transform_single_lead(lead_dict: dict, training_columns: list):
    df = pd.DataFrame([lead_dict])

    df["created_at"] = pd.to_datetime(df.get("created_at"), errors="coerce")
    df["contacted_at"] = pd.to_datetime(df.get("contacted_at"), errors="coerce")
    now = pd.Timestamp.now()

    df["has_location"] = df.get("location").notna().astype(int)
    df["has_phone"] = df.get("phone").notna().astype(int)
    df["has_referral"] = df.get("referral_id").notna().astype(int)
    df["has_notes"] = df.get("notes").notna().astype(int)
    df["notes_length"] = df.get("notes").fillna("").str.len()

    df["days_since_created"] = (now - df["created_at"]).dt.days.fillna(-1)
    df["days_since_contacted"] = (now - df["contacted_at"]).dt.days.fillna(-1)
    df["contact_speed"] = (df["contacted_at"] - df["created_at"]).dt.days.fillna(-1)

    df["created_day_of_week"] = df["created_at"].dt.dayofweek.fillna(-1)
    df["created_month"] = df["created_at"].dt.month.fillna(-1)

    df["referral_lead_count"] = 0

    df["source"] = df.get("source").fillna("Unknown")
    df["course_service"] = df.get("course_service").fillna("Unknown")
    df["gender"] = df.get("gender").fillna("Unknown")
    df["location_grouped"] = df.get("location").fillna("Unknown")

    feature_df = df[
        [
            "source",
            "course_service",
            "gender",
            "location_grouped",
            "has_location",
            "has_phone",
            "has_referral",
            "referral_lead_count",
            "days_since_contacted",
            "days_since_created",
            "contact_speed",
            "notes_length",
            "has_notes",
            "created_day_of_week",
            "created_month",
        ]
    ]

    X = pd.get_dummies(
        feature_df,
        columns=["source", "course_service", "gender", "location_grouped"],
        drop_first=False
    )

    for col in training_columns:
        if col not in X.columns:
            X[col] = 0

    X = X[training_columns]
    return X
