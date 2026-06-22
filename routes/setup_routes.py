from flask import redirect, url_for
from routes.views_routs_shop import shop_routs
from routes.views_routs_admin import admin_routs


def redirect_to_index():
    return redirect(url_for('index'), code=301)


def redirect_to_checkout():
    return redirect(url_for('checkout'), code=301)


def setup_routes(app):
    app.add_url_rule('/', view_func=shop_routs.index_rout, endpoint='index')
    app.add_url_rule('/index.html', view_func=redirect_to_index, endpoint='index_html')
    app.add_url_rule('/index', view_func=redirect_to_index, endpoint='index_redirect')
    app.add_url_rule('/home', view_func=redirect_to_index, endpoint='home_redirect')
    app.add_url_rule('/get_product_details/<int:product_id>', view_func=shop_routs.get_product_details, methods=['GET'])
    app.add_url_rule('/uploads/<filename>', view_func=shop_routs.uploaded_file)
    app.add_url_rule('/shop/<category_name>', view_func=shop_routs.shop)
    app.add_url_rule('/shop/product_details/<name>', view_func=shop_routs.product_details, methods=['GET'])
    app.add_url_rule('/shop/cart', view_func=shop_routs.cart, endpoint='cart')
    app.add_url_rule('/shop/add_to_cart', view_func=shop_routs.add_to_cart, methods=['POST'], endpoint='add_to_cart')
    app.add_url_rule('/shop/remove_from_cart', view_func=shop_routs.remove_from_cart, methods=['POST'], endpoint='remove_from_cart')
    app.add_url_rule('/shop/update_cart_quantity', view_func=shop_routs.update_cart_quantity, methods=['POST'], endpoint='update_cart_quantity')
    app.add_url_rule('/checkout', view_func=shop_routs.checkout, methods=['GET', 'POST'], endpoint='checkout')
    app.add_url_rule('/checkout.html', view_func=redirect_to_checkout, endpoint='checkout_html_redirect')
    app.add_url_rule('/checkout/success', view_func=shop_routs.checkout_success, endpoint='checkout_success')

    #app.add_url_rule('/category/<category_name>', view_func=shop_routs.category)

    app.add_url_rule('/admin-panel', view_func=admin_routs.login_admin_rout, methods=['GET', 'POST'], endpoint='admin_panel_login')
    app.add_url_rule('/admin-panel/logout', view_func=admin_routs.logout_admin_rout, endpoint='admin_panel_logout')
    app.add_url_rule('/admin-panel/home', view_func=admin_routs.home_admin_rout, endpoint='admin_panel_home')
    app.add_url_rule('/admin-panel/products', view_func=admin_routs.product_admin_rout, methods=['GET', 'POST'], endpoint='/admin-panel/products')
    app.add_url_rule('/admin-panel/orders', view_func=admin_routs.order_admin_rout, endpoint='admin_panel_orders')
    app.add_url_rule('/admin-panel/clients', view_func=admin_routs.client_admin_rout, endpoint='admin_panel_clients')
    app.add_url_rule('/admin-panel/statistics', view_func=admin_routs.statistics_admin_rout, endpoint='admin_panel_statistics')
    app.add_url_rule('/admin-panel/import', view_func=admin_routs.import_products, methods=['GET', 'POST'], endpoint='/admin-panel/import')
    app.add_url_rule('/admin-panel/settings', view_func=admin_routs.settings_admin_rout, methods=['GET', 'POST'], endpoint='admin_panel_settings')