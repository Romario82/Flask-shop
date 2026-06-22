from db.connect_db import db
from datetime import datetime
from sqlalchemy import Numeric, inspect, text


class AdminUser(db.Model):
    __tablename__ = 'admin_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)


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

    @property
    def effective_price(self):
        try:
            price_val = float(self.price)
        except (ValueError, TypeError):
            price_val = 0.0
        try:
            promo_val = float(self.promotion) if self.promotion else 0.0
        except (ValueError, TypeError):
            promo_val = 0.0
        return round(max(0.0, price_val - promo_val), 2)

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False)
    customer_name = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    notes = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(20), default='new', nullable=False)
    items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    __tablename__ = 'order_item'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

class SiteSettings(db.Model):
    __tablename__ = 'site_settings'
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(100), nullable=True)
    default_title = db.Column(db.String(150), nullable=True)
    default_description = db.Column(db.String(300), nullable=True)
    default_keywords = db.Column(db.String(300), nullable=True)
    home_title = db.Column(db.String(150), nullable=True)
    home_description = db.Column(db.String(300), nullable=True)
    robots = db.Column(db.String(50), default='index, follow', nullable=True)


class CartItem(db.Model):
    __tablename__ = 'cart_item'
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.String(100), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    
    product = db.relationship('Product', backref=db.backref('cart_items', lazy=True))

def _migrate_order_columns():
    inspector = inspect(db.engine)
    if 'order' not in inspector.get_table_names():
        return
    existing = {col['name'] for col in inspector.get_columns('order')}
    migrations = {
        'customer_name': 'VARCHAR(100)',
        'phone': 'VARCHAR(50)',
        'address': 'VARCHAR(255)',
        'notes': 'VARCHAR(500)',
        'status': "VARCHAR(20) DEFAULT 'new'",
    }
    for column, col_type in migrations.items():
        if column not in existing:
            db.session.execute(text(f'ALTER TABLE "order" ADD COLUMN {column} {col_type}'))
    db.session.commit()


def create_db(app):
    with app.app_context():
        db.create_all()
        _migrate_order_columns()
        from functions.admin_auth import ensure_default_admin
        ensure_default_admin()