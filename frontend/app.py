
import streamlit as st
import pandas as pd
import requests

# The Streamlit app communicates with the Flask backend over a Docker network.
# When both containers are running inside the same Codespace / Docker network,
# Docker's internal DNS resolves "backend" to the backend container's IP.
BACKEND_URL = "http://backend:7860"

st.title("SuperKart Sales Forecasting")
st.write("Enter product and store details to forecast the expected sales revenue for that product-store combination.")

# ── Input widgets ─────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    Product_Weight         = st.number_input("Product Weight (kg)", min_value=0.0, value=12.66, step=0.1)
    Product_Sugar_Content  = st.selectbox("Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
    Product_Allocated_Area = st.number_input("Allocated Display Area (ratio)", min_value=0.0, max_value=1.0, value=0.027, step=0.001, format="%.3f")
    Product_MRP            = st.number_input("Product MRP (₹)", min_value=0.0, value=117.08, step=1.0)
    Product_Id_char        = st.selectbox("Product Category Code", ["FD", "DR", "NC"])

with col2:
    Store_Size              = st.selectbox("Store Size", ["Small", "Medium", "High"])
    Store_Location_City_Type = st.selectbox("City Tier", ["Tier 1", "Tier 2", "Tier 3"])
    Store_Type              = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Supermarket Type3", "Departmental Store", "Food Mart"])
    Store_Age_Years         = st.number_input("Store Age (years)", min_value=0, value=16, step=1)
    Product_Type_Category   = st.selectbox("Product Category", ["Perishables", "Non Perishables"])

# Build the JSON payload
product_data = {
    "Product_Weight":          Product_Weight,
    "Product_Sugar_Content":   Product_Sugar_Content,
    "Product_Allocated_Area":  Product_Allocated_Area,
    "Product_MRP":             Product_MRP,
    "Store_Size":              Store_Size,
    "Store_Location_City_Type": Store_Location_City_Type,
    "Store_Type":              Store_Type,
    "Product_Id_char":         Product_Id_char,
    "Store_Age_Years":         Store_Age_Years,
    "Product_Type_Category":   Product_Type_Category,
}

# ── Single prediction ─────────────────────────────────────────────────────────
st.subheader("Single Prediction")
if st.button("Predict Sales", type="primary"):
    try:
        response = requests.post(f"{BACKEND_URL}/v1/predict", json=product_data, timeout=10)
        if response.status_code == 200:
            predicted = response.json()["Sales"]
            st.success(f"Predicted Sales Revenue: ₹{predicted:,.2f}")
        else:
            st.error(f"API error {response.status_code}: {response.text}")
    except Exception as e:
        st.error(f"Could not reach the backend: {e}")

# ── Batch prediction ──────────────────────────────────────────────────────────
st.subheader("Batch Prediction")
st.write("Upload a CSV file with the same feature columns to get predictions for multiple records at once.")
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file and st.button("Run Batch Predictions", type="primary"):
    try:
        response = requests.post(f"{BACKEND_URL}/v1/predictbatch", files={"file": uploaded_file}, timeout=60)
        if response.status_code == 200:
            results = response.json()
            st.success(f"Predictions completed for {len(results)} records.")
            df_results = pd.DataFrame(list(results.items()), columns=["Row Index", "Predicted Sales (₹)"])
            st.dataframe(df_results, use_container_width=True)
        else:
            st.error(f"API error {response.status_code}: {response.text}")
    except Exception as e:
        st.error(f"Could not reach the backend: {e}")
