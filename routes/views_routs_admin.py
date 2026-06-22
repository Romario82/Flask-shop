from flask import render_template, request, redirect, url_for, flash, session
from db.connect_db import db
from db.models import Order
from functions.upload_form import UploadForm, AddProductForm
from functions.import_products import import_products
from functions.add_products import add_new_products
from functions.admin_stats import get_dashboard_stats, get_clients_data, get_order_statistics
from functions.site_settings import get_site_settings
from functions.settings_form import SeoSettingsForm
from functions.admin_auth import (
    admin_login_required,
    login_admin,
    logout_admin,
    get_admin_users,
    create_admin_user,
    delete_admin_user,
)
from functions.admin_forms import AdminLoginForm, AddAdminUserForm
from werkzeug.utils import secure_filename
from db.config import Config
import os


class AdminRouts:
    @staticmethod
    def login_admin_rout():
        if session.get('admin_user_id'):
            return redirect(url_for('admin_panel_home'))

        form = AdminLoginForm()
        if form.validate_on_submit():
            if login_admin(form.username.data.strip(), form.password.data):
                return redirect(url_for('admin_panel_home'))
            flash('Invalid username or password.', 'error')

        return render_template('login-admin.html', form=form)

    @staticmethod
    def logout_admin_rout():
        logout_admin()
        flash('You have been signed out.', 'success')
        return redirect(url_for('admin_panel_login'))

    @staticmethod
    @admin_login_required
    def home_admin_rout():
        stats = get_dashboard_stats()
        return render_template('index-admin.html', **stats)

    @staticmethod
    @admin_login_required
    def product_admin_rout():
        form = AddProductForm()
        category = request.args.get('category')
        return add_new_products(form, category)

    @staticmethod
    @admin_login_required
    def order_admin_rout():
        orders = Order.query.order_by(Order.order_date.desc()).all()
        return render_template('order-admin.html', orders=orders)

    @staticmethod
    @admin_login_required
    def client_admin_rout():
        clients = get_clients_data()
        return render_template('client-admin.html', clients=clients)

    @staticmethod
    @admin_login_required
    def statistics_admin_rout():
        stats = get_order_statistics()
        return render_template('statistics-admin.html', **stats)

    @staticmethod
    @admin_login_required
    def import_products():
        form = UploadForm()
        if form.validate_on_submit():
            file = form.file.data
            filename = secure_filename(file.filename)
            file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
            file.save(file_path)
            import_products(file_path)
            flash('File successfully uploaded')
            return redirect(url_for('/admin-panel/import'))
        return render_template('import-admin.html', form=form)

    @staticmethod
    @admin_login_required
    def settings_admin_rout():
        settings = get_site_settings()
        seo_form = SeoSettingsForm(obj=settings)
        user_form = AddAdminUserForm(prefix='user')
        admin_users = get_admin_users()
        current_admin_id = session.get('admin_user_id')

        if request.method == 'POST':
            if 'delete_user_id' in request.form:
                user_id = request.form.get('delete_user_id', type=int)
                ok, message = delete_admin_user(user_id, current_admin_id)
                flash(message, 'success' if ok else 'error')
                return redirect(url_for('admin_panel_settings'))

            if user_form.submit.data and user_form.validate():
                ok, message = create_admin_user(
                    user_form.username.data,
                    user_form.password.data,
                )
                flash(message, 'success' if ok else 'error')
                return redirect(url_for('admin_panel_settings'))

            if seo_form.validate_on_submit():
                settings.site_name = seo_form.site_name.data.strip()
                settings.default_title = seo_form.default_title.data.strip()
                settings.default_description = seo_form.default_description.data.strip()
                settings.default_keywords = (seo_form.default_keywords.data or '').strip()
                settings.home_title = seo_form.home_title.data.strip()
                settings.home_description = seo_form.home_description.data.strip()
                settings.robots = seo_form.robots.data.strip()
                db.session.commit()
                flash('SEO settings saved successfully.', 'success')
                return redirect(url_for('admin_panel_settings'))

        return render_template(
            'settings-admin.html',
            form=seo_form,
            user_form=user_form,
            admin_users=admin_users,
            current_admin_id=current_admin_id,
        )


admin_routs = AdminRouts()
