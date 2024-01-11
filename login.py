from flask import Flask
app = Flask(__name__)
from flask import render_template, request, redirect, url_for
from models import db, User

# Assuming you have a User model defined in models.py

def userpass(app):
    @app.route('/', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            # Get the form data
            account = request.form['account']
            password = request.form['password']

            # Check if the user exists in the database
            user = User.query.filter_by(account=account, password=password).first()

            if user:
                # Login successful, redirect to index.html
                return redirect(url_for('homelist'))
            else:
                # Login failed, show an error message
                error_message = "Invalid credentials. Please try again."
                return render_template('login.html', error_message=error_message)

        # If it's a GET request, render the login form
        return render_template('login.html')

    # Define your other routes here

