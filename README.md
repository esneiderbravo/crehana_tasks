# Crehana Tasks

A FastAPI-based microservice for managing users, task lists, and tasks, designed for scalability and maintainability.

## Features

- User registration and authentication (JWT)
- CRUD operations for task lists and tasks
- GraphQL integration for data operations
- Dockerized for easy deployment
- Asynchronous endpoints for high performance

## Tech Stack

- Python 3.11
- FastAPI
- SQLAlchemy (with Alembic for migrations)
- PostgreSQL (via Docker)
- GraphQL (client integration)
- Poetry (dependency management)
- Pytest (testing)

## Project Structure
```
crehana_tasks/ 
├── src/ 
│ ├── api/ # FastAPI routers 
│ ├── application/ # Auth and application logic 
│ ├── controllers/ # Business logic │ 
├── domain/ # DB models │ 
├── infrastructure/ # DB and GraphQL client 
│ └── services/ # GraphQL service layer 
├── tests/ # Pytest test suite 
├── alembic/ # DB migrations 
├── Dockerfile 
├── docker-compose.yml 
├── pyproject.toml 
├── README.md 
└── DECISION_LOG.md
```

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.11
- Poetry

# Setup

1. **Clone the repository:**
   ```sh
   git clone https://github.com/esneiderbravo/crehana_tasks.git
   cd crehana_tasks
   

# Install dependencies:

```sh
poetry install
```

# Start the application, database and graphql containers (with Docker):
```sh
docker compose up --build
```

# Run database migrations:

```sh
alembic upgrade head
```

# Running Tests

```sh
poetry run pytest
```

# Migrations
Use Alembic for database migrations:
```sh
alembic revision --autogenerate -m "message"
alembic upgrade head
```

# License
MIT License