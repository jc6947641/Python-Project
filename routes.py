# routes.py

from flask import render_template
from models import Cargo

def get_data_routes(app):
    @app.route('/')
    def home():
        return render_template('login.html')
    @app.route('/index')
    def index():
        # Fetch all cargo records from the database
        cargo_list = Cargo.query.all()
        # Render the index.html template with cargo data
        return render_template('index.html', cargo_list=cargo_list)
