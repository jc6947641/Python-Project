from flask import render_template,jsonify,request,url_for,redirect,session
from models import User,db

def go_user(app):

    @app.route('/user')
    def user():
        # Fetch all cargo records from the database
        user_id = session.get('user_id')
        print(user_id)
        user_list = User.query.filter_by(id=user_id).all()

        return render_template('user.html', user_list=user_list)

    @app.route('/insert_food_cargo', methods=['GET', 'POST'])
    def alter_user():
        user_id = session.get('user_id')
        print(user_id)
        if request.method == 'POST':
            # Get data from the form
            name = request.form.get('name')
            address = str(request.form.get('address'))  # Convert the input to an integer
            tel = int(request.form.get('tel'))



            # 将物品添加到数据库表Cargo
            db.session.add(new_cargo)
            db.session.commit()

            # 回到index页面
            return redirect(url_for('index'))