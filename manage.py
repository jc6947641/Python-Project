from flask import Flask, request, render_template
from models import db, Cargo  # 假设你有一个名为 Cargo 的模型
from login import userpass, register
from routes import get_data_routes
from cases.foodcase import go_foodcase
from cases.bookcase import go_bookcase
from cases.sportcase import go_sportcase
from cases.medicinecase import go_medicinecase
from cases.user import go_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import secrets

class SearchForm(FlaskForm):
    query = StringField('关键词', validators=[DataRequired()])
    submit = SubmitField('搜索')

secret_key = secrets.token_hex(16)

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key

HOSTNAME = '127.0.0.1'
PORT = '3306'
USERNAME = 'root'
PASSWORD = '123456'
DATABASE = 'store_management'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
userpass(app)
register(app)
get_data_routes(app)
go_foodcase(app)
go_bookcase(app)
go_sportcase(app)
go_medicinecase(app)
go_user(app)


if __name__ == '__main__':
    app.run(debug=True)