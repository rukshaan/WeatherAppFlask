import http.client
import json
import csv
from datetime import datetime, timedelta
import os

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
 
import xgboost as xgb
from sklearn.metrics import mean_absolute_error
from urllib.parse import quote 
def fetch_weather_data(city):
    # Get today's date and the date 7 days ago
    today = datetime.today()
    seven_days_ago = today - timedelta(days=6)
   
    # Format dates to strings
    today_str = today.strftime('%Y-%m-%d')
    seven_days_ago_str = seven_days_ago.strftime('%Y-%m-%d')
    encoded_city = quote(city)
    # API Connection to RapidAPI Weather API
    conn = http.client.HTTPSConnection("weatherapi-com.p.rapidapi.com")
 
    headers = {
           'x-rapidapi-key': "1189d1cbfcmshff6e7d2c8e7e466p1490a7jsn53d09429c10e",
           'x-rapidapi-host': "weatherapi-com.p.rapidapi.com"
    }
 
    # API URL to fetch historical weather data
    url = f"/history.json?q={encoded_city}&lang=en&dt={seven_days_ago_str}&end_dt={today_str}"
 
    # Make the API request
    conn.request("GET", url, headers=headers)
 
    # Get the response
    res = conn.getresponse()
    data = res.read()
   
 
    # Parse the JSON response
 
    weather_data = json.loads(data.decode("utf-8"))
   
    return weather_data


def split_data(X, y):
    # Split the data into training and testing sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # print('x train in split',X_train)
    return X_train, X_test, y_train, y_test
 
 
 
def train_model(X_train, y_train):
    # Initialize the XGBoost model
    model = xgb.XGBRegressor(objective="reg:squarederror", n_estimators=100, random_state=42)
    # print("Shape of X_train:", X_train.shape)
   
    # Train the model
    model.fit(X_train, y_train)
   
    return model
 
 
def evaluate_model(model, X_test, y_test):
    # Make predictions on the test set
    y_pred = model.predict(X_test)
 
    # Evaluate the model using Mean Absolute Error (MAE)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"Mean Absolute Error: {mae:.2f}")
 
    # You can also print predicted vs actual values if needed
    comparison = pd.DataFrame({"Actual": y_test, "Predicted": y_pred})
    print(comparison.head())
 
 
def predict_next_day_temperature(model, input_data):
    # Make a prediction for the next day's temperature
    predicted_temp = model.predict(input_data)
    print(f"Predicted temperature for next day: {predicted_temp[0]:.2f}°C")


def predict_city(city):
    fetch_data = fetch_weather_data(city)
    convert_to_csv(fetch_data, city)

    X_scaled, y, scaler = preprocess_data(city)

    X_train, X_test, y_train, y_test = split_data(X_scaled, y)
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)

    last_known_data = X_scaled[-1:]

    # Get multi-feature predictions
    predictions = predict_next_7_days(model, last_known_data, scaler, days=7)

    # Save predictions with all columns to Excel
    save_predictions_to_excel(predictions, city)
    
    # Generate PDF with predicted data
    predicted_pdf_data(predictions, city)
    return predictions 
 

import random
import numpy as np
def predict_next_7_days(model, last_known_data, scaler, days=7):
    print(last_known_data)

    predictions = []
    
    current_input = last_known_data

    # Get the last known feature values (unscaled)
    last_known_humidity = current_input[0, 0]  
    last_known_windspeed = current_input[0, 1]  
    last_known_precipitation = current_input[0, 2]  

    for day in range(days):
        print('Current data is ', current_input)

        # Predict temperature
        predicted_temp = model.predict(current_input)
        avg_temp = float(predicted_temp[0])

        # Simulate realistic values for other features
        next_day_humidity = last_known_humidity + np.random.normal(0, 5)  # smaller stddev for realism
        next_day_windspeed = last_known_windspeed + np.random.normal(0, 2)
        next_day_precipitation = last_known_precipitation + np.random.normal(0, 0.5)

        # Clip values to prevent unrealistic results
        next_day_humidity = np.clip(next_day_humidity, 0, 100)
        next_day_windspeed = max(next_day_windspeed, 0)
        next_day_precipitation = max(next_day_precipitation, 0)

        predictions.append({
            "AvgTemp": avg_temp,
            "Humidity": next_day_humidity,
            "WindSpeed": next_day_windspeed,
            "Precipitation": next_day_precipitation
        })

        # Prepare next input for the model (scaled features)
        new_data_point = np.array([[next_day_humidity, next_day_windspeed, next_day_precipitation]])
        current_input = scaler.transform(new_data_point)

    return predictions

 
 



# ######################################################### Convert to csv start ################################################################
# import os

# def convert_to_csv(weather_data, city):
#     header = ["Date", "AvgTemp", "Humidity", "WindSpeed", "Precipitation", "Condition"]
#     rows = []

#     # Loop through the forecast data and add each day's weather information
#     for day in weather_data['forecast']['forecastday']:
#         rows.append([
#             day['date'],  # Date
#             day['day']['avgtemp_c'],  # Average Temperature (Celsius)
#             day['day']['avghumidity'],  # Average Humidity
#             day['day']['maxwind_kph'],  # Max Wind Speed (kph)
#             day['day']['totalprecip_mm'],  # Precipitation (mm)
#             day['day']['condition']['text']  # Weather Condition (text)
#         ])

#     # Create 'weather_details' directory if it doesn't exist
#     output_dir = "weather_details"
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)

#     # Save the CSV file in the 'weather_details' directory
#     csv_filename = os.path.join(output_dir, f"{city}_weather_data.csv")
#     with open(csv_filename, mode="w", newline="") as file:
#         writer = csv.writer(file)
#         writer.writerow(header)  # Write the header row
#         writer.writerows(rows)  # Write the weather data

#     print(f"CSV file '{csv_filename}' created successfully.")




# def convert_to_csv(weather_data, city):
#     header = ["Date", "AvgTemp", "Humidity", "WindSpeed", "Precipitation", "Condition"]
#     rows = []

#     # Loop through the forecast data and add each day's weather information
#     for day in weather_data['forecast']['forecastday']:
#         rows.append([
#             day['date'],  # Date
#             day['day']['avgtemp_c'],  # Average Temperature (Celsius)
#             day['day']['avghumidity'],  # Average Humidity
#             day['day']['maxwind_kph'],  # Max Wind Speed (kph)
#             day['day']['totalprecip_mm'],  # Precipitation (mm)
#             day['day']['condition']['text']  # Weather Condition (text)
#         ])

#     # Create 'weather_details' directory if it doesn't exist
#     output_dir = "weather_details"
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)

#     # Define the CSV filename based on the city name
#     csv_filename = os.path.join(output_dir, f"{city}_weather_data.csv")
    
#     # Check if the file exists and write data accordingly
#     file_exists = os.path.exists(csv_filename)

#     with open(csv_filename, mode="a", newline="") as file:  # Open file in append mode
#         writer = csv.writer(file)
        
#         # If the file doesn't exist, write the header first
#         if not file_exists:
#             writer.writerow(header)  # Write the header row
        
#         # Write the weather data
#         writer.writerows(rows)  # Append the new weather data

#     print(f"CSV file '{csv_filename}' updated successfully.")

def convert_to_csv(weather_data, city):
    header = ["Date", "AvgTemp", "Humidity", "WindSpeed", "Precipitation", "Condition"]
    rows = []

    # Loop through the forecast data and collect each day's weather information
    for day in weather_data['forecast']['forecastday']:
        rows.append([
            day['date'],  # Date
            day['day']['avgtemp_c'],  # Average Temperature (Celsius)
            day['day']['avghumidity'],  # Average Humidity
            day['day']['maxwind_kph'],  # Max Wind Speed (kph)
            day['day']['totalprecip_mm'],  # Precipitation (mm)
            day['day']['condition']['text']  # Weather Condition (text)
        ])
    
    # Define the CSV file path
    output_dir = "weather_details"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    csv_filename = os.path.join(output_dir, f"{city}_weather_data.csv")

    # Check if the file exists
    if os.path.exists(csv_filename):
        existing_df = pd.read_csv(csv_filename)
    else:
        existing_df = pd.DataFrame(columns=header)

    # Convert new data into a DataFrame
    new_df = pd.DataFrame(rows, columns=header)

    # Merge existing and new data, updating only if values change
    updated_df = pd.concat([existing_df, new_df]).drop_duplicates(subset=["Date"], keep="last")

    # Save the updated data
    updated_df.to_csv(csv_filename, index=False)

    print(f"CSV file '{csv_filename}' updated successfully.")



# //////////////////////////////////////// Convert to csv end////////////////////////////////////////

# ######################################################### Pre process data start ################################################################
def preprocess_data(city):
    
    csv_filename = os.path.join("weather_details", f"{city}_weather_data.csv")
    df = pd.read_csv(csv_filename)

    df['Date'] = pd.to_datetime(df['Date'])
    df = df.drop(columns=["Date", "Condition"])  # Drop non-numeric columns

    X = df.drop(columns=["AvgTemp"])
    y = df["AvgTemp"]

    X = X.values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, scaler
# //////////////////////////////////////// Pre process data  end////////////////////////////////////////


# ######################################################### categorized preception start ################################################################

def categorize_precipitation(precipitation):
    """Categorizes the precipitation amount into weather conditions."""
    if precipitation == 0:
        return "No precipitation (Clear or dry weather)"
    elif 1 <= precipitation < 5:
        return "Light rain or drizzle"
    elif 5 <= precipitation < 10:
        return "Moderate rain"
    elif 10 <= precipitation < 50:
        return "Heavy rain or showers"
    else:
        return "Very heavy rain, storm, or snowfall"

def save_predictions_to_excel(predictions, city):
    # Create 'predicted_data' directory if it doesn't exist
    output_dir = "predicted_data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Prepare dates for the next 7 days
    today = datetime.today()
    prediction_dates = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, len(predictions) + 1)]

    # Create lists to hold the prediction data
    avg_temps = []
    humidities = []
    windspeeds = []
    precipitations = []
    weather_conditions = []  # New list to store the precipitation category

    # Extract data from predictions and categorize precipitation
    for prediction in predictions:
        avg_temps.append(prediction["AvgTemp"])
        humidities.append(prediction["Humidity"])
        windspeeds.append(prediction["WindSpeed"])
        precipitations.append(prediction["Precipitation"])
        weather_conditions.append(categorize_precipitation(prediction["Precipitation"]))  # Categorize

    # Create a DataFrame with all predictions
    df_predictions = pd.DataFrame({
        "Date": prediction_dates,
        "Predicted AvgTemp (°C)": avg_temps,
        "Predicted Humidity (%)": humidities,
        "Predicted Wind Speed (kph)": windspeeds,
        "Predicted Precipitation (mm)": precipitations,
        "Weather Condition": weather_conditions  # Add categorized precipitation
    })

    # Define the Excel filename
    excel_filename = os.path.join(output_dir, f"{city}_next_7_days_predictions.xlsx")

    # Save to Excel
    df_predictions.to_excel(excel_filename, index=False, sheet_name="Next 7 Days Forecast")

    print(f"Predictions saved successfully to '{excel_filename}'")



# ######################################################### Save predicted dataset to pdf################################################################
from fpdf import FPDF

def predicted_pdf_data(predictions, city):
    """
    Generates a PDF file containing the predicted weather data for the next 7 days.
    
    Args:
        predictions (list): List of dictionaries containing predicted weather data.
        city (str): Name of the city for which predictions are made.
    """
    # Create 'predicted_pdf' directory if it doesn't exist
    output_dir = "predicted_pdf"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Prepare dates for the next 7 days
    today = datetime.today()
    prediction_dates = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, len(predictions) + 1)]

    # Create a PDF object
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add a title
    pdf.cell(200, 20, txt=f"Weather Predictions for {city.capitalize()} (Next 7 Days)", ln=True, align="C")
    pdf.ln(20)  # Add some space

    # Add table headers
    pdf.set_font("Arial", size=10, style="B")
    pdf.cell(20, 10, "Date", border=1)
    pdf.cell(25, 10, "Avg Temp (°C)", border=1)
    pdf.cell(25, 10, "Humidity (%)", border=1)
    pdf.cell(30, 10, "Wind Speed (kph)", border=1)
    pdf.cell(30, 10, "Precipitation (mm)", border=1)
    pdf.cell(65, 10, "Weather Condition", border=1)
    pdf.ln()

    # Add table rows with predicted data
    pdf.set_font("Arial", size=10)
    for i, prediction in enumerate(predictions):
        pdf.cell(20, 10, prediction_dates[i], border=1)
        pdf.cell(25, 10, f"{prediction['AvgTemp']:.2f}", border=1)
        pdf.cell(25, 10, f"{prediction['Humidity']:.2f}", border=1)
        pdf.cell(30, 10, f"{prediction['WindSpeed']:.2f}", border=1)
        pdf.cell(30, 10, f"{prediction['Precipitation']:.2f}", border=1)
        pdf.cell(65, 10, categorize_precipitation(prediction['Precipitation']), border=1)
        pdf.ln()

    # Save the PDF file
    pdf_filename = os.path.join(output_dir, f"{city}_next_7_days_predictions.pdf")
    pdf.output(pdf_filename)

    print(f"PDF file '{pdf_filename}' created successfully.")