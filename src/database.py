import psycopg2


def get_connection():
    return psycopg2.connect(
        host="database-1.c5qagcekwsqw.eu-north-1.rds.amazonaws.com",
        port=5432,
        database="customer",
        user="postgres",
        password="DataScience1212"
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
    past_60dpd_12m
):
    connection = get_connection()
    cursor = connection.cursor()

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
            past_60dpd_12m
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s
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
        past_60dpd_12m
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
