from flask import Flask
app = Flask(__name__)
from flask import render_template, request, redirect, url_for, session
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
                # Login successful, get the user ID
                user_id = user.id
                session['user_id'] = user_id

                # 重定向到 index.html 或任何其他路由
                return redirect(url_for('homelist'))

                # Redirect to index.html or any other route with the user ID
                return redirect(url_for('homelist', user_id=user_id))
            else:
                # Login failed, show an error message
                error_message = "Invalid credentials. Please try again."
                return render_template('login.html', error_message=error_message)

        # If it's a GET request, render the login form
        return render_template('login.html')

    # Define your other routes here
def register(app):
    @app.route('/register', methods=['GET', 'POST'], endpoint='register')
    def register_view():
        if request.method == 'POST':
            # 获取表单数据
            account = request.form['account']
            password = request.form['password']
            name = request.form['name']
            address = request.form['address']
            tel = request.form['tel']

            # 检查数据库中是否已存在该用户
            user = User.query.filter_by(account=account).first()

            if user:
                # 如果用户已存在，显示错误信息
                error_message = "Account already exists. Please log in."
                return render_template('register.html', error_message=error_message)
            else:
                # 如果用户不存在，创建新用户并保存到数据库
                new_user = User(account=account, name = name,password=password,address = address,tel = tel)
                db.session.add(new_user)
                db.session.commit()

                # 注册成功，重定向到登录页面
                return redirect(url_for('login'))
        else:
             # 如果是GET请求，渲染注册表单
            return render_template('register.html')