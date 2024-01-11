from flask import Flask
from models import db
from login import userpass, register  # 导入新的函数
from routes import get_data_routes
import secrets

secret_key = secrets.token_hex(16)

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key  # 使用生成的随机密钥

HOSTNAME = '127.0.0.1'
PORT = '3306'
USERNAME = 'root'
PASSWORD = '123456'
DATABASE = 'store_management'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
userpass(app)
register(app)  # 调用新的函数
get_data_routes(app)

if __name__ == '__main__':
    app.run(debug=True)