from routes.views_routs_shop import shop_routs
from routes.views_routs_admin import admin_routs

def setup_routes(app):
    app.add_url_rule('/', view_func=shop_routs.index_rout, endpoint='index')
    app.add_url_rule('/index', view_func=shop_routs.index_rout)
    app.add_url_rule('/home', view_func=shop_routs.index_rout)
    app.add_url_rule('/get_product_details/<int:product_id>', view_func=shop_routs.get_product_details, methods=['GET'])
    app.add_url_rule('/uploads/<filename>', view_func=shop_routs.uploaded_file)
    app.add_url_rule('/shop/<category_name>', view_func=shop_routs.shop)
    app.add_url_rule('/shop/product_details/<name>', view_func=shop_routs.product_details, methods=['GET'])

    #app.add_url_rule('/category/<category_name>', view_func=shop_routs.category)

    app.add_url_rule('/admin-panel', view_func=admin_routs.index_admin_rout, endpoint='admin-panel')
    app.add_url_rule('/admin-panel/products', view_func=admin_routs.product_admin_rout, methods=['GET', 'POST'], endpoint='/admin-panel/products')
    app.add_url_rule('/admin-panel/orders', view_func=admin_routs.order_admin_rout)
    app.add_url_rule('/admin-panel/clients', view_func=admin_routs.client_admin_rout)
    app.add_url_rule('/admin-panel/statistics', view_func=admin_routs.statistics_admin_rout)
    app.add_url_rule('/admin-panel/import', view_func=admin_routs.import_products, methods=['GET', 'POST'], endpoint='/admin-panel/import')
    app.add_url_rule('/admin-panel/settings', view_func=admin_routs.settings_admin_rout, methods=['GET', 'POST'])