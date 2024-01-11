from flask import Flask
from models import db
from login import userpass
from routes import get_data_routes
import secrets

secret_key = secrets.token_hex(16)  # 16 字节的随机十六进制字符串


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

# 配置数据库连接
HOSTNAME = '127.0.0.1'
PORT = '3306'
USERNAME = 'root'
PASSWORD = '123456'
DATABASE = 'store_management'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 禁用修改跟踪

# 初始化数据库
db.init_app(app)
userpass(app)
app_data = Flask(__name__)
get_data_routes(app)



if __name__ == '__main__':
    app.run(debug=True)
