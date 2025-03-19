from flask import Blueprint,session,flash
import json
from flask import Flask, request, jsonify,render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from Weather.models import User  # Import from models.py
from flask_login import login_user,current_user;
from flask_login import logout_user
auth=Blueprint('auth',__name__)
 
@auth.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        # Retrieve form data using request.form.get()
        uname = request.form.get('uname')
        email = request.form.get('email')
        password = request.form.get('password')
        c_password = request.form.get('c_password')
        # terms = request.form.get('terms')  # This will be None if not checked

        # Validate the data
        if not all([uname, email, password, c_password]):
            return jsonify({"message": "Missing required fields"}), 400

        if password != c_password:
            return jsonify({"message": "Passwords do not match"}), 400
        
        # Check if user already exists
        user = User.query.filter((User.uname == uname) | (User.email == email)).first()
        if user:
            #return jsonify({"message": "Username or email already exists"}), 400
            return render_template('login.html')
        # Hash the password before saving
        hashed_password = generate_password_hash(password)
        print("conform password is",c_password)
        # Create a new user and add to the database
        new_user = User(uname=uname, email=email, password=hashed_password,c_password=c_password)
        db.session.add(new_user)
        db.session.commit()

        return render_template('signup.html')

    # For GET requests, render the sign-up form
    return render_template('signup.html')



@auth.route("/login", methods=['GET', 'POST'])
def login():
    # If the user is already logged in, redirect to the home page
    if current_user.is_authenticated:  # Using Flask-Login's current_user
        return redirect(url_for('views.home'))  # Redirect to home page if already logged in

    if request.method == 'POST':
        # Get username/email and password from the form
        username = request.form.get('username')
        password = request.form.get('password')

        # Find the user by username or email
        user = User.query.filter((User.uname == username) | (User.email == username)).first()

        # If the user doesn't exist or the password is incorrect
        if user and check_password_hash(user.password, password):
            
            login_user(user)  # Automatically manages session for the user
            flash("Login successful!", "success")
            return redirect(url_for('views.home'))

        # If login fails, show error message
        flash("Invalid credentials, please try again.", "error")
        #return jsonify({"message": "Invalid credentials, please try again!"}), 400
        return render_template('login.html')

    # For GET requests, render the login form
    return render_template('login.html')

# Optional: You can also add a route for logging out
@auth.route("/logout",methods=["POST"])
def logout():
    # session.clear()  # Clear session data
    logout_user()  # This will log out the user
    
    return redirect(url_for('auth.login'))
