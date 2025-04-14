from flask import render_template, request, redirect, url_for, flash
from db.connect_db import db
from db.models import User, Product, Order, OrderItem
from functions.upload_form import UploadForm, AddProductForm
from functions.import_products import import_products
from functions.add_products import add_new_products
from werkzeug.utils import secure_filename
from db.config import Config
import os

import pandas as pd

class AdminRouts:
    @staticmethod
    def index_admin_rout():
        return render_template('index-admin.html')

    @staticmethod
    def product_admin_rout():
        form = AddProductForm()
        category = request.args.get('category')
        return add_new_products(form, category)

    @staticmethod
    def order_admin_rout():
        return render_template('order-admin.html')

    @staticmethod
    def client_admin_rout():
        return render_template('client-admin.html')

    @staticmethod
    def statistics_admin_rout():
        return render_template('statistics-admin.html')

    @staticmethod
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
    def settings_admin_rout():
        return render_template('settings-admin.html')


admin_routs = AdminRouts()