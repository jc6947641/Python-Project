from flask import Flask
from models import db
from login import userpass, register  # 导入新的函数
from routes import get_data_routes
from cases.foodcase import go_foodcase
from cases.bookcase import go_bookcase
from cases.sportcase import go_sportcase
from cases.medicinecase import go_medicinecase
from cases.user import go_user
from cases.search_function import go_search_function
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
go_foodcase(app)  # 食品仓库
go_bookcase(app)  # 书籍仓库
go_sportcase(app)  # 运动器材仓库
go_medicinecase(app)
go_user(app)
go_search_function(app)


if __name__ == '__main__':
    app.run(debug=True)