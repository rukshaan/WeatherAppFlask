from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from . import db


class Weather(db.Model):
    __tablename__ = 'weather_data'
    condition_code = db.Column(db.Integer, primary_key=True)  # condition_code as primary key
    country = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False, unique=True)
    localtime = db.Column(db.DateTime, nullable=False)
    temp_c = db.Column(db.Float, nullable=False)
    wind_kph = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    feelslike_c = db.Column(db.Float, nullable=False)
    cloud = db.Column(db.Float, nullable=False)
    condition = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Weather {self.name} in {self.country} >"


class Weather1(db.Model):
    __tablename__ = 'weather_data1'

    # Define columns
   
    condition_code = db.Column(db.Integer,nullable=False)
    country = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    temp_c = db.Column(db.String(100), nullable=False)
    wind_kph = db.Column(db.String(100), nullable=False)
    humidity = db.Column(db.String(100), nullable=False)
    feelslike_c = db.Column(db.String(100), nullable=False)
    
    condition = db.Column(db.String(100), nullable=False)
    condition_icon = db.Column(db.String(100), nullable=True)
    localtime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
 
    # Primary Key Constraint across 'name' and 'condition_code'
    __table_args__ = (
        db.PrimaryKeyConstraint('name', 'condition_code'),
    )

    def __repr__(self):
        return f"<Weather1 {self.condition_code}, {self.name} in {self.country} >"



# class User(db.Model):
#     __tablename__ = 'User'
#     id = db.Column(db.Integer, primary_key=True,autoincrement=True)
#     uname = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(100), nullable=False)
#     password = db.Column(db.String(255), nullable=False)
#     c_password = db.Column(db.String(255), nullable=False)
    
#     def __repr__(self):
#         return f"<User {self.uname} >"


class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    c_password = db.Column(db.String(255), nullable=False)
    _is_active = db.Column(db.Boolean, default=True)  # Custom active field
    
    @property
    def is_active(self):
        return self._is_active

    def __repr__(self):
        return f"<User {self.uname} >"