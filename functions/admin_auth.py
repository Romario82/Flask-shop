from functools import wraps

from flask import redirect, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from db.connect_db import db
from db.models import AdminUser


def admin_login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get('admin_user_id'):
            return redirect(url_for('admin_panel_login'))
        return view(*args, **kwargs)

    return wrapped


def login_admin(username, password):
    admin = AdminUser.query.filter_by(username=username).first()
    if admin and check_password_hash(admin.password_hash, password):
        session['admin_user_id'] = admin.id
        session['admin_username'] = admin.username
        return True
    return False


def logout_admin():
    session.pop('admin_user_id', None)
    session.pop('admin_username', None)


def get_current_admin():
    admin_id = session.get('admin_user_id')
    if not admin_id:
        return None
    return AdminUser.query.get(admin_id)


def ensure_default_admin():
    if AdminUser.query.filter_by(username='admin').first():
        return
    admin = AdminUser(
        username='admin',
        password_hash=generate_password_hash('admin'),
    )
    db.session.add(admin)
    db.session.commit()


def get_admin_users():
    return AdminUser.query.order_by(AdminUser.username).all()


def create_admin_user(username, password):
    username = username.strip()
    if AdminUser.query.filter_by(username=username).first():
        return False, 'User already exists.'
    admin = AdminUser(
        username=username,
        password_hash=generate_password_hash(password),
    )
    db.session.add(admin)
    db.session.commit()
    return True, 'User created successfully.'


def delete_admin_user(user_id, current_admin_id):
    admin = AdminUser.query.get(user_id)
    if not admin:
        return False, 'User not found.'
    if admin.id == current_admin_id:
        return False, 'You cannot delete your own account.'
    if AdminUser.query.count() <= 1:
        return False, 'Cannot delete the last admin user.'
    db.session.delete(admin)
    db.session.commit()
    return True, 'User deleted successfully.'
