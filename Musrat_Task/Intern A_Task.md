## MetroBlue Lead Scoring API ##

###  Intern A: Musrat 

**Project Overview**

This project is a standalone Python FastAPI service that predicts whether a lead will convert into a paying client. It uses machine learning models trained on lead data and exposes predictions through REST API endpoints.

The system supports:

- Lead conversion prediction (Lead Scoring)
- Model retraining
- API-based integration with external systems

-Objectives
- Build a machine learning model to predict lead conversion
- Perform feature engineering on lead data
- Evaluate multiple models and select the best one
- Deploy the model using FastAPI
- Provide real-time predictions via API

*Tech Stack*
- Python
- Pandas, NumPy
- Scikit-learn
- SQLAlchemy / PyMySQL
- FastAPI
- Uvicorn
- Pytest

**Project Structure**

lead_score_API/

│

├── main.py                # FastAPI app

├── train.py               # Model training

├── predict.py             # Prediction logic

├── retrain.py             # Retraining script

├── preprocess.py          # Feature engineering

├── db_extract.py          # Data extraction

│
├── models/

│   │ ├── lead_model.pkl

│  │  └── training_columns.pkl


├── tests/

│  │  └── test_predict.py


├── requirements.txt

└── README.md


### Weekly Tasks

**Week 1 – Data Exploration & Feature Engineering**
-Extracted data from database / CSV
-Performed exploratory data analysis
-Defined target variable (converted vs not converted)
-Built feature engineering pipeline

*Output:*

- Data extraction script
- Feature engineering pipeline
-Clean dataset

** Week 2 – Model Training & Evaluation **
- Trained Logistic Regression and Random Forest models
- Evaluated using accuracy, precision, recall, F1-score
- Handled small dataset and class imbalance
- Selected best model (Random Forest)

*Output:*

- Trained models
- Evaluation metrics
-  Saved model (.pkl)

**Week 3 – Model Deployment & Testing**
- Implemented prediction function (score_lead)
- Built retraining script
- Created unit tests (pytest)
- Developed FastAPI endpoints
- Tested API in browser (Swagger UI)

*Output:*

- Working API (/api/leads/score)
- Prediction system
- Unit tests passed
- Retraining pipeline

 Model Details
- Target Variable
- converted = 1 if lead stage is Paid
- converted = 0 otherwise

Models Used
- Logistic Regression
- Random Forest (selected model)
Evaluation Metrics (Sample)
Accuracy: 0.60
Precision: 0.50
Recall: 0.50
F1 Score: 0.50

### How to Run (First Time Setup) ###
Create virtual environment
-> python -m venv venv

Activate environment
-> venv\Scripts\activate

Install dependencies
-> pip install -r requirements.txt

Train model 
-> python train.py

 Run API server
->  python -m uvicorn main:app --reload


**API Usage**

Open in browser:

- http://127.0.0.1:8000/docs

Endpoint: Score Lead

- POST /api/leads/score

Request:
{
  "name": Musrat",
  
  "source": "Github",
  
  "course_service": "Python",
  
  "gender": "Female",
  
  "location": "Darwin",
  
  "created_at": "2026-03-20",
  
  "contacted_at": "2026-03-21",
  
  "referral_id": 2,
  
  "notes": "Interested",
  
  "phone": "0400000000"
}

Response:
{
  "score": 0.3,
  
  "label": "Warm",
  
  "top_factors": 
  
  [

   "has_referral",

    "has_notes",
    
    "has_phone"
  ]
}

*Testing*
Run unit tests:
-> pytest


*Retraining*
-> python retrain.py
