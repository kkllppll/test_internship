# Internship Tech Task - REST API

A REST API built with FastAPI for managing users and articles, with JWT authentication and role-based access control.

## Tech Stack

- **FastAPI** - web framework
- **PostgreSQL** - database
- **SQLAlchemy** - ORM
- **JWT (python-jose)** - authentication
- **Docker + Docker Compose** - containerization
- **pytest** - testing

## Roles

| Role   | Permissions |
|--------|-------------|
| `user`   | Manage own articles, view others' articles |
| `editor` | View and update any article |
| `admin`  | Full access to all articles and users |

> Users can only be created via the seed script or direct DB queries. Roles are assigned on creation.

---

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose installed

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <repo-folder>
```

### 2. Set up environment variables

Copy the example env file and fill in your values:

```bash
cp .env.example .env
```

The `.env` file should contain:

```env
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_db
DATABASE_URL=postgresql://your_user:your_password@db:5432/your_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Build and run

```bash
docker compose up --build
```

The API will be available at: `http://localhost:8000`

---

## Load Initial Data (Seed)

To populate the database with sample users and articles:

```bash
docker compose exec app python seed.py
```

This creates the following users:

| Username | Password   | Role   |
|----------|------------|--------|
| admin    | admin123   | admin  |
| editor   | editor123  | editor |
| user1    | user123    | user   |

---

## Run Tests

Tests use SQLite in-memory — no running database required.

```bash
docker compose exec app pytest tests/ -v --cov=app --cov-report=term-missing
```

Or locally (with dependencies installed):

```bash
pip install -r requirements.txt
pytest tests/ -v --cov=app --cov-report=term-missing
```

---

## API Documentation

Once the app is running, interactive docs are available at:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## API Overview

### Auth
| Method | Endpoint       | Description         | Auth required |
|--------|----------------|---------------------|---------------|
| POST   | /auth/login    | Get JWT token       | No            |

### Users
| Method | Endpoint       | Description              | Auth required |
|--------|----------------|--------------------------|---------------|
| GET    | /users/        | List all users (admin)   | Admin         |
| GET    | /users/me      | Get current user         | Yes           |
| GET    | /users/{id}    | Get user by ID           | Yes           |
| PUT    | /users/{id}    | Update user              | Yes (own/admin)|
| DELETE | /users/{id}    | Delete user (admin)      | Admin         |

### Articles
| Method | Endpoint          | Description                   | Auth required |
|--------|-------------------|-------------------------------|---------------|
| GET    | /articles/        | List all articles             | Yes           |
| GET    | /articles/{id}    | Get article by ID             | Yes           |
| POST   | /articles/        | Create article                | Yes           |
| PUT    | /articles/{id}    | Update article                | Yes (own/editor/admin)|
| DELETE | /articles/{id}    | Delete article                | Yes (own/admin)|

### Status
| Method | Endpoint  | Description         |
|--------|-----------|---------------------|
| GET    | /status   | Health check        |

Query parameters available on list endpoints: `search`, `limit`, `offset`.




---

## Deployment (Google Cloud Run)

The app is containerized with Docker and deployed to Google Cloud Run.

### Requirements

- [gcloud CLI](https://cloud.google.com/sdk/docs/install) installed
- Google Cloud project with billing enabled
- External PostgreSQL (e.g. [Neon](https://neon.tech))

### Steps

```bash
# 1. Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# 2. Enable required services
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com

# 3. Build and push Docker image to Google Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/internship-api

# 4. Deploy to Cloud Run
gcloud run deploy internship-api \
  --image gcr.io/YOUR_PROJECT_ID/internship-api \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated \
  --set-env-vars DATABASE_URL="your_neon_connection_string",SECRET_KEY="your_secret_key",ALGORITHM="HS256",ACCESS_TOKEN_EXPIRE_MINUTES="30"
```

### Seed the production database

After deploying, run the seed script locally pointing to the production database:

```bash
DATABASE_URL="your_neon_connection_string" python seed.py
```

---

## CI/CD

GitHub Actions automatically runs tests on every push and pull request to `main`.

Config: `.github/workflows/tests.yml`
