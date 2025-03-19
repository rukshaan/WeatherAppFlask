from flask import Blueprint, render_template,request,jsonify
import http.client
import json
from datetime import datetime
from Weather import db
from Weather.models import Weather1  # Import from models.py
from datetime import datetime, timedelta 
from Weather.predict_weather import predict_city
from flask_login import login_required, current_user




# Create the Blueprint
views = Blueprint('views', __name__)

@views.route('/',methods=['POST','GET'])
@login_required
def home():
    # Set up the API connection
    
    homeget()
    # home_img(Weather1.name)
    jaffna_data=getcity("Jaffna")
    trinco_data=getcity("Trincomalee")
    colombo_data=getcity("Colombo")
    vavuniya_data=getcity("Vavuniya")
    
    cities = Weather1.query.with_entities(Weather1.name).distinct().all()
    # weather_data=home_img(Weather1.name)
    unique_cities = [city[0] for city in cities]  # Extract city names from the query result
      
    return render_template('weather.html', jaffna_data=jaffna_data,vavuniya_data=vavuniya_data,colombo_data=colombo_data,trinco_data=trinco_data,unique_cities=unique_cities)
    

# Route to add city weather data to the database
@views.route('/add_city', methods=['POST'])
def add_city():
    # city_name = request.form.get('example-input1-group2')  # Get the city name from the form submission
    city_name = request.json.get('city_name') 
    print('city name is',city_name)
    if not city_name:
        return render_template("weather.html",error= "City name is required!")

    # Call the function to fetch weather data for the city
    weather_data = get_weather_data_from_api(city_name)

    if weather_data:
        # Store the weather data in the database
        store_weather_data_in_db(weather_data)
        return jsonify({'data':'weather data added successfully'})
    else:
        return jsonify({'data':'weather not added'})  # Display error on the page

# Function to fetch weather data from the API
def get_weather_data_from_api(city_name):
    import http.client
    from urllib.parse import urlencode

    # Set up the API connection
    
    conn = http.client.HTTPSConnection("weatherapi-com.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': "4765efd0e4msh0e6f4310f441125p115acdjsnc5b407e62f78",  # Replace with your actual API key
        'x-rapidapi-host': "weatherapi-com.p.rapidapi.com"
    }
    
    params = urlencode({"q": city_name})
       
        # Make the request to fetch the weather data for the city
    conn.request("GET", f"/current.json?{params}", headers=headers)
  
    res = conn.getresponse()
    data = res.read()
    # print('printing data ',data)
     
    if res.status == 200:
        weather_data = json.loads(data.decode("utf-8"))
        location = weather_data['location']
        current = weather_data['current']
        # print(weather_data)
        #Extract relevant information from the weather data
        location = weather_data['location']
        current = weather_data['current']
        condition = current['condition']
 
    # Create a new WeatherData instance
   
 
        existing_data = Weather1.query.filter_by(
            name=location['name'],
            condition_code=condition['code']
        ).first()
 
 
    if existing_data is None:
        weather_info = Weather1(
            name=location['name'],
            country=location['country'],
            temp_c=current['temp_c'],
            humidity=current['humidity'],
            wind_kph=current['wind_kph'],
            feelslike_c = current['feelslike_c'],
            condition=current['condition']['text'],
            condition_icon=current['condition']['icon'],
            condition_code=current['condition']['code'],
            localtime=location['localtime']
        )
        db.session.add(weather_info)
        db.session.commit()
        print("Weather data inserted into PostgreSQL!")
        return weather_info
 
    else:
        print("Weather data for this country and localtime already exists, skipping insert.")
 
 
    # print(weather_data)
# Function to store the weather data in the database
def store_weather_data_in_db(weather_data):
    try:
        # Ensure all required fields are present
        if not weather_data.get('city') or not weather_data.get('country'):
            print("Error: Missing city or country in weather data.")
            return
        
        # Check if the weather data already exists in the database based on city and country
       #existing_weather = Weather1.query.filter_by(name=weather_data['city'], country=weather_data['country']).first()
        # existing_weather = Weather1.query.filter_by(name='London', country='UK').first()
        existing_weather = Weather1.query.filter_by(name=weather_data['city'], country=weather_data['country']).first()
        if not existing_weather:
            # Create a new weather entry if it doesn't exist
            new_weather = Weather1(
                country=weather_data['country'],
                name=weather_data['city'],
                temp_c=weather_data['temp_c'],
                condition=weather_data['condition'],
                humidity=weather_data['humidity'],
                wind_kph=weather_data['wind_kph']
            )
            print(existing_weather)
            # Add the new weather data to the session
            db.session.add(new_weather)
            # Commit the transaction to the database
            db.session.commit()
            print("Weather data stored successfully.")
        else:
            print("Data already stored for this city and country.")
    except Exception as e:
        print(f"Error while storing data in the database: {str(e)}")
        db.session.rollback()  # Rollback the session to prevent partial transactions


def getcity(city_name):
    
    # Query the database for weather data for the specific city
    weather_data = Weather1.query.filter_by(name=city_name).first()
    # print('weather data',weather_data)
    if weather_data:
        # Pass the weather data to the template and render it
        return weather_data
    else:
        print("no data found")


@views.route('/cityName', methods=['POST','GET'])
def city_weather_dropdown():
    city_name = request.json.get('city_name') 

    if not city_name:
        return jsonify({'error':'no city selected'})
    
    # Query the database for weather data for the specific city
    weather_data1 = Weather1.query.filter_by(name=city_name).first()
    
    predictions_name=predict_city(city_name)
    print('prediction data is',predictions_name)
    if weather_data1:
        # Pass the weather data to the template and render it
        weather_details = {
            'name': weather_data1.name,
            'country': weather_data1.country,
            'temp_c': weather_data1.temp_c,
            'humidity': weather_data1.humidity,
            'wind_kph': weather_data1.wind_kph,
            'feelslike_c': weather_data1.feelslike_c,
            'condition': weather_data1.condition,
            'condition_icon': weather_data1.condition_icon,
            'condition_code': weather_data1.condition_code,
            'localtime': weather_data1.localtime.strftime("%Y-%m-%d %H:%M:%S")
        }
        print("datas",weather_details)
        # return weather_details,predictions
        
    else:
         print("error while getting city from db")
    return jsonify({
        'weather_details': weather_details,
        # 'predictions': predictions_name
        # "predictions": [float(pred) for pred in predictions_name] 
        # "predictions": [float(pred["AvgTemp"]) for pred in predictions_name]
        "predictions": [float(pred["AvgTemp"]) for pred in predictions_name]

    })
    
    
def homeget():
    conn_api = http.client.HTTPSConnection("weatherapi-com.p.rapidapi.com")
    
    # Set the necessary headers for the API request
    headers = {
        'x-rapidapi-key': "4765efd0e4msh0e6f4310f441125p115acdjsnc5b407e62f78",  # Replace with your actual API key
        'x-rapidapi-host': "weatherapi-com.p.rapidapi.com"
    }
   
    # Make the API request for weather data for a specific location
    conn_api.request("GET", "/current.json?q=53.1%2C-0.13", headers=headers)
    
    # Get the response from the API
    response = conn_api.getresponse()
    
    # Read the response data
    data = response.read()
    

    # Check if the response status is OK (200)
    if response.status == 200:
        # Parse the JSON data
       
        weather_data = json.loads(data.decode("utf-8")) 
        current = weather_data['current']
        condition=current['condition']
        # Extract the specific data we need
        location=weather_data['location']
        
        country = location['country']
        city = location['name']
        localtime = location['localtime']
        
        temp_c = current['temp_c']
        wind_kph = current['wind_kph']
        humidity = current['humidity']
        feelslike_c = current['feelslike_c']
           
        condition_text=current['condition']['text']
        condition_icon=current['condition']['icon']
        condition_code=current['condition']['code']
        
        existing_weather=Weather1.query.filter_by(country=country,name=city).first()
        # Create a new Weather instance and add it to the database
        if not existing_weather:
            new_weather = Weather1(
            condition_code=condition_code,  
            condition_icon=condition_icon,
            condition=condition_text, 
            country=country,
            name=city,
            localtime=datetime.strptime(localtime, "%Y-%m-%d %H:%M"),  # Parse localtime into a DateTime object
            temp_c=temp_c,
            wind_kph=wind_kph,
            humidity=humidity,
            feelslike_c=feelslike_c,      
        )
            db.session.add(new_weather)
            db.session.commit()
        else:          
            print ("Already Entered")
    else:
        print("")  




import os
@views.route('/get_prediction_files', methods=['GET'])
def get_prediction_files():
    # Directory where prediction files are stored
    # prediction_dir = "predicted_data"
    prediction_dir = "predicted_pdf"
    # Get all Excel files in the directory
    prediction_files = [f for f in os.listdir(prediction_dir) if f.endswith('.pdf')]
    logger.info(f"Prediction files: {prediction_files}")    
    # Return the list of files as JSON
    return jsonify(prediction_files)

from flask import Blueprint, request, jsonify
import smtplib
import os
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email_validator import validate_email, EmailNotValidError
from dotenv import load_dotenv
import pandas as pd
from email.mime.application import MIMEApplication
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="weather_report_app")
def get_country_from_city(city_name):
    location = geolocator.geocode(city_name, language='en')
    if location:
        address = location.address.split(', ')
        country = address[-1]
        return country
    else:
        return None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

@views.route('/send_report', methods=['POST'])
def send_report():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400

        receiver_email = data.get('email', 'rukshanjeyarajah@gmail.com')  # Use the email from the form or default to shaanruk0309@gmail.com
        cities = [city['value'] for city in data.get('cities', [])]

        # Validate inputs
        if not cities:
            return jsonify({"success": False, "message": "Please select at least one city"}), 400

        try:
            # Validate receiver email format
            email_info = validate_email(receiver_email, check_deliverability=True)
            receiver_email = email_info.normalized
        except EmailNotValidError as e:
            return jsonify({"success": False, "message": str(e)}), 400

        # Create email content
        msg = MIMEMultipart()
        msg['From'] = os.getenv('EMAIL_USER')
        msg['To'] = receiver_email
        msg['Subject'] = "Weather Prediction Report Request"

        # Build email body
        body = f"New weather report request received\n\n"
        body += f"Requested cities: {', '.join([city.capitalize() for city in cities])}\n\n"
        # body += "Prediction Data:\n"
        msg.attach(MIMEText(body, 'plain'))
        
        for city in cities:
            try:
                # Replace underscores with spaces to match the actual file naming convention
                # city_name_with_spaces = city.replace('_', ' ').lower()
                # # Sanitize city name for file path
                # safe_city = city_name_with_spaces.replace(' ', ' ')
                safe_city = city.strip().lower()
                file_path = os.path.join("predicted_pdf", f"{safe_city}_next_7_days_predictions.pdf")
                logger.info(f"Reading data from {file_path}")
                if os.path.exists(file_path):
                    # df = pd.read_excel(file_path)
                    # body += f"\n--- {city.capitalize()} ---\n"
                    # body += df.to_string(index=False) + "\n"
                    
                    with open(file_path, 'rb') as file:
                        logger.info(f"Processing data from {file_path}")
                        part = MIMEApplication(file.read(), Name=os.path.basename(file_path))
                        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                        msg.attach(part)
                    # body += f"\n--- {city.capitalize()} ---\n"
                    # body += f"PDF report attached.\n"
                    # Retrieve country name
                    country = get_country_from_city(city)
                    if country:
                        body += f"\n--- {city.capitalize()}, {country} ---\n"
                    else:
                        body += f"\n--- {city.capitalize()} (Country not found) ---\n"
                    body += f"PDF report attached.\n"
                else:
                    body += f"\n⚠️ Data not available for {city.capitalize()}\n"
            except Exception as e:
                logger.error(f"Error processing {city}: {str(e)}")
                body += f"\n❌ Error processing data for {city.capitalize()}\n"

        msg.attach(MIMEText(body, 'plain'))

        # Send email
        try:
            with smtplib.SMTP_SSL(
                'smtp.gmail.com',  # Gmail SMTP server
                465,
                timeout=30
            ) as server:
                server.login(
                    os.getenv('EMAIL_USER'), 
                    os.getenv('EMAIL_PASSWORD')
                )
                server.sendmail(
                    os.getenv('EMAIL_USER'), 
                    receiver_email, 
                    msg.as_string()
                )
                logger.info(f"Email successfully sent to {receiver_email}")
                
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error: {str(e)}")
            return jsonify({"success": False, "message": f"Failed to send email: {str(e)}"}), 500

        return jsonify({"success": True, "message": "Report sent successfully"})

    except Exception as e:
        logger.critical(f"Unexpected error: {str(e)}", exc_info=True)
        return jsonify({"success": False, "message": "Internal server error"}), 500
    
    
