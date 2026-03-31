# Lead Scoring Module

## Overview
This module predicts whether a lead is likely to convert into a paying client.

## Files
- `db_extract.py` - pulls lead data from MySQL
- `preprocess.py` - feature engineering and transformation
- `train.py` - trains and saves the best model
- `predict.py` - scores a single lead
- `retrain.py` - retrains the model on latest data
- `tests/test_predict.py` - simple unit tests

## Features Used
- source
- course_service
- gender
- location
- has_phone
- has_referral
- referral_lead_count
- days_since_contacted
- days_since_created
- contact_speed
- notes_length
- has_notes
- created_day_of_week
- created_month

## Target
- converted = 1 if stage == "Paid"
- converted = 0 otherwise

## Run training
```bash
python train.py