from flask import render_template,jsonify,request,url_for,redirect,session
from models import Cargo,db
def go_bookcase(app):
    @app.route('/book')
    def book():
        # Get the user_id from the session
        user_id = session.get('user_id')
        # Check if user_id is present in the session
        if user_id is not None:
            # Fetch cargo records from the database where owner_id is equal to user_id
            cargo_list = Cargo.query.filter_by(owner_id=user_id, store_id='书籍').all()

            # Get the maximum ID value from the Cargo records
            max_id = Cargo.query.with_entities(Cargo.id).order_by(Cargo.id.desc()).first()

            # Extract the maximum ID value or default to 0 if there are no cargo records
            max_id_value = max_id[0] if max_id else 0

            # Render the index.html template with cargo data and max_id_value
            return render_template('book.html', cargo_list=cargo_list, max_id_value=max_id_value)
        else:
            # If user_id is not present in the session, redirect to the login page or handle it accordingly
            return redirect(url_for('login'))

    @app.route('/insert_book_cargo', methods=['GET', 'POST'])
    def insert_book_cargo():
        user_id = session.get('user_id')
        print(user_id)
        if request.method == 'POST':
            try:
                # Get data from the request
                data = request.get_json()
                name = data.get('newCargoName')
                num = int(data.get('newCargoNum'))  # Convert the input to an integer
                owner_id = user_id
                store_id = '书籍'

                # Check if the quantity is greater than 0
                if num <= 0:
                    return render_template('insert_book_cargo.html', error="数量必须大于0")
                existing_cargo = Cargo.query.filter_by(name=name, owner_id=owner_id,store_id = store_id).first()
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

                return redirect(url_for('book'))
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)})

        return render_template('insert_book_cargo.html')

    @app.route('/insert_book', methods=['POST'])
    def insert_book():
        try:
            # Get data from the request
            data = request.get_json()
            cargo_id = data.get('cargoId')
            cargo_num = int(data.get('cargoNum'))  # Convert cargo_num to an integer

            # Retrieve the cargo record from the database using cargo_id
            current_cargo = Cargo.query.filter_by(id=cargo_id).first()

            # Update the cargo quantity
            if current_cargo:
                current_cargo.num += cargo_num

                # Commit the changes to the database
                db.session.commit()

                return jsonify({'success': True})
            else:
                return jsonify({'success': False, 'error': 'Cargo not found'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

    @app.route('/deliver_book', methods=['POST'])
    def deliver_book():
        try:
            # Get data from the request
            data = request.get_json()
            cargo_id = data.get('cargoId')
            delivery_num = int(data.get('deliveryNum'))  # Convert delivery_num to an integer

            # Retrieve the cargo record from the database using cargo_id
            current_cargo = Cargo.query.filter_by(id=cargo_id).first()

            # Check if delivery quantity is valid
            if current_cargo and current_cargo.num - delivery_num >= 0:
                # Update the cargo quantity
                current_cargo.num -= delivery_num

                # Commit the changes to the database
                db.session.commit()

                return jsonify({'success': True})
            else:
                return jsonify({'success': False, 'error': '仓库物品数量不足'})

        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})




