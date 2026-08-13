import pickle
import pandas as pd
import numpy as np


with open("models/lg_model.pkl","rb") as file:
    lr_moodel = pickle.load(file)

    if lr_moodel:
        print("model successfully imported")

with open("models/education_encoder.pkl","rb") as file:
    education_encoder = pickle.load(file)
    if education_encoder:
        print("encoder imported ")

with open("models/std_scalar.pkl","rb") as file:
    scalar = pickle.load(file)

    if scalar:
        print("scalar imported")



def applicant_info(
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
    past_60dpd_12m):

    data_dict = {"Age":age,"Marital_Status":marital_status,
                 "Dependents":dependents,"Education_Level":education_level,
                 "Employment_Status":employment_status,
                 "Years_Employed":years_employed,"Annual_Income":annual_income,
                 "Housing_Type":housing_type,
                 "Years_At_Residence":years_at_residence,
                 "Bureau_Score":bureau_score,
                 "Num_Existing_Cards":num_existing_cards,
                 "Total_Existing_Debt":total_existing_debt,
                 "Requested_Credit_Limit":requested_credit_limit,
                 "Bureau_Inquiries_6M":bureau_inquiries_6m,
                 "Past_30DPD_12M":past_30dpd_12m,
                "Past_60DPD_12M":past_60dpd_12m}


    # log transformation on the some feature as done when model training
    df = pd.DataFrame([data_dict])
    print("1. DATAFRAME CREATED")

    df["Annual_Income"] = np.log1p(df["Annual_Income"])
    df["Total_Existing_Debt"] = np.log1p(df["Total_Existing_Debt"])
    df["Requested_Credit_Limit"] = np.log1p(df["Requested_Credit_Limit"])
    df["Bureau_Score"] = np.log1p(df["Bureau_Score"])
    print("2. LOG TRANSFORMATION DONE")



    # doing the mapping as done in the model training

    marital_mapping = {
        "single": 0,
        "married": 1,
        "divorced": 2,
        "widowed": 3
    }

    employment_mapping = {
        "retired": 0,
        "salaried": 1,
        "self-employed": 2,
        "unemployed": 3,
        "student": 4
    }

    housing_mapping = {
        "mortgage": 0,
        "own": 1,
        "rent": 2,
        "unemployed": 3,
        "with parents": 4
    }

    df["Marital_Status"] = df["Marital_Status"].str.lower().map(marital_mapping)

    df["Employment_Status"] = (
        df["Employment_Status"].str.lower().map(employment_mapping)
    )

    df["Housing_Type"] = (
        df["Housing_Type"].str.lower().map(housing_mapping)
    )

    print(education_encoder.categories_)

    df[["Education_Level"]] = education_encoder.transform(df[["Education_Level"]])

    print("mappping done")

    print("COLUMNS BEFORE SCALING:")
    print(df.columns)




    scaled_df = scalar.transform(df)
    print("4. SCALING DONE")

    predication = lr_moodel.predict(scaled_df)

    print("MODEL OUTPUT:", predication)

    return int(predication[0])


