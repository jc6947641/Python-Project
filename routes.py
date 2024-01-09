from flask import jsonify, request, render_template
from models import db, Product

def init_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/add_product', methods=['POST'])
    def add_product():
        data = request.json  # 假设前端以 JSON 形式发送数据
        name = data.get('name')
        quantity = data.get('quantity')

        if not name or not quantity:
            return jsonify({'error': 'Name and quantity are required'}), 400

        new_product = Product(name=name, quantity=quantity)
        db.session.add(new_product)
        db.session.commit()

        return jsonify({'message': 'Product added successfully'}), 201

    @app.route('/get_products', methods=['GET'])
    def get_products():
        products = Product.query.all()
        product_list = [{'id': product.id, 'name': product.name, 'quantity': product.quantity} for product in products]
        return jsonify({'products': product_list})

    @app.route('/delete_product/<int:product_id>', methods=['DELETE'])
    def delete_product(product_id):
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        db.session.delete(product)
        db.session.commit()

        return jsonify({'message': 'Product deleted successfully'})
