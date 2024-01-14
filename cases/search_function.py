from flask import render_template,jsonify,request,url_for,redirect,session
from models import Cargo,db

def go_search_function(app):
    @app.route('/insert_cargo', methods=['POST'])
    def insert_cargo():
        try:
            # 获取数据
            data = request.get_json()
            cargo_id = data.get('cargoId')
            print(cargo_id)
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

    @app.route('/deliver_cargo', methods=['POST'])
    def deliver_cargo():
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