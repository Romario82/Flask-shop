from flask import Flask, render_template, session
import uuid
from routes.setup_routes import setup_routes
from db.config import Config
from db.connect_db import db
from db.models import create_db, Product, CartItem
from functions.site_settings import get_site_settings, settings_to_dict


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        create_db(app)

    @app.before_request
    def ensure_cart_id():
        if 'cart_id' not in session:
            session['cart_id'] = str(uuid.uuid4())

    @app.context_processor
    def inject_site_settings():
        try:
            return {'site_settings': settings_to_dict(get_site_settings())}
        except Exception:
            from functions.site_settings import DEFAULTS
            return {'site_settings': DEFAULTS}

    @app.context_processor
    def inject_cart():
        cart_id = session.get('cart_id')
        if not cart_id:
            return {'cart_items': [], 'cart_count': 0, 'cart_total': 0.0}
        
        cart_items = CartItem.query.filter_by(cart_id=cart_id).all()
        cart_count = sum(item.quantity for item in cart_items)
        cart_total = sum(item.product.effective_price * item.quantity for item in cart_items)
        cart_total = round(cart_total, 2)
        
        return {
            'cart_items': cart_items,
            'cart_count': cart_count,
            'cart_total': cart_total
        }

    setup_routes(app)

    @app.errorhandler(404)
    def page_not_found(e):
        categories = db.session.query(Product.category).distinct().all()
        categories = [category[0] for category in categories]
        return render_template('404.html', categories=categories), 404

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)