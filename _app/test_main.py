# test_main.py
#pytest

import pytest
from httpx import AsyncClient
from app.main import app
from app.database import SessionLocal, engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Product

# Dependency to override the database session in tests
@pytest.fixture(scope="module")
async def async_session():
    async with AsyncSession(engine) as session:
        yield session

@pytest.fixture(scope="module")
async def test_client(async_session: AsyncSession):
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_create_product(test_client: AsyncClient):
    response = await test_client.post("/api/products/", json={
        "name": "Test Product",
        "description": "Description for test product",
        "price": 10.99,
        "inventory_count": 100,
        "category": "Test Category"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Product"
    assert data["description"] == "Description for test product"

@pytest.mark.asyncio
async def test_read_product(test_client: AsyncClient):
    # First, create a product
    response = await test_client.post("/api/products/", json={
        "name": "Another Test Product",
        "description": "Description for another test product",
        "price": 15.99,
        "inventory_count": 50,
        "category": "Test Category"
    })
    product_id = response.json()["id"]

    # Now, read the product
    response = await test_client.get(f"/api/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Another Test Product"
    assert data["description"] == "Description for another test product"

@pytest.mark.asyncio
async def test_update_product(test_client: AsyncClient):
    # First, create a product
    response = await test_client.post("/api/products/", json={
        "name": "Update Test Product",
        "description": "Description for update test product",
        "price": 20.99,
        "inventory_count": 70,
        "category": "Test Category"
    })
    product_id = response.json()["id"]

    # Now, update the product
    response = await test_client.put(f"/api/products/{product_id}", json={
        "name": "Updated Product Name",
        "description": "Updated description",
        "price": 25.99,
        "inventory_count": 80,
        "category": "Updated Category"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Product Name"
    assert data["description"] == "Updated description"

@pytest.mark.asyncio
async def test_delete_product(test_client: AsyncClient):
    # First, create a product
    response = await test_client.post("/api/products/", json={
        "name": "Delete Test Product",
        "description": "Description for delete test product",
        "price": 30.99,
        "inventory_count": 90,
        "category": "Test Category"
    })
    product_id = response.json()["id"]

    # Now, delete the product
    response = await test_client.delete(f"/api/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Delete Test Product"

@pytest.mark.asyncio
async def test_search_products(test_client: AsyncClient):
    # First, create a product
    await test_client.post("/api/products/", json={
        "name": "Search Test Product",
        "description": "Description for search test product",
        "price": 40.99,
        "inventory_count": 60,
        "category": "Test Category"
    })

    # Now, search the product
    response = await test_client.get("/api/products/search/", params={"query": "Search Test Product"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == "Search Test Product"

@pytest.mark.asyncio
async def test_sell_product(test_client: AsyncClient):
    # First, create a product
    response = await test_client.post("/api/products/", json={
        "name": "Sell Test Product",
        "description": "Description for sell test product",
        "price": 50.99,
        "inventory_count": 100,
        "category": "Test Category"
    })
    product_id = response.json()["id"]

    # Now, sell the product
    response = await test_client.post(f"/api/products/{product_id}/sell/", json={"quantity": 5})
    assert response.status_code == 200
    data = response.json()
    assert data["sales_count"] == 5
    assert data["inventory_count"] == 95

@pytest.mark.asyncio
async def test_get_popular_products(test_client: AsyncClient):
    # First, create some products
    for i in range(3):
        await test_client.post("/api/products/", json={
            "name": f"Popular Test Product {i}",
            "description": f"Description for popular test product {i}",
            "price": 60.99 + i,
            "inventory_count": 100 - i,
            "category": "Test Category"
        })

    # Simulate sales to make products popular
    await test_client.post("/api/products/1/sell/", json={"quantity": 10})
    await test_client.post("/api/products/2/sell/", json={"quantity": 20})

    # Now, get popular products
    response = await test_client.get("/api/products/popular/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["sales_count"] >= data[1]["sales_count"]

