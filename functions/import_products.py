from db.connect_db import db
import os
import pandas as pd
from db.models import Product

def import_products(file_path):
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)

    for _, row in df.iterrows():
        product = db.session.query(Product).filter_by(name=row['name']).first()

        if product:
            product.price = row['price']
            product.description = row['description']
            product.stock = row['stock']
            product.manufacturer = row['manufacturer']
            product.characteristics = row['characteristics']
            product.category = row['category']
            product.seo_title = row.get('seo_title')
            product.seo_description = row.get('seo_description')
            product.promotion = row.get('promotion')
            product.image = row.get('image')
        else:
            product = Product(
                name=row['name'],
                price=row['price'],
                description=row['description'],
                stock=row['stock'],
                manufacturer=row['manufacturer'],
                characteristics=row['characteristics'],
                category=row['category'],
                seo_title=row.get('seo_title'),
                seo_description=row.get('seo_description'),
                promotion=row.get('promotion'),
                image=row.get('image')
            )
            db.session.add(product)
    db.session.commit()