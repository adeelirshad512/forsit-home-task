Database Schema
The database uses MySQL and consists of three main tables: products, inventory, and sales. Each table is designed to support the API's functionality with proper indexing for performance and normalization to avoid redundancy.
1. Products Table
Stores information about products available in the e-commerce platform.

Table Name: products
Columns:
id: Integer, Primary Key, Auto-incrementing unique identifier.
name: String(255), Product name (not null).
category: String(100), Product category (not null, indexed for filtering).
price: Float, Product price (not null).


Indexes:
Primary Key: id
Index: idx_product_name on name for fast searches.
Index: category for category-based queries.


Purpose: Stores core product details for sales and inventory operations.

2. Inventory Table
Tracks stock levels and updates for products.

Table Name: inventory
Columns:
id: Integer, Primary Key, Auto-incrementing unique identifier.
product_id: Integer, Foreign Key referencing products.id (not null, indexed).
stock: Integer, Current stock level (not null).
updated_at: DateTime, Timestamp of last update (not null, indexed).


Indexes:
Primary Key: id
Index: idx_inventory_product on product_id for quick lookups.
Index: updated_at for time-based queries.


Purpose: Manages stock levels and supports low-stock alerts.

3. Sales Table
Records sales transactions for revenue and sales analysis.

Table Name: sales
Columns:
id: Integer, Primary Key, Auto-incrementing unique identifier.
product_id: Integer, Foreign Key referencing products.id (not null, indexed).
quantity: Integer, Number of units sold (not null).
total_amount: Float, Total sale amount (not null).
sale_date: DateTime, Date and time of sale (not null, indexed).


Indexes:
Primary Key: id
Index: idx_sale_date_product on sale_date and product_id for efficient filtering.


Purpose: Stores sales data for revenue and trend analysis.

Relationships

Products ↔ Inventory: One-to-one. Each product has one inventory record (product_id foreign key in inventory).
Products ↔ Sales: One-to-many. A product can have multiple sales records (product_id foreign key in sales).

Notes

The schema is normalized to reduce redundancy (e.g., product details are stored only in products).
Indexes are added on frequently queried fields (e.g., category, sale_date) to optimize performance.
A script (scripts/seed_database.py) populates the database with sample data mimicking Amazon/Walmart product sales and inventory.

API Endpoints
The API is built with FastAPI and secured using API key authentication. All endpoints require an X-API-Key header with the value 123 (set in .env for development). Below are the key endpoints with their purpose and cURL examples.
Authentication

Mechanism: API key passed in the X-API-Key header.
Example Header: X-API-Key: 123
Purpose: Restricts access to admin users.

1. Sales Endpoints
Handles sales data retrieval, creation, and revenue analysis.
Create a Sale

Endpoint: POST /sales/
Purpose: Records a new sale.
Request Body:{
  "product_id": 1,
  "quantity": 5,
  "total_amount": 49.95,
  "sale_date": "2025-05-18T12:00:00"
}


Response: Sale details.
cURL:curl -X POST "http://localhost:8000/sales/" \
-H "X-API-Key: 123" \
-H "Content-Type: application/json" \
-d '{"product_id":1,"quantity":5,"total_amount":49.95,"sale_date":"2025-05-18T12:00:00"}'



Get a Sale

Endpoint: GET /sales/{sale_id}
Purpose: Retrieves details of a specific sale.
Response: Sale details.
cURL:curl -X GET "http://localhost:8000/sales/1" \
-H "X-API-Key: 123"



Get Sales (Filtered)

Endpoint: GET /sales/?skip=0&limit=100&start_date=2025-01-01T00:00:00&end_date=2025-05-18T23:59:59&product_id=1&category=electronics
Purpose: Retrieves paginated sales data with optional filters (date range, product, category).
Response: List of sales with pagination metadata.
cURL:curl -X GET "http://localhost:8000/sales/?skip=0&limit=100&start_date=2025-01-01T00:00:00&end_date=2025-05-18T23:59:59&product_id=1&category=electronics" \
-H "X-API-Key: 123"



Get Revenue

Endpoint: GET /sales/revenue/?period=monthly&start_date=2025-01-01T00:00:00&end_date=2025-05-18T23:59:59&category=electronics
Purpose: Analyzes revenue by period (daily, weekly, monthly, annual) with optional filters.
Response: Revenue data grouped by the specified period.
cURL:curl -X GET "http://localhost:8000/sales/revenue/?period=monthly&start_date=2025-01-01T00:00:00&end_date=2025-05-18T23:59:59&category=electronics" \
-H "X-API-Key: 123"



2. Product Endpoints
Manages product registration and retrieval.
Create a Product

Endpoint: POST /products/
Purpose: Registers a new product.
Request Body:{
  "name": "Wireless Mouse",
  "category": "electronics",
  "price": 19.99
}


Response: Product details.
cURL:curl -X POST "http://localhost:8000/products/" \
-H "X-API-Key: 123" \
-H "Content-Type: application/json" \
-d '{"name":"Wireless Mouse","category":"electronics","price":19.99}'



Get a Product

Endpoint: GET /products/{product_id}
Purpose: Retrieves details of a specific product.
Response: Product details.
cURL:curl -X GET "http://localhost:8000/products/1" \
-H "X-API-Key: 123"



Get Products (Paginated)

Endpoint: GET /products/?skip=0&limit=100
Purpose: Retrieves paginated list of products.
Response: List of products with pagination metadata.
cURL:curl -X GET "http://localhost:8000/products/?skip=0&limit=100" \
-H "X-API-Key: 123"



3. Inventory Endpoints
Manages inventory levels and low-stock alerts.
Update Inventory

Endpoint: PUT /inventory/{product_id}
Purpose: Updates stock level for a product.
Request Body:{
  "stock": 50
}


Response: Updated inventory details.
cURL:curl -X PUT "http://localhost:8000/inventory/1" \
-H "X-API-Key: 123" \
-H "Content-Type: application/json" \
-d '{"stock":50}'



Get Inventory

Endpoint: GET /inventory/{product_id}
Purpose: Retrieves current stock level for a product.
Response: Inventory details.
cURL:curl -X GET "http://localhost:8000/inventory/1" \
-H "X-API-Key: 123"



Get Inventory History

Endpoint: GET /inventory/{product_id}/history?skip=0&limit=100
Purpose: Retrieves paginated history of inventory updates for a product.
Response: List of inventory updates with pagination metadata.
cURL:curl -X GET "http://localhost:8000/inventory/1/history?skip=0&limit=100" \
-H "X-API-Key: 123"



Get Low Stock Alerts

Endpoint: GET /inventory/low-stock/?threshold=10
Purpose: Retrieves products with stock below the specified threshold.
Response: List of low-stock products.
cURL:curl -X GET "http://localhost:8000/inventory/low-stock/?threshold=10" \
-H "X-API-Key: 123"



Setup Instructions
The source code is hosted on a public GitHub repository (link to be provided in submission). Follow these steps to set up the project:

Clone the Repository:
git clone <repository_url>
cd fastapi_app


Install Dependencies:
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt


Configure Environment:

Create a .env file in the project root.
Add:DATABASE_URL=mysql://admin:<password>@forsit.caz6o2cmyk17.us-east-1.rds.amazonaws.com:3306/forsit
ENVIRONMENT=development
PROJECT_NAME=FastAPI App
log_level=INFO
API_KEY=123




Populate Database:

Run the seed script to add sample data:python scripts/seed_database.py




Run the Application:

Use the provided run.sh script to start the application:./run.sh


This script activates the virtual environment, sets environment variables, and runs the FastAPI app with Uvicorn on http://localhost:8000.


Access the API:

Open http://localhost:8000/docs for the interactive FastAPI Swagger UI.
Use the cURL commands above with X-API-Key: 123.



Notes

Security: API keys are used for simplicity, as per the task's flexibility on authentication. In production, consider JWT or OAuth for enhanced security.
Logging: A logger is implemented (app/core/logger.py) to track API requests and errors, stored in app/logs/app.log.
Demo Data: The seed script generates realistic data for products, sales, and inventory, mimicking e-commerce platforms like Amazon/Walmart.
No Docker: As per the task, MySQL is assumed to be on AWS RDS, so Docker is not used. However, the codebase is Docker-compatible if needed later.
No Tests: Unit/integration tests were not required for submission, but the code is structured to support testing (e.g., dependency injection via Depends).
Run Script: The run.sh script simplifies starting the application, eliminating the need to manually activate the virtual environment or run Uvicorn commands.

This documentation is intentionally straightforward to meet the task requirements while clearly explaining the database and API functionality. For further details, refer to the GitHub repository's README or contact me.
