from sqlalchemy.orm import Session
from . import models, schemas

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def update_product(db: Session, product_id: int, product: schemas.ProductUpdate):
    db_product = get_product(db, product_id)
    if db_product:
        for key, value in product.dict().items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product

def search_products(db: Session, query: str):
    return db.query(models.Product).filter(
        (models.Product.name.contains(query)) |
        (models.Product.description.contains(query)) |
        (models.Product.category.contains(query))
    ).all()

def increment_sales(db: Session, product_id: int):
    db_product = get_product(db, product_id)
    if db_product:
        db_product.sales_count += 1
        db.commit()
        db.refresh(db_product)
    return db_product

def get_popular_products(db: Session, limit: int = 10):
    return db.query(models.Product).order_by(models.Product.sales_count.desc()).limit(limit).all()

