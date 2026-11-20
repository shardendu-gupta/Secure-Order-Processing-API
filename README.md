# Secure Order Processing API

A backend application built using **Python, Django REST Framework, and PostgreSQL** to manage products, inventory, and order processing through secure REST APIs.

The project includes JWT authentication, role-based permissions, product management, inventory tracking, stock reservation, and order status management.

## Features

### 1. User Authentication
- User registration
- JWT login and authentication
- Access and refresh token support
- Protected user profile API
- User profile update
- Role-based access control

### 2. Product Management
- Create, retrieve, update, and delete products
- Unique SKU validation
- Product search
- Product ordering
- Pagination
- Soft delete for products

### 3. Inventory Management
- Create and view product inventory
- Track available and reserved stock
- Stock IN, OUT, and SET operations
- Prevent stock reduction below reserved quantity
- Maintain stock movement history

### 4. Order Processing
- Create orders with multiple products
- Validate product availability
- Calculate order totals automatically
- Reserve inventory when an order is created
- Cancel pending orders
- Update order status
- Deduct stock when an order moves to processing
- Restrict customers to viewing their own orders

### 5. Database and Security
- PostgreSQL database
- Django ORM
- Database transactions
- Row-level locking for important stock operations
- Serializer validation
- Role-based API permissions
- Protected endpoints using JWT

## Technology Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- Simple JWT
- python-decouple

## Project Structure

```text
Secure-Order-Processing-API/
│
├── accounts/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── permissions.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── products/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── permissions.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── inventory/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── permissions.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── orders/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── permissions.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── .env.example
├── .gitignore
├── manage.py
└── requirements.txt
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Secure-Order-Processing-API
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory.

```env
SECRET_KEY=your-secret-key
DEBUG=True

DB_NAME=your_database_name
DB_USER=your_database_username
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432
```

Create the PostgreSQL database and configure your database credentials.

### 5. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

## API Endpoints

All endpoints use the `/api/` prefix.

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/accounts/register/` | Register user |
| POST | `/api/accounts/login/` | Login and obtain JWT tokens |
| POST | `/api/accounts/token/refresh/` | Refresh access token |
| GET | `/api/accounts/profile/` | View user profile |
| PUT/PATCH | `/api/accounts/profile/update/` | Update user profile |

### Products

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/products/` | List products |
| POST | `/api/products/create/` | Create product |
| GET | `/api/products/{id}/` | Retrieve product |
| PUT/PATCH | `/api/products/{id}/update/` | Update product |
| DELETE | `/api/products/{id}/delete/` | Soft delete product |

Product search and ordering examples:

```text
/api/products/?search=laptop
/api/products/?ordering=price
/api/products/?page=1&page_size=10
```

### Inventory

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/inventory/` | List inventory |
| POST | `/api/inventory/create/` | Create inventory |
| GET | `/api/inventory/{product_id}/` | View product inventory |
| POST | `/api/inventory/{product_id}/adjust/` | Adjust stock |
| GET | `/api/inventory/{product_id}/movements/` | View stock movement history |

### Orders

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/orders/create/` | Create order |
| GET | `/api/orders/` | List orders |
| GET | `/api/orders/{id}/` | View order details |
| POST | `/api/orders/{id}/cancel/` | Cancel pending order |
| PATCH | `/api/orders/{id}/status/` | Update order status |

## Authentication

Protected endpoints require a JWT access token.

Add the following header to your request:

```text
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## Order Status Workflow

```text
PENDING
   |
   v
CONFIRMED
   |
   v
PROCESSING
   |
   v
SHIPPED
   |
   v
DELIVERED
```

Pending or confirmed orders can also be cancelled according to the implemented status rules.

## User Roles

| Role | Permissions |
|---|---|
| ADMIN | Manage products, inventory, and orders |
| STAFF | Manage products, inventory, and order status |
| CUSTOMER | View products, create orders, and manage own orders |

## Database Transactions

Database transactions and row-level locking are used in important inventory and order operations to help prevent inconsistent stock updates during concurrent requests.

## Future Improvements

- Automated API testing
- Background order notifications
- API documentation using Swagger/OpenAPI
- Docker deployment
- Production deployment

## Author

**Python Backend Developer**

This project was developed as a backend portfolio project to demonstrate practical knowledge of Django REST Framework, PostgreSQL, REST API development, authentication, inventory management, and order processing.
