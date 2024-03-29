from flask import render_template,jsonify,request,url_for,redirect,session
from models import Cargo,db

def go_medicinecase(app):
    @app.route('/medicine')
    def medicine():
        # Get the user_id from the session
        user_id = session.get('user_id')

        # Check if user_id is present in the session
        if user_id is not None:
            # Fetch cargo records from the database where owner_id is equal to user_id
            cargo_list = Cargo.query.filter_by(owner_id=user_id, store_id='药品').all()

            # Get the maximum ID value from the Cargo records
            max_id = Cargo.query.with_entities(Cargo.id).order_by(Cargo.id.desc()).first()

            # Extract the maximum ID value or default to 0 if there are no cargo records
            max_id_value = max_id[0] if max_id else 0

            # Render the index.html template with cargo data and max_id_value
            return render_template('medicine.html', cargo_list=cargo_list, max_id_value=max_id_value)
        else:
            # If user_id is not present in the session, redirect to the login page or handle it accordingly
            return redirect(url_for('login'))

    @app.route('/insert_medicine_cargo', methods=['GET', 'POST'])
    def insert_medicine_cargo():
        user_id = session.get('user_id')
        print(user_id)
        if request.method == 'POST':
            try:
                # Get data from the request
                data = request.get_json()
                name = data.get('newCargoName')
                num = int(data.get('newCargoNum'))  # Convert the input to an integer
                owner_id = user_id
                store_id = '药品'

                # Check if the quantity is greater than 0
                if num <= 0:
                    return render_template('insert_medicine_cargo.html', error="数量必须大于0")
                existing_cargo = Cargo.query.filter_by(name=name, owner_id=owner_id, store_id=store_id).first()
                if existing_cargo:
                    return jsonify(
                        {'success': False, 'error': f"仓库中已经有 '{name}' 了，无法再添加"})

                # 获取当前物品最大的ID值
                max_id = Cargo.query.with_entities(Cargo.id).order_by(Cargo.id.desc()).first()

                # 计算ID
                new_id = max_id[0] + 1 if max_id else 1

                new_cargo = Cargo(id=new_id, name=name, num=num, owner_id=owner_id, store_id=store_id)

                # 将物品添加到数据库表Cargo
                db.session.add(new_cargo)
                db.session.commit()

                # 回到index页面
                return jsonify({'success': True})

                return redirect(url_for('medicine'))
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)})

        return render_template('insert_medicine_cargo.html')

