from flask import render_template, send_from_directory, jsonify, session, request, redirect, url_for, flash
import uuid
from db.connect_db import db
from db.models import Product, CartItem, Order
from db.config import Config
from functions.shop_filter import shop_filter
from functions.shop_index import shop_index
from functions.checkout import get_cart_items, process_checkout
from functions.checkout_form import CheckoutForm

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

    @staticmethod
    def cart():
        categories = db.session.query(Product.category).distinct().all()
        categories = [category[0] for category in categories]
        return render_template('shop-cart.html', categories=categories)

    @staticmethod
    def checkout():
        cart_items = get_cart_items()
        if not cart_items:
            flash('Your cart is empty. Add products before checkout.', 'error')
            return redirect(url_for('cart'))

        categories = db.session.query(Product.category).distinct().all()
        categories = [category[0] for category in categories]
        form = CheckoutForm()

        if form.validate_on_submit():
            return process_checkout(form, cart_items)

        return render_template('checkout.html', categories=categories, form=form)

    @staticmethod
    def checkout_success():
        order_id = session.pop('last_order_id', None)
        order = Order.query.get(order_id) if order_id else None
        categories = db.session.query(Product.category).distinct().all()
        categories = [category[0] for category in categories]
        return render_template('checkout-success.html', categories=categories, order=order)

    @staticmethod
    def add_to_cart():
        product_id = request.form.get('product_id', type=int)
        quantity = request.form.get('quantity', 1, type=int)
        
        if not product_id:
            return redirect(url_for('index'))
            
        product = Product.query.get(product_id)
        if not product:
            return redirect(url_for('index'))
            
        cart_id = session.get('cart_id')
        if not cart_id:
            session['cart_id'] = str(uuid.uuid4())
            cart_id = session['cart_id']
            
        cart_item = CartItem.query.filter_by(cart_id=cart_id, product_id=product_id).first()
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(cart_id=cart_id, product_id=product_id, quantity=quantity)
            db.session.add(cart_item)
            
        db.session.commit()
        return redirect(request.referrer or url_for('cart'))

    @staticmethod
    def remove_from_cart():
        product_id = request.form.get('product_id', type=int)
        cart_id = session.get('cart_id')
        
        if product_id and cart_id:
            cart_item = CartItem.query.filter_by(cart_id=cart_id, product_id=product_id).first()
            if cart_item:
                db.session.delete(cart_item)
                db.session.commit()
                
        return redirect(url_for('cart'))

    @staticmethod
    def update_cart_quantity():
        product_id = request.form.get('product_id', type=int)
        quantity = request.form.get('quantity', type=int)
        cart_id = session.get('cart_id')
        
        if product_id and cart_id and quantity is not None:
            cart_item = CartItem.query.filter_by(cart_id=cart_id, product_id=product_id).first()
            if cart_item:
                if quantity > 0:
                    cart_item.quantity = quantity
                else:
                    db.session.delete(cart_item)
                db.session.commit()
                
        return redirect(url_for('cart'))

shop_routs = ShopRouts()