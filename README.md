# Expense Tracker API

A simple RESTful API built with FastAPI to manage personal expenses. It includes user authentication, CRUD operations for expenses, and date-based filtering.

## Features

- **User Authentication**: Secure user registration and login using JWT access tokens.
- **Expense Management**: Full CRUD (Create, Read, Update, Delete) functionality for user-specific expenses.
- **Expense Filtering**: Filter expenses by date ranges, including presets like "last week," "last month," "last 3 months," or a custom date range.
- **Database Initialization**: Automatically creates database tables and populates the database with a test user and sample data on the first run.
- **Data Validation**: Uses Pydantic models for request and response data validation.

## Technologies Used

- **[FastAPI](https://fastapi.tiangolo.com/)**: The main web framework for building the API.
- **[SQLAlchemy](https://www.sqlalchemy.org/)**: The SQL toolkit and Object Relational Mapper (ORM) used for database interaction.
- **[Pydantic](https://www.google.com/search?q=https://docs.pydantic.dev/)**: For data validation and settings management.
- **[Uvicorn](https://www.uvicorn.org/)**: The ASGI server to run the application.
- **[Passlib & python-jose](https://passlib.readthedocs.io/)**: For password hashing and JWT management.
- **[Psycopg2](https://www.psycopg.org/docs/)**: PostgreSQL adapter for Python.
- **[python-dotenv](https://pypi.org/project/python-dotenv/)**: For managing environment variables.

## API Endpoints

All expense-related routes require authentication.

### Authentication (`/auth`)

- **`POST /auth/register`**

  - Registers a new user.
  - Request Body: `UserRegister` schema (username, password, confirm_password).
  - Response: `UserResponse` schema (id, username).

- **`POST /auth/login`**

  - Logs in a user and returns a bearer token.
  - Request Body: OAuth2PasswordRequestForm (username, password).
  - Response: `{ "access_token": "...", "token_type": "bearer" }`.

### Expenses (`/expenses`)

- **`GET /expenses/`**

  - Retrieves a list of all expenses for the authenticated user.
  - Supports filtering with query parameters:
    - `filter`: `last_week`, `last_month`, `last_3_months`, `custom`.
    - `start_date`: (YYYY-MM-DD) - Required if `filter=custom`.
    - `end_date`: (YYYY-MM-DD) - Required if `filter=custom`.
  - Response: `list[ExpenseResponse]`.

- **`POST /expenses/`**

  - Creates a new expense for the authenticated user.
  - Request Body: `ExpenseCreate` schema (description, amount, date, category).
  - Response: `ExpenseResponse`.

- **`GET /expenses/{expense_id}`**

  - Retrieves a specific expense by its ID.
  - Response: `ExpenseResponse`.

- **`PATCH /expenses/{expense_id}`**

  - Partially updates an existing expense.
  - Request Body: `ExpenseUpdate` schema (all fields optional).
  - Response: `ExpenseResponse`.

- **`DELETE /expenses/{expense_id}`**

  - Deletes a specific expense by its ID.
  - Response: `{ "message": "Expense deleted successfully" }`.

## Setup and Installation

1.  **Clone the Repository**

    ```bash
    git clone https://github.com/Trishan0/expense-tracker-api.git
    cd expense-tracker-api
    ```

2.  **Create and Activate a Virtual Environment**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate
    ```

3.  **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Create `.env` File**
    Create a `.env` file in the root directory. This file is ignored by Git. Add the following environment variables:

    ```ini
    DATABASE_URL="postgresql://user:password@hostname:port/database_name"
    SECRET_KEY="your_very_strong_secret_key"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

    _(These variables are required by `api/database.py` and `api/security.py`)_

5.  **Run the Application**

    ```bash
    uvicorn api.main:app --reload
    ```

    The API will be available at `http://localhost:8000`.

## Database Initialization

On the first run, the application will:

1.  Create the `user` and `expense` tables in your database.

2.  If no users exist, it will create a default user:

    - **Username**: `test`
    - **Password**: `test`

3.  It will then populate the `test` user's account with sample expense data from `api/sample_data.json`.

## Project Inspiration

[RoadMap.sh](https://roadmap.sh/projects/expense-tracker-api)
