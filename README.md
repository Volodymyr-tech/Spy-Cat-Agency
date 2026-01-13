# Spy Cat Agency 🐾🕵️

The project features a built-in web interface served directly by the backend.

### Tech Stack
- **Templating**: HTML + Jinja2 (Server-Side Rendering).
- **Scripts**: Vanilla JavaScript for dynamic interactions.
- **Authentication**: Built-in secure authentication system to manage access to the agency's data.

### Features
- **Web UI**: Manage cats and missions directly from your browser.
- **Form Validation**: Real-time feedback using JavaScript.
- **Protected Routes**: Secure access to sensitive spy data.

### Tech Stack
- **Framework**: FastAPI
- **Database**: PostgreSQL (SQLAlchemy ORM + Alembic migrations)
- **Environment**: Docker & Docker Compose
- **Package Manager**: Poetry

---

## Getting Started

### 1. Environment Setup
Clone the repository and create a `.env` file from the example: ``` .env.example ```


### Run with Docker
```
docker-compose up --build
```
The API will be available at http://localhost:8010/

### API Documentation
Once the server is running, visit:

Swagger UI: http://localhost:8010/docs

ReDoc: http://localhost:8010/redoc

POSTMAN https://documenter.getpostman.com/view/39888354/2sBXVhBpxJ
