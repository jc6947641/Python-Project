from flask import render_template,jsonify,request,url_for,redirect,session
from models import Cargo,db


def go_foodcase(app):

    @app.route('/food')
    def food():
        # Get the user_id from the session
        user_id = session.get('user_id')

        # Check if user_id is present in the session
        if user_id is not None:
            # Fetch cargo records from the database where owner_id is equal to user_id
            cargo_list = Cargo.query.filter_by(owner_id=user_id,store_id = '食品').all()

            # Get the maximum ID value from the Cargo records
            max_id = Cargo.query.with_entities(Cargo.id).order_by(Cargo.id.desc()).first()

            # Extract the maximum ID value or default to 0 if there are no cargo records
            max_id_value = max_id[0] if max_id else 0

            # Render the index.html template with cargo data and max_id_value
            return render_template('food.html', cargo_list=cargo_list, max_id_value=max_id_value)
        else:
            # If user_id is not present in the session, redirect to the login page or handle it accordingly
            return redirect(url_for('login'))

    @app.route('/insert_food_cargo', methods=['GET', 'POST'])
    def insert_food_cargo():
        user_id = session.get('user_id')
        print(user_id)
        if request.method == 'POST':
            # Get data from the form
            name = request.form.get('name')
            num = str(request.form.get('num'))  # Convert the input to an integer
            owner_id = user_id
            store_id = '食品'


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
            return redirect(url_for('food'))

        return render_template('insert_food_cargo.html')
    @app.route('/insert_food', methods=['POST'])
    def insert_food():
        try:
            # 获取数据
            data = request.get_json()
            cargo_id = data.get('cargoId')
            cargo_num = int(data.get('cargoNum'))

            # 获取数据库中的货物记录
            current_cargo = Cargo.query.filter_by(id=cargo_id).first()

            # 更新货物数量
            if current_cargo:
                current_cargo.num += cargo_num
                db.session.commit()

                # 返回成功响应
                return jsonify({'success': True})
            else:
                return jsonify({'success': False, 'error': '货物不存在'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

    @app.route('/deliver_food', methods=['POST'])
    def deliver_food():
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

    @app.route('/search', methods=['GET', 'POST'])
    def search_food():
        # 使用 SQLAlchemy 查询数据库，尝试获取名称包含查询参数的货物


        if request.method == 'POST':
            query = request.form.get('keyword')
            user_id = session.get('user_id')  # 获取当前用户的 ID
            # 在查询时添加一个过滤条件，只选择当前账号的作品
            results = Cargo.query.filter(Cargo.name.contains(query), Cargo.owner_id == user_id).all()
            # 如果找到了匹配的货物，将它们的名称和 ID 作为字典添加到列表中

            return render_template('search.html', results=results)
        else:
            # 如果没有找到匹配的货物，返回一个错误消息
            message = f"没有找到名称包含 '{query}' 的货物。"


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class SearchForm(FlaskForm):
    keyword = StringField('请输入产品名称...')
    submit = SubmitField('查找产品')