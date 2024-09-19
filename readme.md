
# Product Catalog API

## Overview

This FastAPI application provides a RESTful API for managing products. It includes functionalities to create, read, update, delete, search, sell products, and retrieve popular products based on sales. The application uses SQLAlchemy for database interactions and Pydantic for data validation.

## Features

- **CRUD Operations**: Create, read, update, and delete products.
- **Search Products**: Search products by name, description, or category.
- **Record Sales**: Increment sales count for a product.
- **Get Popular Products**: Retrieve products sorted by sales count.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)
- SQLite or other SQLAlchemy-supported database (configured in `crud.py`)

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/khand420/product-catalog-Fastapi-.git
   cd product-management-api
   ```

2. **Set Up Virtual Environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the Database** (if using SQLite, no additional configuration is required):

   Make sure `DATABASE_URL` in `crud.py` points to your database.

### Usage

1. **Run the Application**:

   ```bash
   uvicorn _app.main:app --reload
   ```

   The API will be available at `http://127.0.0.1:8000`.

2. **API Endpoints**:

   - **Create Product**:
     - `POST /api/products/`
     - Request body: `ProductCreate`
     - Response: `Product`

   - **Read Product**:
     - `GET /api/products/{product_id}`
     - Response: `Product`

   - **Update Product**:
     - `PUT /api/products/{product_id}`
     - Request body: `ProductUpdate`
     - Response: `Product`

   - **Delete Product**:
     - `DELETE /api/products/{product_id}`
     - Response: `Product`

   - **Search Products**:
     - `GET /api/products/search/`
     - Query parameter: `query`
     - Response: List of `Product`

   - **Sell Product**:
     - `POST /api/products/{product_id}/sell/`
     - Response: `Product`

   - **Get Popular Products**:
     - `GET /api/products/popular/`
     - Query parameter: `limit`
     - Response: List of `Product`

3. **Testing**:

   Use Postman or any other API testing tool to interact with the API endpoints. Make sure to send appropriate request bodies and query parameters.

### Example Usage with Postman

- **Create Product**:
  - Method: POST
  - URL: `http://127.0.0.1:8000/api/products/`
  - Body (JSON):
    ```json
    {
      "name": "Sample Product",
      "description": "A sample product description.",
      "price": 29.99,
      "inventory_count": 100,
      "category": "Electronics"
    }
    ```

- **Search Products**:
  - Method: GET
  - URL: `http://127.0.0.1:8000/api/products/search/?query=Sample`
  
- **Sell Product**:
  - Method: POST
  - URL: `http://127.0.0.1:8000/api/products/{product_id}/sell/`
  - Body (JSON):
    ```json
    {
      "quantity": 1
    }
    ```

### Dependencies

- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn (for running the server)

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Contact

For questions or feedback, please contact [khand7661@gmail.com](mailto:khand7661@gmail.com).

