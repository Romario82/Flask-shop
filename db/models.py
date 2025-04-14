from db.connect_db import db
from datetime import datetime
from sqlalchemy import Numeric


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    orders = db.relationship('Order', backref='user', lazy=True)


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(Numeric(10, 2), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    stock = db.Column(db.Integer, default=0)
    manufacturer = db.Column(db.String(80), nullable=False)
    characteristics = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    seo_title = db.Column(db.String(80), nullable=True)
    seo_description = db.Column(db.String(200), nullable=True)
    promotion = db.Column(db.String(80), nullable=True)
    image = db.Column(db.String(80), nullable=True)
    order_items = db.relationship('OrderItem', backref='product', lazy=True)

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow())
    total = db.Column(db.Float, nullable=False)
    items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    __tablename__ = 'order_item'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

def create_db(app):
    with app.app_context():
        db.create_all()