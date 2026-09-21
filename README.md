
# 🛒 E-Commerce API

A production-oriented E-Commerce Backend API built using FastAPI, PostgreSQL, SQLAlchemy, Redis, Docker, and Nginx.

## 🚀 Features

- JWT Authentication using OAuth2 Password Flow
- Role-based authorization (Customer/Admin)
- Product and Category management
- Shopping Cart
- Order creation and cancellation
- Order status management
- Product reviews
- Search, filtering, sorting, and pagination
- Redis caching
- File uploads
- Background tasks
- Security headers and CORS
- Docker Compose deployment
- Automated testing with GitHub Actions

## 🛠️ Tech Stack

- Python 3.13
- FastAPI
- PostgreSQL
- SQLAlchemy
- Redis
- Docker & Docker Compose
- Nginx
- Pytest
- GitHub Actions

## 📁 Project Structure

```text
app/
├── models/
├── schemas/
├── routers/
├── services/
├── repositories/
├── dependencies/
├── core/
└── main.py

tests/
Dockerfile
docker-compose.yml
requirements.txt
pytest.ini
```

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd E-Commerce-API
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file with your local database URL, secret key, and other required configuration.

Never commit real secrets to GitHub.

### 5. Run the application

```bash
python -m uvicorn app.main:app --reload
```

## 🐳 Docker Setup

Start the services:

```bash
docker compose up -d --build
```

Stop the services:

```bash
docker compose down
```

Check service status:

```bash
docker compose ps
```

## 📚 API Documentation

After starting the application:

- Swagger UI: `/docs`
- ReDoc: `/redoc`

## 🧪 Running Tests

```bash
python -m pytest -v
```

## 🔐 Security

- JWT-based authentication
- Role-based access control
- Environment-based configuration
- Security response headers
- CORS configuration
- Protected user resources

## 👨‍💻 Author

Lekhana Dama
