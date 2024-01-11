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

    @app.route('/insert_cargo', methods=['GET', 'POST'])
    def insert_cargo():

        if request.method == 'POST':
            # Get data from the form
            id = request.form.get('id')
            name = request.form.get('name')
            num = request.form.get('num')
            owner_id = request.form.get('owner_id')
            store_id = request.form.get('store_id')

            new_cargo = Cargo(id = id ,name=name, num=num, owner_id=owner_id, store_id=store_id)

            # Add the new cargo to the database
            db.session.add(new_cargo)
            db.session.commit()

            message = "成功插入货物！"
            return jsonify({'success': True, 'message': message})

        return render_template('insert_cargo.html')

    return app
