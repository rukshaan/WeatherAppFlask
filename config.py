import os
from dotenv import load_dotenv


load_dotenv()


 # Default to 'my_password' if not set in the .env file


 
# class Config:
#     DB_HOST = os.getenv('DB_HOST', 'localhost')     # Default to 'localhost' if not set in the .env file
#     DB_PORT = os.getenv('DB_PORT', '5432')         # Default to '5432' if not set in the .env file
#     DB_NAME = os.getenv('DB_NAME', 'weatherDB')   # Default to 'my_database' if not set in the .env file
#     DB_USER = os.getenv('DB_USER', 'postgres')       # Default to 'my_user' if not set in the .env file
#     DB_PASSWORD = os.getenv('DB_PASSWORD', '12345678') 
#     SQLALCHEMY_TRACK_MODIFICATIONS = False  # To disable the warning about track modifications
#     SECRET_KEY = os.urandom(24)  # Used for securing sessions, cookies, etc.
#     SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
#     # Example: 'postgresql://postgres:password@localhost/myflaskdb'
class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:root@localhost:5432/weatherDB'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # To avoid a warning
    SECRET_KEY = 'class123'
