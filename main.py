# Credit Risk Analyzer API
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from model.predict import predict as model_predict, MODEL_VERSION, model, threshold
from schema.user_input import UserInput
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.responses import FileResponse
import pandas as pd


Model = {}
@asynccontextmanager
async def lifespan(app : FastAPI):
    Model['model'] = model
    Model['threshold'] = threshold
    
    yield

    Model.clear()

app = FastAPI(lifespan=lifespan, title="Credit Risk Analyzer API",
               description="This API predicts the credit risk of a loan applicant" \
               " based on their personal and financial information.",
                 version=MODEL_VERSION)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / 'frontend'

# Serve frontend assets
app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static"
)
  

@app.get('/')
def home():
    return FileResponse(FRONTEND_DIR / 'index.html')
@app.get('/health')
def health():
    return {'status': 'OK',
            'Version': MODEL_VERSION,
            'model': model is not None}
# getting in input
@app.post('/predict')
def predict(user_input: UserInput):
    user_input_dict = pd.DataFrame([{
        
        'person_age': user_input.person_age,
        'person_income': user_input.person_income,
        'person_home_ownership': user_input.person_home_ownership,
        'person_emp_length': user_input.person_emp_length,
        'loan_intent': user_input.loan_intent,
        'loan_grade': user_input.loan_grade,
        'loan_amnt': user_input.loan_amnt,
        'loan_int_rate': user_input.loan_int_rate,
        'cb_person_default_on_file': user_input.cb_person_default_on_file,
        'cb_person_cred_hist_length': user_input.cb_person_cred_hist_length,
        'loan_percent_income': user_input.loan_percent_income
    }])
    try:
        prediction = model_predict(user_input_dict)
        return JSONResponse(status_code=200, content=prediction)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))