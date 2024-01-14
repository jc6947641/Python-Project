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

    @app.route('/search', methods=['GET', 'POST'])
    def search_food():
        if request.method == 'POST':
            query = request.form.get('keyword')
            user_id = session.get('user_id')  # Get the current user's ID from the session

            # When using filter, you can combine conditions using and_ from SQLAlchemy
            cargo_list = Cargo.query.filter(Cargo.name.contains(query), Cargo.owner_id == user_id).all()

            # If matching cargos are found, add their names and IDs to a dictionary and pass it to the template
            return render_template('search.html', cargo_list=cargo_list, query=query)
        else:
            query = request.args.get('search_query')  # Get the query parameter
            if not query:
                message = "搜索查询为空。"
                return render_template('search.html', message=message)

            # Again, use and_ to combine conditions
            user_id = session.get('user_id')
            cargo_list = Cargo.query.filter(Cargo.name.contains(query), Cargo.owner_id == user_id).all()

            if not cargo_list:
                message = f"没有找到名称包含 '{query}' 的货物。"
                return render_template('search.html', message=message)

            return render_template('search.html', cargo_list=cargo_list, query=query)


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class SearchForm(FlaskForm):
    keyword = StringField('请输入产品名称...')
    submit = SubmitField('查找产品')






