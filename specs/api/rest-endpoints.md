# REST API Endpoints Specification

## Overview
Complete specification for all REST API endpoints for the Todo application. All endpoints require JWT authentication.

## Authentication Endpoints

### Register User
- **POST** `/api/auth/register`
- **Headers**: `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "SecurePassword123!"
  }
  ```
- **Response**: `201 Created`
  ```json
  {
    "id": "uuid-string",
    "email": "user@example.com",
    "created_at": "2023-01-01T00:00:00Z"
  }
  ```
- **Errors**: 400, 409, 422

### Login User
- **POST** `/api/auth/login`
- **Headers**: `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "SecurePassword123!"
  }
  ```
- **Response**: `200 OK`
  ```json
  {
    "access_token": "jwt-token-string",
    "token_type": "bearer",
    "user": {
      "id": "uuid-string",
      "email": "user@example.com"
    }
  }
  ```
- **Errors**: 400, 401, 422

### Get Current User
- **GET** `/api/auth/me`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `200 OK`
  ```json
  {
    "id": "uuid-string",
    "email": "user@example.com",
    "created_at": "2023-01-01T00:00:00Z"
  }
  ```
- **Errors**: 401

## Task Endpoints

### Get All Tasks
- **GET** `/api/tasks`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `200 OK`
  ```json
  [
    {
      "id": "uuid-string",
      "title": "Task title",
      "description": "Task description",
      "completed": false,
      "user_id": "user-uuid",
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-01T00:00:00Z",
      "completed_at": null
    }
  ]
  ```
- **Errors**: 401

### Create Task
- **POST** `/api/tasks`
- **Headers**: `Authorization: Bearer <token>`, `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "title": "New task",
    "description": "Task description (optional)"
  }
  ```
- **Response**: `201 Created`
  ```json
  {
    "id": "uuid-string",
    "title": "New task",
    "description": "Task description (optional)",
    "completed": false,
    "user_id": "user-uuid",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z",
    "completed_at": null
  }
  ```
- **Errors**: 400, 401, 422

### Get Task by ID
- **GET** `/api/tasks/{id}`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `200 OK`
  ```json
  {
    "id": "uuid-string",
    "title": "Task title",
    "description": "Task description",
    "completed": false,
    "user_id": "user-uuid",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z",
    "completed_at": null
  }
  ```
- **Errors**: 401, 404

### Update Task
- **PUT** `/api/tasks/{id}`
- **Headers**: `Authorization: Bearer <token>`, `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "title": "Updated task title",
    "description": "Updated description",
    "completed": false
  }
  ```
- **Response**: `200 OK`
  ```json
  {
    "id": "uuid-string",
    "title": "Updated task title",
    "description": "Updated description",
    "completed": false,
    "user_id": "user-uuid",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z",
    "completed_at": null
  }
  ```
- **Errors**: 400, 401, 404, 422

### Toggle Task Completion
- **PATCH** `/api/tasks/{id}/complete`
- **Headers**: `Authorization: Bearer <token>`, `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "completed": true
  }
  ```
- **Response**: `200 OK`
  ```json
  {
    "id": "uuid-string",
    "title": "Task title",
    "description": "Task description",
    "completed": true,
    "user_id": "user-uuid",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z",
    "completed_at": "2023-01-01T00:00:00Z"
  }
  ```
- **Errors**: 401, 404, 422

### Delete Task
- **DELETE** `/api/tasks/{id}`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `204 No Content`
- **Errors**: 401, 404

## Common Headers
All authenticated endpoints require:
- `Authorization: Bearer <jwt-token>`

## Common Error Responses
- **400 Bad Request**: Malformed request or validation error
- **401 Unauthorized**: Missing or invalid JWT token
- **403 Forbidden**: Access denied (trying to access other user's data)
- **404 Not Found**: Resource does not exist
- **409 Conflict**: Resource conflict (e.g., duplicate email)
- **422 Unprocessable Entity**: Validation error in request body
- **500 Internal Server Error**: Unexpected server error

## Response Format
Successful responses follow this pattern:
- 200 OK: Object or Array of objects
- 201 Created: New resource object
- 204 No Content: Successful deletion/update with no response body
- 4xx/5xx: Error object with message