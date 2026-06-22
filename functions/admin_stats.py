from sqlalchemy import func

from db.connect_db import db
from db.models import Order, OrderItem, Product, User


def get_dashboard_stats():
    total_income = db.session.query(func.coalesce(func.sum(Order.total), 0)).scalar()
    return {
        'goods_count': Product.query.count(),
        'orders_count': Order.query.count(),
        'clients_count': User.query.count(),
        'total_income': round(float(total_income or 0), 2),
        'latest_orders': Order.query.order_by(Order.order_date.desc()).limit(10).all(),
    }


def get_clients_data():
    rows = (
        db.session.query(
            User,
            func.count(Order.id).label('orders_count'),
            func.coalesce(func.sum(Order.total), 0).label('total_spent'),
        )
        .outerjoin(Order, User.id == Order.user_id)
        .group_by(User.id)
        .order_by(func.coalesce(func.sum(Order.total), 0).desc())
        .all()
    )
    return [
        {
            'user': user,
            'orders_count': orders_count,
            'total_spent': round(float(total_spent or 0), 2),
        }
        for user, orders_count, total_spent in rows
    ]


def get_order_statistics():
    total_income = db.session.query(func.coalesce(func.sum(Order.total), 0)).scalar()
    orders_count = Order.query.count()
    avg_order = round(float(total_income or 0) / orders_count, 2) if orders_count else 0

    status_rows = (
        db.session.query(Order.status, func.count(Order.id))
        .group_by(Order.status)
        .order_by(func.count(Order.id).desc())
        .all()
    )

    monthly_rows = (
        db.session.query(
            func.strftime('%Y-%m', Order.order_date).label('month'),
            func.count(Order.id).label('orders_count'),
            func.coalesce(func.sum(Order.total), 0).label('income'),
        )
        .filter(Order.order_date.isnot(None))
        .group_by('month')
        .order_by('month')
        .all()
    )

    top_products = (
        db.session.query(
            Product.name,
            func.sum(OrderItem.quantity).label('qty'),
            func.coalesce(func.sum(OrderItem.quantity * OrderItem.price), 0).label('revenue'),
        )
        .join(OrderItem, Product.id == OrderItem.product_id)
        .group_by(Product.id)
        .order_by(func.sum(OrderItem.quantity).desc())
        .limit(10)
        .all()
    )

    return {
        'total_income': round(float(total_income or 0), 2),
        'orders_count': orders_count,
        'clients_count': User.query.count(),
        'avg_order': avg_order,
        'status_stats': [
            {'status': status or 'unknown', 'count': count}
            for status, count in status_rows
        ],
        'monthly_stats': [
            {
                'month': month,
                'orders_count': orders_count,
                'income': round(float(income or 0), 2),
            }
            for month, orders_count, income in monthly_rows
        ],
        'top_products': [
            {
                'name': name,
                'qty': int(qty or 0),
                'revenue': round(float(revenue or 0), 2),
            }
            for name, qty, revenue in top_products
        ],
    }
