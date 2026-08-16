
# Import necessary libraries
import numpy as np
import joblib       # For loading the serialised model
import pandas as pd
from flask import Flask, request, jsonify

# Initialise the Flask application
superkart_api = Flask("SuperKart")

# Load the trained model pipeline (preprocessing + regressor) at startup
# The model file is copied into the Docker container during build
model = joblib.load("superkart_model.joblib")


@superkart_api.get('/')
def home():
    """Simple health-check endpoint."""
    return "SuperKart Sales Forecasting API is running."


@superkart_api.post('/v1/predict')
def predict_sales():
    """
    Single-record inference endpoint.
    Expects a JSON body with all 10 feature keys.
    Returns the predicted Product_Store_Sales_Total.
    """
    data = request.get_json()

    # Build a single-row DataFrame matching the features expected by the model
    sample = {
        'Product_Weight':          data['Product_Weight'],
        'Product_Sugar_Content':   data['Product_Sugar_Content'],
        'Product_Allocated_Area':  data['Product_Allocated_Area'],
        'Product_MRP':             data['Product_MRP'],
        'Store_Size':              data['Store_Size'],
        'Store_Location_City_Type': data['Store_Location_City_Type'],
        'Store_Type':              data['Store_Type'],
        'Product_Id_char':         data['Product_Id_char'],
        'Store_Age_Years':         data['Store_Age_Years'],
        'Product_Type_Category':   data['Product_Type_Category'],
    }

    input_df = pd.DataFrame([sample])
    prediction = model.predict(input_df).tolist()[0]
    return jsonify({'Sales': round(prediction, 2)})


@superkart_api.post('/v1/predictbatch')
def predict_sales_batch():
    """
    Batch inference endpoint.
    Accepts a multipart file upload (CSV) and returns predictions for every row.
    """
    file = request.files['file']
    input_df = pd.read_csv(file)
    predictions = model.predict(input_df).tolist()
    output = {str(i): round(pred, 2) for i, pred in enumerate(predictions)}
    return output


if __name__ == '__main__':
    superkart_api.run(debug=True)
