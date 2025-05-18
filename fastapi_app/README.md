FastAPI E-commerce Admin API
This project is a FastAPI-based backend API for an e-commerce admin dashboard, managing sales, inventory, and products using Python and MySQL (AWS RDS). It was developed as a take-home task for a Back-end Developer position at Forsit.
How to Run

Clone the Repository:
git clone https://github.com/adeelirshad512/forsit-home-task.git
cd forsit-home-task/fastapi_app


Configure Environment:

Ensure a .env file exists in the root directory with the DATABASE_URL. Use the password provided in the email from Kitae Park (kitae@forsit.co.kr) to set up the database connection. The run.sh script will load this file automatically.


Run the Application:

Use the provided run.sh script:./run.sh


The app will start on http://localhost:8000. Access the Swagger UI at http://localhost:8000/docs and use X-API-Key: 123 for requests.



Project Structure
The codebase is organized into modules for clarity (recent refactor: eede444..808b28e on branch refactor/refactor-codebase). Below is the structure:
.
├── app
│   ├── api
│   │   ├── models      # Database models (e.g., inventory.py, product.py, sale.py)
│   │   ├── queries     # Query logic for database operations
│   │   ├── routers     # API route definitions (e.g., inventory.py, product.py, sale.py)
│   │   ├── schemas     # Pydantic schemas for request/response validation
│   │   └── services    # Business logic for API operations
│   ├── config          # Configuration files (e.g., database.py, settings.py)
│   ├── core            # Utilities (e.g., auth.py, logger.py, response.py)
│   ├── logs            # Log files (e.g., app.log)
│   ├── main.py         # Entry point for the FastAPI app
│   └── scripts         # Scripts for seeding demo data (e.g., seed_database.py)
├── Dockerfile          # Dockerfile for containerization (not used)
├── mypy.ini            # MyPy configuration for type checking
├── README.md           # This file
├── requirements.txt    # Python dependencies
└── run.sh              # Script to run the app

For detailed documentation, refer to the submitted PDF (E-commerce_Admin_API_Documentation.pdf).
