
import streamlit as st
import requests

#  deployed FastAPI endpoint
API_URL = "https://end-to-end-customer-churn-hw7x.onrender.com/predict"

st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="centered"
)

st.title("📊 Telecom Customer Churn Prediction")
st.write(
    "Enter customer details to estimate the likelihood "
    "that the customer will leave the telecom service."
)

with st.form("customer_form"):

    st.subheader("Customer Information")

    col1, col2 = st.columns(2)

    with col1:
        gender = st.selectbox("Gender", ["Female", "Male"])
        senior = st.selectbox("Senior Citizen", [0, 1])
        partner = st.selectbox("Has Partner?", ["Yes", "No"])
        dependents = st.selectbox("Has Dependents?", ["Yes", "No"])
        tenure = st.number_input(
            "Tenure (months)", min_value=0, max_value=100, value=2
        )
        phone = st.selectbox("Phone Service", ["Yes", "No"])
        multiple_lines = st.selectbox(
            "Multiple Lines", ["No", "Yes", "No phone service"]
        )
        internet = st.selectbox(
            "Internet Service", ["DSL", "Fiber optic", "No"]
        )
        security = st.selectbox(
            "Online Security", ["Yes", "No", "No internet service"]
        )
        backup = st.selectbox(
            "Online Backup", ["Yes", "No", "No internet service"]
        )

    with col2:
        protection = st.selectbox(
            "Device Protection", ["Yes", "No", "No internet service"]
        )
        support = st.selectbox(
            "Tech Support", ["Yes", "No", "No internet service"]
        )
        tv = st.selectbox(
            "Streaming TV", ["Yes", "No", "No internet service"]
        )
        movies = st.selectbox(
            "Streaming Movies", ["Yes", "No", "No internet service"]
        )
        contract = st.selectbox(
            "Contract",
            ["Month-to-month", "One year", "Two year"]
        )
        paperless = st.selectbox("Paperless Billing", ["Yes", "No"])
        payment = st.selectbox(
            "Payment Method",
            [
                "Electronic check",
                "Mailed check",
                "Bank transfer (automatic)",
                "Credit card (automatic)"
            ]
        )
        monthly_charges = st.number_input(
            "Monthly Charges", min_value=0.0, value=55.5, step=1.0
        )
        total_charges = st.number_input(
            "Total Charges", min_value=0.0, value=111.0, step=1.0
        )

    submitted = st.form_submit_button(
        "Predict Churn", type="primary", use_container_width=True
    )

if submitted:
    customer = {
        "gender": gender,
        "SeniorCitizen": senior,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "PhoneService": phone,
        "MultipleLines": multiple_lines,
        "InternetService": internet,
        "OnlineSecurity": security,
        "OnlineBackup": backup,
        "DeviceProtection": protection,
        "TechSupport": support,
        "StreamingTV": tv,
        "StreamingMovies": movies,
        "Contract": contract,
        "PaperlessBilling": paperless,
        "PaymentMethod": payment,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges
    }

    try:
        with st.spinner("Contacting the prediction API..."):
            response = requests.post(
                API_URL, json=customer, timeout=120
            )

        if response.ok:
            result = response.json()
            st.subheader("Prediction Result")

            if result["prediction"] == "Churn":
                st.warning("⚠️ The model predicts that this customer may churn.")
            else:
                st.success("✅ The model predicts that this customer may stay.")

            st.metric(
                "Estimated Churn Probability",
                f"{result['churn_probability_percent']:.2f}%"
            )

            st.caption(
                f"Decision threshold: {result['threshold']:.2f}"
            )
            st.info(
                "This is a model estimate, not a guarantee of customer behavior."
            )
        else:
            st.error(f"API error ({response.status_code}): {response.text}")

    except requests.exceptions.Timeout:
        st.error(
            "The API took too long to respond. The free Render service "
            "may be waking up. Wait a little and try again."
        )
    except requests.exceptions.RequestException as error:
        st.error(f"Could not connect to the API: {error}")
