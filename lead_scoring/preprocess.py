from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

TOP_N_LOCATIONS = 10
NUMERIC_FEATURES = [
    "gender_encoded",
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
CATEGORICAL_FEATURES = ["source", "course_service", "location_grouped"]
FEATURE_COLUMNS = CATEGORICAL_FEATURES + NUMERIC_FEATURES



def clean_gender(value: object) -> int:
    if pd.isna(value):
        return -1
    text = str(value).strip().lower()
    if text == "male":
        return 1
    if text == "female":
        return 0
    return -1



def prepare_dataframe(df: pd.DataFrame, top_locations: list[str] | None = None) -> pd.DataFrame:
    df = df.copy()

    for col in [
        "source",
        "course_service",
        "gender",
        "location",
        "phone",
        "stage",
        "referral_id",
        "notes",
        "created_at",
        "contacted_at",
    ]:
        if col not in df.columns:
            df[col] = np.nan

    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
    df["contacted_at"] = pd.to_datetime(df["contacted_at"], errors="coerce")
    now = pd.Timestamp.now().normalize()

    if "stage" in df.columns:
        df["converted"] = np.where(df["stage"].fillna("").str.lower() == "paid", 1, 0)

    df["has_location"] = df["location"].notna().astype(int)
    df["has_phone"] = df["phone"].notna().astype(int)
    df["has_referral"] = df["referral_id"].notna().astype(int)
    df["has_notes"] = df["notes"].notna().astype(int)
    df["notes_length"] = df["notes"].fillna("").astype(str).str.len()

    df["days_since_created"] = (now - df["created_at"]).dt.days.fillna(-1)
    df["days_since_contacted"] = (now - df["contacted_at"]).dt.days.fillna(-1)
    df["contact_speed"] = (df["contacted_at"] - df["created_at"]).dt.days.fillna(-1)

    df["created_day_of_week"] = df["created_at"].dt.dayofweek.fillna(-1)
    df["created_month"] = df["created_at"].dt.month.fillna(-1)

    referral_counts = df["referral_id"].value_counts(dropna=True).to_dict()
    df["referral_lead_count"] = df["referral_id"].map(referral_counts).fillna(0)

    df["gender_encoded"] = df["gender"].apply(clean_gender)

    df["location"] = df["location"].fillna("Unknown")
    if top_locations is None:
        top_locations = (
            df["location"].value_counts().head(TOP_N_LOCATIONS).index.tolist()
        )
    df["location_grouped"] = df["location"].apply(
        lambda x: x if x in set(top_locations) else "Other"
    )

    df["source"] = df["source"].fillna("Unknown")
    df["course_service"] = df["course_service"].fillna("Unknown")

    for col in NUMERIC_FEATURES:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype(float)

    return df



def build_training_frame(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series, dict]:
    prepared = prepare_dataframe(df)
    X = prepared[FEATURE_COLUMNS].copy()
    y = prepared["converted"].astype(int)
    metadata = {
        "top_locations": (
            prepared["location"]
            .value_counts()
            .head(TOP_N_LOCATIONS)
            .index.tolist()
        )
    }
    return X, y, metadata



def build_preprocessor() -> ColumnTransformer:
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="constant", fill_value=-1.0)),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="constant", fill_value="Unknown")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, NUMERIC_FEATURES),
            ("cat", categorical_pipeline, CATEGORICAL_FEATURES),
        ]
    )



def transform_single_lead(lead_dict: dict, top_locations: list[str] | None = None) -> pd.DataFrame:
    df = pd.DataFrame([lead_dict])
    prepared = prepare_dataframe(df, top_locations=top_locations)
    return prepared[FEATURE_COLUMNS].copy()
