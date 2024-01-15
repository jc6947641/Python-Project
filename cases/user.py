from flask import render_template,jsonify,request,url_for,redirect,session,flash
from models import User,db

def go_user(app):

    @app.route('/user')
    def user():
        # Fetch all cargo records from the database
        user_id = session.get('user_id')
        print(user_id)
        user_list = User.query.filter_by(id=user_id).all()

        return render_template('user.html', user_list=user_list)

    @app.route('/alter_user', methods=['POST'])
    def alter_user():
        user_id = session.get('user_id')

        # 获取POST请求中的用户信息
        new_user_id = request.form.get('newUserId')
        new_name = request.form.get('newName')
        new_address = request.form.get('newAddress')
        new_tel = request.form.get('newTel')

        # 根据用户ID更新用户信息
        user = User.query.filter_by(id=new_user_id).first()
        if user:
            user.name = new_name
            user.address = new_address
            user.tel = new_tel
            db.session.commit()
            flash('用户信息更新成功。')
        else:
            flash('未找到用户。')

        return redirect(url_for('homelist'))