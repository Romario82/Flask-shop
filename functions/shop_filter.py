from flask import render_template, request
from db.connect_db import db
from db.models import Product
from sqlalchemy.sql import func


def shop_filter(category_name):
    categories = db.session.query(Product.category).distinct().all()
    categories = [category[0] for category in categories]

    manufacturers = db.session.query(Product.manufacturer).filter_by(category=category_name).distinct().all()
    manufacturers = [manufacturer[0] for manufacturer in manufacturers]

    max_price = db.session.query(func.max(Product.price)).filter(Product.category == category_name).scalar()
    min_pr = request.args.get('min_price', type=float)
    max_pr = request.args.get('max_price', type=float)
    manufacturer_filter = request.args.get('manufacturer')
    sort_order = request.args.get('sort')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 9, type=int)
    products = None
    id = request.args.get('')

    if manufacturer_filter:
        products = db.session.query(Product).filter(Product.category == category_name,
                                                    Product.manufacturer == manufacturer_filter)
    if sort_order == 'price_asc':
        products = db.session.query(Product).filter(Product.category == category_name).order_by(Product.price.asc())
    if sort_order == 'price_desc':
        products = db.session.query(Product).filter(Product.category == category_name).order_by(Product.price.desc())
    if min_pr == 0:
        products = db.session.query(Product).filter(Product.category == category_name,
                                                    Product.price <= max_pr).order_by(Product.price.asc())
    if min_pr is not None and min_pr >= 500.01:
        products = db.session.query(Product).filter(Product.category == category_name,
                                                    Product.price >= min_pr).order_by(Product.price.asc())

    if manufacturer_filter == None and sort_order == None and min_pr == None and max_pr == None:
        products = db.session.query(Product).filter(Product.category == category_name)

    if products is not None:
        pagination = products.paginate(page=page, per_page=per_page, error_out=False)
        products = pagination.items
    else:
        pagination = db.session.query(Product).filter(Product.category == category_name).paginate(page=page,
                                                                                                  per_page=per_page,
                                                                                                  error_out=False)
        products = pagination.items

    return render_template(
        'shop.html', id=id,
        products=products,
        categories=categories,
        manufacturers=manufacturers,
        category_name=category_name,
        max_price=max_price,
        pagination=pagination)