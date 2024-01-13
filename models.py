import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cargo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    num = db.Column(db.DECIMAL(10, 2), default=0)
    owner_id = db.Column(db.Integer, nullable=False)
    store_id = db.Column(db.Integer, nullable=False)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    account = db.Column(db.String(45), nullable=False)
    password = db.Column(db.String(45), nullable=False)
    address = db.Column(db.String(45))
    tel = db.Column(db.Integer)


class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255))



from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    query = StringField('关键词', validators=[DataRequired()])
    submit = SubmitField('搜索')