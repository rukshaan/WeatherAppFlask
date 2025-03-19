from Weather import create_app
from flask import Blueprint,session,flash,redirect,url_for
# Create the app instance using create_app()
app = create_app()
# Register the Blueprint for authentication routes


if __name__ == '__main__':
    # Only call app.run() once, no need to call create_app() here again
    app.run(debug=True)

