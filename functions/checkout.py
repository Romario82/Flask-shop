import secrets

from flask import flash, redirect, session, url_for
from werkzeug.security import generate_password_hash

from db.connect_db import db
from db.models import CartItem, Order, OrderItem, Product, User
from functions.checkout_form import CheckoutForm


def get_cart_items():
    cart_id = session.get('cart_id')
    if not cart_id:
        return []
    return CartItem.query.filter_by(cart_id=cart_id).all()


def get_or_create_customer(email, customer_name):
    user = User.query.filter_by(email=email).first()
    if user:
        return user

    base_username = email.split('@')[0][:40]
    username = base_username
    suffix = 1
    while User.query.filter_by(username=username).first():
        username = f'{base_username}{suffix}'
        suffix += 1

    user = User(
        username=username,
        email=email,
        password=generate_password_hash(secrets.token_urlsafe(16)),
    )
    db.session.add(user)
    db.session.flush()
    return user


def process_checkout(form: CheckoutForm, cart_items):
    for item in cart_items:
        product = item.product
        if product.stock is not None and product.stock < item.quantity:
            flash(
                f'Not enough stock for "{product.name}". Available: {product.stock or 0}.',
                'error',
            )
            return redirect(url_for('cart'))

    total = round(sum(item.product.effective_price * item.quantity for item in cart_items), 2)
    user = get_or_create_customer(form.email.data.strip(), form.customer_name.data.strip())

    order = Order(
        user_id=user.id,
        total=total,
        customer_name=form.customer_name.data.strip(),
        phone=form.phone.data.strip(),
        address=form.address.data.strip(),
        notes=(form.notes.data or '').strip() or None,
        status='new',
    )
    db.session.add(order)
    db.session.flush()

    for item in cart_items:
        product = item.product
        db.session.add(OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity,
            price=item.product.effective_price,
        ))
        if product.stock is not None:
            product.stock = max(0, product.stock - item.quantity)

    cart_id = session.get('cart_id')
    CartItem.query.filter_by(cart_id=cart_id).delete()
    db.session.commit()

    session['last_order_id'] = order.id
    return redirect(url_for('checkout_success'))
