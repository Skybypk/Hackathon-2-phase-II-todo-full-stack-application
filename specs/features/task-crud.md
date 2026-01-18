# Task CRUD Feature Specification

## Overview
The Task CRUD feature enables authenticated users to create, read, update, delete, and mark tasks as complete/incomplete.

## Acceptance Criteria

### Create Task
- ✅ User can create a new task with title and optional description
- ✅ Task is associated with the authenticated user
- ✅ Task creation requires valid JWT token
- ✅ Task must have a unique ID assigned by the system
- ✅ Task should have created_at timestamp
- ✅ Task should have completed status (default: false)

### Read Tasks
- ✅ User can view all their tasks
- ✅ User can view a specific task by ID
- ✅ User can only see their own tasks (enforced by backend)
- ✅ Tasks returned in descending order of creation time
- ✅ Each task includes: id, title, description, completed status, created_at, updated_at

### Update Task
- ✅ User can update task title and/or description
- ✅ User can mark task as complete/incomplete
- ✅ Only the task owner can update the task
- ✅ Updated_at timestamp is updated on modification

### Delete Task
- ✅ User can delete their own tasks
- ✅ Only the task owner can delete the task
- ✅ Task is permanently removed from the database

### Complete/Uncomplete Task
- ✅ User can toggle task completion status
- ✅ System updates completed_at timestamp when marked complete
- ✅ System clears completed_at timestamp when marked incomplete

## Business Rules
- Each user can only access their own tasks
- Tasks cannot be shared between users
- Deleted tasks are permanently removed (no soft delete)
- Completed tasks remain accessible but with completed status

## Error Handling
- 401 Unauthorized: No valid JWT token provided
- 403 Forbidden: User trying to access another user's tasks
- 404 Not Found: Task does not exist
- 422 Unprocessable Entity: Invalid input data

## API Endpoints
- POST /api/tasks - Create new task
- GET /api/tasks - Get all user's tasks
- GET /api/tasks/{id} - Get specific task
- PUT /api/tasks/{id} - Update task
- PATCH /api/tasks/{id}/complete - Toggle completion status
- DELETE /api/tasks/{id} - Delete task