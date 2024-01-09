from flask import Flask
from models import db
from routes import init_routes

app = Flask(__name__)

# 配置数据库连接
HOSTNAME = '127.0.0.1'
PORT = '3306'
USERNAME = 'root'
PASSWORD = '123456'
DATABASE = 'case_base'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 禁用修改跟踪

# 初始化数据库
db.init_app(app)

# 初始化路由
init_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
