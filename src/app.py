from fastapi import FastAPI,Form,Request
from fastapi.templating import Jinja2Templates
from src.database import insert_applicant
from src.predication import applicant_info
app = FastAPI()
templates = Jinja2Templates(directory="FrountEnd")

import pandas as pd


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.post("/submit")
def submit_application(request:Request,age:int=Form(...),marital_status: str = Form(...),dependents: int = Form(...),
                       education_level: str = Form(..., alias="education"),
                       employment_status: str = Form(...),
                       years_employed: int = Form(...),
                       annual_income: float = Form(...),
                       housing_type: str = Form(...),
                       years_at_residence: int = Form(...),
                       bureau_score: int = Form(...),
                       num_existing_cards: int = Form(..., alias="existing_cards"),
                       total_existing_debt: float = Form(..., alias="existing_debt"),
                       requested_credit_limit: float = Form(..., alias="credit_limit"),
                       bureau_inquiries_6m: int = Form(2),
                       past_30dpd_12m: int = Form(1),
                       past_60dpd_12m: int = Form(0)
                       ):

    applicant_id = insert_applicant(
        age,
        marital_status,
        dependents,
        education_level,
        employment_status,
        years_employed,
        annual_income,
        housing_type,
        years_at_residence,
        bureau_score,
        num_existing_cards,
        total_existing_debt,
        requested_credit_limit,
        bureau_inquiries_6m,
        past_30dpd_12m,
        past_60dpd_12m
    )

    applicant_information = applicant_info(age,
        marital_status,
        dependents,
        education_level,
        employment_status,
        years_employed,
        annual_income,
        housing_type,
        years_at_residence,
        bureau_score,
        num_existing_cards,
        total_existing_debt,
        requested_credit_limit,
        bureau_inquiries_6m,
        past_30dpd_12m,
        past_60dpd_12m
    )

    if applicant_information == 0:
        return templates.TemplateResponse(
            request=request,  # <--- Pass request directly here
            name="result.html",
            context={
                    "status": "approved",
                    "title": "Congratulations!",
                    "message": "Your application has been approved based on our credit assessment.",
                    "description": "Your financial profile meets the current eligibility criteria.",
                },
            )
    else:
        return templates.TemplateResponse(
            request=request,  # <--- Pass request directly here
            name="result.html",
            context={
                    "status": "rejected",
                    "title": "Application Not Approved",
                    "message": "We're sorry, but your application could not be approved at this time.",
                    "description": "Based on the current credit assessment, the application does not meet the required eligibility criteria.",
                },
            )
