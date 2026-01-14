# Spy Cat Agency 🐾🕵️

The project features a built-in web interface served directly by the backend.

### Tech Stack
- **Framework**: FastAPI
- **Templating**: HTML + Jinja2 (Server-Side Rendering).
- **Scripts**: Vanilla JavaScript for dynamic interactions.
- **Authentication**: Built-in secure authentication system to manage access to the agency's data.

- **Environment**: Docker & Docker Compose
- **Package Manager**: Poetry


### Features
- **Web UI**: Manage cats and missions directly from your browser.
- **Form Validation**: Real-time feedback using JavaScript.
- **Protected Routes**: Secure access to sensitive spy data.


---

## Getting Started

### 1. Environment Setup
Clone the repository and create a `.env` file in /app directory from the example: ``` .env.example ```


### Run with Docker
```
docker-compose up --build
```
The API will be available at http://localhost:8010/

### API Documentation
Once the server is running, visit:

Swagger UI: http://localhost:8010/docs

ReDoc: http://localhost:8010/redoc

POSTMAN [https://web.postman.co/workspace/My-Workspace~c205ccd8-820b-4dff-8f06-c11994ef1a1c/collection/39888354-d1eef2b0-ed3c-42c9-96c2-bda104d9ca76?action=share&source=copy-link&creator=39888354](https://web.postman.co/documentation/39888354-d1eef2b0-ed3c-42c9-96c2-bda104d9ca76/publish?workspaceId=c205ccd8-820b-4dff-8f06-c11994ef1a1c&authFlowId=5ad42165-779e-412f-b431-18a6268b88a1)
