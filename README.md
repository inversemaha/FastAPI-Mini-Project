# Inventory Management API

[![MIT License](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://github.com/inversemaha/FastAPI-Mini-Project/blob/main/LICENSE)
[![repo size](https://img.shields.io/github/repo-size/inversemaha/FastAPI-Mini-Project.svg)](https://github.com/inversemaha/FastAPI-Mini-Project)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.121.0-009688.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791.svg)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red.svg)](https://www.sqlalchemy.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.12+-green.svg)](https://pydantic.dev/)
[![last commit](https://img.shields.io/github/last-commit/inversemaha/FastAPI-Mini-Project.svg)](https://github.com/inversemaha/FastAPI-Mini-Project/commits/main)
[![commit activity](https://img.shields.io/github/commit-activity/y/inversemaha/FastAPI-Mini-Project.svg)](https://github.com/inversemaha/FastAPI-Mini-Project/commits/main)

A comprehensive **Inventory Management System** built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**. This RESTful API provides complete functionality for managing categories, products, suppliers, and stock entries with advanced features like stock tracking, relationship management, and real-time inventory monitoring.

## 🚀 Features

### Core Functionality
- **Categories Management**: Create, read, update, and delete product categories
- **Products Management**: Complete product catalog with pricing, description, and category organization
- **Suppliers Management**: Manage supplier information with contact details and location tracking
- **Stock Management**: Track stock entries, quantities, and inventory movements
- **Inventory Tracking**: Real-time monitoring of stock levels and availability

### Advanced Features
- **Relationship Management**: Automatic loading of related data (categories, suppliers, products)
- **Data Validation**: Comprehensive input validation using Pydantic schemas
- **Stock Monitoring**: Track inventory levels, stock movements, and reorder points
- **Error Handling**: Proper HTTP status codes and error responses
- **Pagination Support**: Efficient handling of large datasets
- **Business Logic**: Stock validation, supplier management, and category organization

### Technical Features
- **FastAPI Framework**: Modern, fast web framework with automatic API documentation
- **PostgreSQL Database**: Robust relational database with ACID compliance
- **SQLAlchemy ORM**: Object-relational mapping with relationship handling
- **Schema Registry**: Advanced pattern for handling forward references
- **Type Safety**: Full type hints and validation throughout the codebase

## 📋 Prerequisites

- **Python 3.9+**
- **PostgreSQL 12+**
- **pip** (Python package manager)

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/inversemaha/FastAPI-Mini-Project.git
cd FastAPI-Mini-Project/Inventory-Management-API
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv myenv

# Activate virtual environment
# On Windows:
myenv\Scripts\activate
# On macOS/Linux:
source myenv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```bash
# Create PostgreSQL database
createdb maha_inventory_db

# Update database connection in config/database.py
# Default connection string: postgresql://postgres:1@localhost:5432/maha_inventory_db
```

### 5. Initialize Database Tables
```bash
# Tables will be created automatically when running the application
# The app creates tables based on SQLAlchemy models on startup
```

## 🚀 Usage

### Starting the Server
```bash
# Start the development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **Main API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Basic API Usage

#### Categories Endpoint
```bash
# Get all categories
GET /categories?skip=0&limit=10

# Get specific category
GET /categories/{category_id}

# Create new category
POST /categories
{
    "name": "Electronics",
    "description": "Electronic devices and components"
}

# Update category
PUT /categories/{category_id}
{
    "name": "Consumer Electronics",
    "description": "Consumer electronic devices"
}

# Delete category
DELETE /categories/{category_id}
```

#### Products Endpoint
```bash
# Get all products with category info
GET /products?skip=0&limit=10

# Get specific product with relationships
GET /products/{product_id}

# Create new product
POST /products
{
    "name": "Wireless Headphones",
    "description": "Bluetooth wireless headphones with noise cancellation",
    "price": 199.99,
    "category_id": 1,
    "sku": "WH-001"
}

# Update product
PUT /products/{product_id}
{
    "name": "Premium Wireless Headphones",
    "price": 249.99
}

# Delete product
DELETE /products/{product_id}
```

#### Suppliers Endpoint
```bash
# Get all suppliers
GET /suppliers?skip=0&limit=10

# Create new supplier
POST /suppliers
{
    "name": "TechCorp Supplies",
    "contact_info": "contact@techcorp.com",
    "address": "123 Tech Street, Silicon Valley, CA"
}

# Update supplier
PUT /suppliers/{supplier_id}
{
    "contact_info": "support@techcorp.com",
    "address": "456 Innovation Ave, Silicon Valley, CA"
}

# Delete supplier
DELETE /suppliers/{supplier_id}
```

#### Stock Entries Endpoint
```bash
# Get all stock entries
GET /stock-entries?skip=0&limit=10

# Create new stock entry
POST /stock-entries
{
    "product_id": 1,
    "supplier_id": 1,
    "quantity": 100,
    "unit_cost": 150.00,
    "entry_date": "2025-11-15T10:00:00"
}

# Update stock entry
PUT /stock-entries/{entry_id}
{
    "quantity": 120,
    "unit_cost": 145.00
}

# Delete stock entry
DELETE /stock-entries/{entry_id}
```

## 📊 Database Schema

### Tables
- **categories**: Product categories (id, name, description)
- **suppliers**: Supplier information (id, name, contact_info, address)
- **products**: Product catalog (id, name, description, price, category_id, sku)
- **stock_entries**: Inventory entries (id, product_id, supplier_id, quantity, unit_cost, entry_date)

### Relationships
- Products ↔ Categories (Many-to-One)
- Stock Entries ↔ Products (Many-to-One)
- Stock Entries ↔ Suppliers (Many-to-One)

## 🏗️ Project Structure

```
Inventory-Management-API/
├── main.py                 # FastAPI application entry point
├── config/
│   └── database.py         # Database configuration and connection
├── models/                 # SQLAlchemy ORM models
│   ├── category.py
│   ├── product.py
│   ├── supplier.py
│   └── stockEntry.py
├── schemas/                # Pydantic schemas for request/response
│   ├── category.py
│   ├── product.py
│   ├── supplier.py
│   └── stockEntry.py
├── routes/                 # API route handlers
│   ├── category.py
│   ├── product.py
│   ├── supplier.py
│   └── stockEntry.py
├── myenv/                  # Virtual environment
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore patterns
└── README.md              # Project documentation
```

## 🔧 Configuration

### Database Configuration
Update `config/database.py` with your database credentials:
```python
db_url = "postgresql://username:password@localhost:5432/database_name"
```

### Environment Variables
Create a `.env` file for sensitive configurations:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
SECRET_KEY=your-secret-key
DEBUG=True
```

## 📦 Dependencies

### Core Dependencies
- **FastAPI**: Modern web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **psycopg2-binary**: PostgreSQL adapter for Python
- **uvicorn**: ASGI server implementation

### Development Dependencies
- **pytest**: Testing framework
- **httpx**: HTTP client for testing
- **black**: Code formatter
- **flake8**: Code linter

## 🧪 Testing

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_products.py
```

## 🚀 Deployment

### Using Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Using Heroku
```bash
# Create Procfile
echo "web: uvicorn main:app --host=0.0.0.0 --port=${PORT:-5000}" > Procfile

# Deploy to Heroku
heroku create your-app-name
git push heroku main
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add docstrings to all functions and classes
- Write unit tests for new features
- Update documentation for API changes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastAPI** for the excellent web framework
- **SQLAlchemy** for powerful ORM capabilities
- **Pydantic** for data validation and settings management
- **PostgreSQL** for reliable database management

## 📞 Support

For support and questions:
- Create an issue in the [GitHub repository](https://github.com/inversemaha/FastAPI-Mini-Project/issues)
- Check the [FastAPI documentation](https://fastapi.tiangolo.com/)
- Review the [SQLAlchemy documentation](https://docs.sqlalchemy.org/)

## 🔮 Future Enhancements

- [ ] User authentication and authorization
- [ ] Advanced inventory analytics and reporting
- [ ] Low stock alerts and notifications
- [ ] Barcode scanning integration
- [ ] Purchase order management
- [ ] Inventory valuation methods (FIFO, LIFO, Weighted Average)
- [ ] Multi-location inventory tracking
- [ ] Export functionality (CSV, PDF, Excel)
- [ ] Dashboard with real-time analytics
- [ ] API rate limiting and caching
- [ ] Automated reorder point calculations
- [ ] Integration with accounting systems

---

**Made with ❤️ using FastAPI and PostgreSQL**
