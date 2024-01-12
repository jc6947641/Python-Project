from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

# 模拟用户登录状态，实际项目中可以使用用户认证系统
logged_in = False

@app.route('/')
def index():
    if logged_in:
        return render_template('homelist.html')
    else:
        return redirect(url_for('login'))

@app.route('/login')
def login():
    global logged_in
    logged_in = True
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    global logged_in
    logged_in = False
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
