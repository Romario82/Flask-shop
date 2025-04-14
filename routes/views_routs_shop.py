from flask import render_template
from db.connect_db import db
from db.models import Product
from flask import send_from_directory
from db.config import Config
from flask import jsonify
from functions.shop_filter import shop_filter
from functions.shop_index import shop_index

class ShopRouts:
    @staticmethod
    def index_rout():
        return shop_index()

    @staticmethod
    def uploaded_file(filename):
        return send_from_directory(Config.UPLOAD_FOLDER, filename)

    @staticmethod
    def shop(category_name):
        return shop_filter(category_name)

    @staticmethod
    def product_details(name):
        categories = db.session.query(Product.category).distinct().all()
        categories = [category[0] for category in categories]
        product = db.session.query(Product).filter_by(name=name).first()
        return render_template('product_details.html', product=product, categories=categories, name=name)


    @staticmethod
    def get_product_details(product_id):
        product = Product.query.get(product_id)
        if product:
            return jsonify({
                'name': product.name,
                'price': product.price,
                'promotion': product.promotion,
                'description': product.description,
                'manufacturer': product.manufacturer,
                'image': product.image
            })
        else:
            return jsonify({'error': 'Product not found'}), 404


shop_routs = ShopRouts()