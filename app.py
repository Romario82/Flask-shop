from flask import Flask, render_template
from routes.setup_routes import setup_routes
from db.config import Config
from db.connect_db import db
from db.models import create_db
from db.models import Product


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        create_db(app)

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