from flask import render_template, request
from db.connect_db import db
from db.models import Product
from sqlalchemy import desc

def shop_index():
    categories = db.session.query(Product.category).distinct().all()
    categories = [category[0] for category in categories]
    latest_promoted_products = (db.session.query(Product).filter(Product.promotion != "0").
                                order_by(desc(Product.id)).limit(10).all())
    return render_template('index.html',
                           categories=categories,
                           latest_products=latest_promoted_products)