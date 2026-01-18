# Backend Implementation - Hackathon Phase II

## Overview
This is a secure, production-ready FastAPI backend for a Todo application with JWT authentication and Neon PostgreSQL integration.

## Architecture
- **Framework**: FastAPI
- **Database**: SQLModel with Neon Serverless PostgreSQL
- **Authentication**: JWT tokens verified using BETTER_AUTH_SECRET
- **Security**: All endpoints require JWT authentication and enforce user isolation

## Folder Structure
```
backend/
├── main.py                 # Application entry point
├── db.py                   # Database connection and session management
├── models.py               # SQLModel database models
├── auth.py                 # JWT verification and decoding logic
├── dependencies.py         # FastAPI dependencies
├── routes/
│   └── tasks.py           # Task-related API routes
├── schemas/
│   └── task.py            # Pydantic schemas for tasks
├── requirements.txt       # Python dependencies
└── CLAUDE.md             # This documentation
```

## Authentication
- All API endpoints require JWT authentication in the Authorization header: `Authorization: Bearer <token>`
- JWT tokens are issued by Better Auth and verified using the BETTER_AUTH_SECRET
- User identity is extracted from the token's `sub` claim
- Requests are rejected if tokens are missing, invalid, or expired
- User isolation is enforced - users can only access their own tasks

## API Endpoints
- `GET    /api/tasks`                    - Get all tasks for authenticated user
- `POST   /api/tasks`                    - Create a new task for authenticated user
- `GET    /api/tasks/{id}`              - Get a specific task by ID
- `PUT    /api/tasks/{id}`              - Update a specific task by ID
- `DELETE /api/tasks/{id}`              - Delete a specific task by ID
- `PATCH  /api/tasks/{id}/complete`     - Update completion status of a task

## Database Model
- **Table**: tasks
- **Fields**:
  - id (int, primary key)
  - user_id (string, indexed) - links task to user
  - title (string, required)
  - description (string, optional)
  - completed (boolean, default: false)
  - created_at (datetime)
  - updated_at (datetime)

## Security Features
- JWT token validation on every request
- User isolation - users can only access their own data
- Proper error handling with appropriate HTTP status codes
- Input validation using Pydantic schemas

## Environment Variables
- `NEON_DB_URL` - Database connection string for Neon PostgreSQL
- `BETTER_AUTH_SECRET` - Secret key for JWT verification

## Error Handling
- 401 Unauthorized for invalid/missing JWT tokens
- 403 Forbidden for unauthorized access to resources
- 404 Not Found for non-existent resources
- Proper exception handling throughout the application

## Running the Application
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```