
# **Lead Scoring API Project **

**Project Name:** MetroBlue ML Service
## **1. Introduction**

The purpose of this project is to develop a machine learning–based API that predicts whether a lead will convert into a paying customer. This helps businesses prioritise high-value leads, improve marketing efficiency, and increase conversion rates.
The system is built as a REST API using FastAPI and integrates a trained machine learning model for real-time predictions.

## **2. Project Objectives**

* Build a predictive model to classify leads as **converted (Paid) or not converted**
* Perform data analysis and feature engineering
* Develop an API to serve predictions
* Provide model insights and evaluation metrics
* Enable scalability and real-time usage

## **3. System Architecture**

The project follows a modular architecture:

### **Components**

* **Data Layer:** CSV / Database (Leads data)
* **ML Model:** Scikit-learn classification model
* **API Layer:** FastAPI
* **Client Interface:** Swagger UI (localhost:8000/docs)

### **Workflow**

1. Data is collected from database/CSV
2. Data preprocessing and feature engineering performed
3. Model is trained and saved
4. FastAPI loads model
5. User sends request → API returns prediction

### **Dataset Overview**

* Lead sources (Facebook, Google, Referral)
* Customer details (location, gender)
* Lead stages (Cold, Warm, Hot, Paid)

### **Target Variable**

* `converted = 1` → if stage = Paid
* `converted = 0` → otherwise

### **Feature Engineering**

* One-hot encoding for:

  * Source
  * Course/service
  * Location
* Binary features:

  * Gender encoding
  * Has phone
  * Has location
* Handling missing values

### **Algorithms Used**

* Logistic Regression
* Random Forest
* Decision Tree

### **Model Evaluation Metrics**

* Accuracy
* Precision
* Recall
* F1-score
* Confusion Matrix

### **Outcome**

* Best performing model selected based on F1-score and accuracy
* Model saved using `joblib`


## **6. API Development**

The machine learning model is deployed using FastAPI.

### **Available Endpoints**

#### **1. Health Check**

```
GET /health
```

Returns API status

#### **2. Predict Lead Conversion**

```
POST /predict-lead
```

Input:

```json
{
  "source": "Facebook",
  "location": "Darwin",
  "gender": "Male"
}
```

Output:

```json
{
  "prediction": 1,
  "probability": 0.87
}
```

#### **3. Model Information**

```
GET /lead-model-info
```

#### **4. Revenue Forecast (Optional)**

```
GET /revenue-forecast
```

## **7. Results**

* The model successfully predicts lead conversion with good accuracy
* Helps identify high-quality leads
* API responds in real-time
* Easy integration with frontend or CRM systems

## **8. Tools & Technologies**

* **Programming Language:** Python
* **Libraries:** pandas, scikit-learn, numpy
* **API Framework:** FastAPI
* **Model Storage:** joblib
* **Server:** Uvicorn
* **Version Control:** Git


## **9. Challenges Faced**

* Handling missing and inconsistent data
* Feature selection and encoding
* Model overfitting
* Environment setup issues (Python, dependencies)

# MetroBlue ML Project  
## Intern Roles & Responsibilities
Musrat : Intern A,
Gabino : Intern B,
Thomas: Intern C
---

##  Intern A — Lead Scoring Model & Pipeline  
**Focus:** Machine Learning model to predict lead conversion  

###  Key Responsibilities
- Set up Python environment (venv, required libraries)
- Extract data from database (leads, clients, referrals)
- Perform Exploratory Data Analysis (EDA)
  - Conversion rates  
  - Lead sources  
  - Stage distribution (Cold, Warm, Hot, Paid)  

### Target Variable
- `converted = 1` → Paid  
- `converted = 0` → Others  

###  Feature Engineering
- Encoding:
  - Source  
  - Location  
  - Service  
- Binary Features:
  - Gender  
  - Has phone  
  - Has location  

###  Model Training
- Logistic Regression  
- Random Forest  
- Decision Tree  

### Model Evaluation
- Accuracy  
- Precision  
- Recall  
- F1-score  

###  Final Deliverables
- Trained lead scoring model  
- Clean dataset & engineered features  
- Model evaluation report  



##  Intern B — Revenue Forecasting Model  
**Focus:** Predict future revenue based on lead conversions  

###  Key Responsibilities
- Prepare historical revenue data  
- Aggregate data:
  - Monthly revenue  
  - Conversion trends  
- Perform time-based analysis  

###  Forecasting Models
- Linear Regression  
- Time Series (ARIMA - optional)  

###  Predictions
- Forecast next 3–6 months revenue  

###  Evaluation
- Evaluate model performance  

###  Integration
- Integrate forecasting logic into backend  

###  Final Deliverables
- Revenue prediction model  
- Monthly forecast results  
- Model accuracy evaluation  



##  Intern C — API Development & Integration  
**Focus:** Build and expose ML models via API  

###  Key Responsibilities
- Set up FastAPI project structure  
- Load trained models (Intern A & B)  

###  API Endpoints
- `GET /health` → API status  
- `POST /predict-lead` → Lead conversion prediction  
- `GET /lead-model-info` → Model details  
- `GET /revenue-forecast` → Revenue prediction  

### API Features
- Input validation (JSON requests)  
- Structured JSON responses  
- API testing using Swagger (`/docs`)  
- Error handling and stability  

###  Final Deliverables
- Fully functional FastAPI service  
- Integrated ML models  
- API documentation (Swagger UI)  



##  How It All Works Together

- **Intern A** → Builds lead conversion prediction model  
- **Intern B** → Builds revenue forecasting model  
- **Intern C** → Integrates models into API  

###  Final Outcome
A complete ML-powered API that can:
- Predict lead conversion probability  
- Forecast future revenue  


POST /predict-lead → Lead conversion prediction
GET /lead-model-info → Model details
GET /revenue-forecast → Future revenue prediction
Handle input validation (JSON requests)
Return structured JSON responses
Test API using Swagger (/docs)
Ensure error handling and stability
Final Deliverables
Fully working FastAPI service
Integrated ML models
API documentation (Swagger UI)
How They Work Together
Intern A builds the lead prediction model
Intern B builds revenue forecasting model
Intern C connects both models into a working API
