from fastapi import FastAPI, Request, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from uvicorn import run as app_run

from us_visa.constants import APP_HOST, APP_PORT
from us_visa.pipeline.prediction_pipeline import USvisaData, USvisaClassifier
from us_visa.pipeline.training_pipeline import TrainPipeline

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="templates")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_usvisa_data(
    request: Request,
    continent: str = Form(...),
    education_of_employee: str = Form(...),
    has_job_experience: str = Form(...),
    requires_job_training: str = Form(...),
    no_of_employees: str = Form(...),
    company_age: str = Form(...),
    region_of_employment: str = Form(...),
    prevailing_wage: str = Form(...),
    unit_of_wage: str = Form(...),
    full_time_position: str = Form(...),
):
    return USvisaData(
        continent=continent,
        education_of_employee=education_of_employee,
        has_job_experience=has_job_experience,
        requires_job_training=requires_job_training,
        no_of_employees=no_of_employees,
        company_age=company_age,
        region_of_employment=region_of_employment,
        prevailing_wage=prevailing_wage,
        unit_of_wage=unit_of_wage,
        full_time_position=full_time_position,
    )

@app.get("/", tags=["authentication"])
async def index(request: Request):
    return templates.TemplateResponse("usvisa.html", {"request": request, "context": "Rendering"})

@app.get("/train")
async def train_model():
    try:
        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()
        return {"status": "success", "message": "Training successful!"}
    except Exception as e:
        return {"status": "error", "message": f"Error occurred: {str(e)}"}

@app.post("/")
async def predict(request: Request, usvisa_data: USvisaData = Depends(get_usvisa_data)):
    try:
        usvisa_df = usvisa_data.get_usvisa_input_data_frame()
        model_predictor = USvisaClassifier()
        prediction = model_predictor.predict(dataframe=usvisa_df)[0]
        status = "Visa-approved" if prediction == 1 else "Visa Not-Approved"
        return templates.TemplateResponse("usvisa.html", {"request": request, "context": status})
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)
