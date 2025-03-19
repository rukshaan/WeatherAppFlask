
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_login import LoginManager
# Create a single instance of SQLAlchemy
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Load the app configuration from config.py
    app.config.from_object('config.Config')
    
    # Initialize the database and migration objects
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)  # Initialize login manager here
    login_manager.login_view = 'auth.login'  # Set the default login route


    # Import and register blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    # Set up user_loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from .models import User  # Import the User model
        return User.query.get(int(user_id))


    return app

