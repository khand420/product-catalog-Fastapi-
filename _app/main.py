from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product)

@app.get("/api/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db=db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.put("/api/products/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    db_product = crud.update_product(db=db, product_id=product_id, product=product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.delete("/api/products/{product_id}", response_model=schemas.Product)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.delete_product(db=db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.get("/api/products/search/")
def search_products(query: str, db: Session = Depends(get_db)):
    return crud.search_products(db=db, query=query)

@app.post("/api/products/{product_id}/sell/")
def sell_product(product_id: int, db: Session = Depends(get_db)):
    return crud.increment_sales(db=db, product_id=product_id)

@app.get("/api/products/popular/")
def get_popular_products(limit: int = 10, db: Session = Depends(get_db)):
    popular_products = crud.get_popular_products(db, limit=limit)
    if not popular_products:
        raise HTTPException(status_code=404, detail="No products found")
    return popular_products




# pytest --cov=app tests/
# uvicorn _app.main:_app --reload
# pytest tests/test_api.py
