# routes.py

from flask import render_template,jsonify,request,url_for,redirect,session
from models import Cargo,db

def get_data_routes(app):
    @app.route('/')
    def home():
        return render_template('login.html')
    @app.route('/homelist')
    def homelist():
        return render_template('homelist.html')

    @app.route('/index')
    def index():
        # Get the user_id from the session
        user_id = session.get('user_id')

        # Check if user_id is present in the session
        if user_id is not None:
            # Fetch cargo records from the database where owner_id is equal to user_id
            cargo_list = Cargo.query.filter_by(owner_id=user_id).all()

            # Get the maximum ID value from the Cargo records
            max_id = Cargo.query.with_entities(Cargo.id).order_by(Cargo.id.desc()).first()

            # Extract the maximum ID value or default to 0 if there are no cargo records
            max_id_value = max_id[0] if max_id else 0

            # Render the index.html template with cargo data and max_id_value
            return render_template('index.html', cargo_list=cargo_list, max_id_value=max_id_value)
        else:
            # If user_id is not present in the session, redirect to the login page or handle it accordingly
            return redirect(url_for('login'))

    @app.route('/delete_cargo/<int:cargo_id>', methods=['POST'])
    def delete_cargo(cargo_id):
        cargo_to_delete = Cargo.query.get(cargo_id)

        if cargo_to_delete:
            # Check if the cargo to be deleted has the maximum ID
            is_max_id = (cargo_id == Cargo.query.with_entities(Cargo.id).order_by(Cargo.id.desc()).first()[0])

            db.session.delete(cargo_to_delete)
            db.session.commit()

            # If the cargo had the maximum ID, update the maximum ID
            if is_max_id:
                max_id = Cargo.query.with_entities(Cargo.id).order_by(Cargo.id.desc()).first()
                new_max_id = max_id[0] - 1 if max_id else 0
                Cargo.query.filter_by(id=new_max_id).update({'id': new_max_id})
                db.session.commit()

            message = f"成功删除货物(ID: {cargo_id})！"
            return jsonify({'success': True, 'message': message})
        else:
            message = f"删除失败，找不到货物(ID: {cargo_id})。"
            return jsonify({'success': False, 'message': message})


    return app
