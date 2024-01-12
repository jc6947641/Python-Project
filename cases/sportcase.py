from flask import render_template,jsonify,request,url_for,redirect,session
from models import Cargo,db

def go_sportcase(app):
    @app.route('/sport')
    def sport():
        # Get the user_id from the session
        user_id = session.get('user_id')

        # Check if user_id is present in the session
        if user_id is not None:
            # Fetch cargo records from the database where owner_id is equal to user_id
            cargo_list = Cargo.query.filter_by(owner_id=user_id, store_id='运动器材').all()

            # Get the maximum ID value from the Cargo records
            max_id = Cargo.query.with_entities(Cargo.id).order_by(Cargo.id.desc()).first()

            # Extract the maximum ID value or default to 0 if there are no cargo records
            max_id_value = max_id[0] if max_id else 0

            # Render the index.html template with cargo data and max_id_value
            return render_template('sport.html', cargo_list=cargo_list, max_id_value=max_id_value)
        else:
            # If user_id is not present in the session, redirect to the login page or handle it accordingly
            return redirect(url_for('login'))

    @app.route('/insert_sport_cargo', methods=['GET', 'POST'])
    def insert_sport_cargo():
        user_id = session.get('user_id')
        print(user_id)
        if request.method == 'POST':
            # Get data from the form
            name = request.form.get('name')
            num = int(request.form.get('num'))  # Convert the input to an integer
            owner_id = user_id
            store_id = '运动器材'

            # Check if the quantity is greater than 0
            if num <= 0:
                return render_template('insert_food_cargo.html', error="Quantity must be greater than 0")

            # 获取当前物品最大的ID值
            max_id = Cargo.query.with_entities(Cargo.id).order_by(Cargo.id.desc()).first()

            # 计算ID
            new_id = max_id[0] + 1 if max_id else 1

            new_cargo = Cargo(id=new_id, name=name, num=num, owner_id=owner_id, store_id=store_id)

            # 将物品添加到数据库表Cargo
            db.session.add(new_cargo)
            db.session.commit()

            # 回到index页面
            return redirect(url_for('sport'))

        return render_template('insert_sport_cargo.html')