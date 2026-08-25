import psycopg2
from src.predication import predication_default,predication_default_proba


def get_connection():
    return psycopg2.connect(
        host="credit-db.c70ec4qg6ieo.ap-south-1.rds.amazonaws.com",
        port=5432,
        database="customer",
        user="postgres",
        password="DataScience1212",
        sslmode="require"
    )




def insert_applicant(
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
    past_60dpd_12m,
    applicant_information
):
    connection = get_connection()
    cursor = connection.cursor()


    query = """CREATE TABLE IF NOT EXISTS applicants (
    applicant_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    age INTEGER,
    marital_status VARCHAR(20),
    dependents INTEGER,
    education_level VARCHAR(50),
    employment_status VARCHAR(50),
    years_employed INTEGER,
    annual_income NUMERIC(15,2),
    housing_type VARCHAR(30),
    years_at_residence INTEGER,
    bureau_score INTEGER,
    num_existing_cards INTEGER,
    total_existing_debt NUMERIC(15,2),
    requested_credit_limit NUMERIC(15,2),
    bureau_inquiries_6m INTEGER,
    past_30dpd_12m INTEGER,
    past_60dpd_12m INTEGER,
    predicted_default Integer
    );
"""

    cursor.execute(query)
    connection.commit()

    predicted_default = predication_default


    query = """
        INSERT INTO applicants (
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
            past_60dpd_12m,
            predicted_default
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s,%s
        )
        RETURNING applicant_id;
    """



    values = (
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
        past_60dpd_12m,
        predicted_default,
        applicant_information
    )

    cursor.execute(query, values)

    applicant_id = cursor.fetchone()[0]

    connection.commit()

    cursor.close()
    connection.close()

    return applicant_id






if __name__ == "__main__":
    connection = get_connection()
    print("PostgreSQL connection successful!")
    connection.close()
