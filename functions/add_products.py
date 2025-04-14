from db.connect_db import db
from db.models import Product
from flask import render_template, request, redirect, url_for, flash

def add_new_products(form, category=None):
    category = request.args.get('category')

    if form.validate_on_submit():
        new_product = Product(
            name=form.name.data,
            price=form.price.data,
            description=form.description.data,
            stock=form.stock.data,
            manufacturer=form.manufacturer.data,
            characteristics=form.characteristics.data,
            category=form.category.data,
            seo_title=form.seo_title.data,
            seo_description=form.seo_description.data,
            promotion=form.promotion.data,
            image=form.image.data
        )
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('/admin-panel/products'))

    if request.method == 'POST' and 'delete_product_id' in request.form:
        product_id = request.form['delete_product_id']
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        flash('Product has been deleted successfully', 'success')
        return redirect(url_for('/admin-panel/products'))

    if request.method == 'POST' and 'edit_product_id' in request.form:
        product_id = request.form['edit_product_id']
        product = Product.query.get_or_404(product_id)
        product.name = request.form['name']
        product.price = request.form['price']
        product.description = request.form['description']
        product.stock = int(request.form['stock'])
        product.manufacturer = request.form['manufacturer']
        product.characteristics = request.form['characteristics']
        product.category = request.form['category']
        product.seo_title = request.form['seo_title']
        product.seo_description = request.form['seo_description']
        product.promotion = request.form['promotion']
        product.image = request.form['image']

        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('/admin-panel/products'))

    categories = db.session.query(Product.category.distinct()).all()
    categories = [category[0] for category in categories]

    if category:
        products = Product.query.filter_by(category=category).all()
    else:
        products = Product.query.all()
    return render_template('products-admin.html', form=form, products=products, categories=categories, current_category=category)