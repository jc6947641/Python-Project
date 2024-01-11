# routes.py

from flask import render_template,jsonify,request,url_for,redirect
from models import Cargo,db

def get_data_routes(app):
    @app.route('/')
    def home():
        return render_template('login.html')
    @app.route('/index')
    def index():
        # Fetch all cargo records from the database
        cargo_list = Cargo.query.all()
        # Render the index.html template with cargo data
        return render_template('index.html', cargo_list=cargo_list)

    @app.route('/delete_cargo/<int:cargo_id>', methods=['POST'])
    def delete_cargo(cargo_id):
        cargo_to_delete = Cargo.query.get(cargo_id)

        if cargo_to_delete:
            db.session.delete(cargo_to_delete)
            db.session.commit()
            message = f"成功删除货物(ID: {cargo_id})！"
            return jsonify({'success': True, 'message': message})
        else:
            message = f"删除失败，找不到货物(ID: {cargo_id})。"
            return jsonify({'success': False, 'message': message})

    return app
def insert_cargo(app):
    @app.route('/insert_cargo', methods=['GET', 'POST'])
    def insert_cargo_route():
        if request.method == 'POST':
            # 获取从表单提交的数据
            cargo_data = {
                'id': request.form['id'],
                'name': request.form['name'],
                'num': request.form['num'],
                'owner_id': request.form['owner_id'],
                'store_id': request.form['store_id']
            }

            # Check if a Cargo with the same ID exists
            existing_cargo = Cargo.query.filter_by(id=cargo_data['id']).first()
            if existing_cargo:
                return render_template('insert_cargo.html', error="仓库中已经有相同的id的物品.")

            # Check if the specified store_id exists in the Cargo table
            existing_store = Cargo.query.filter_by(store_id=cargo_data['store_id']).first()
            if not existing_store:
                return render_template('insert_cargo.html', error="没有该仓库.")

            # 创建 Cargo 对象并插入到数据库
            new_cargo = Cargo(**cargo_data)
            db.session.add(new_cargo)
            db.session.commit()

            return redirect(url_for('index'))

        return render_template('insert_cargo.html')

    return app
