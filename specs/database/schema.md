# Database Schema Specification

## Overview
Database schema for the Todo application using SQLModel with Neon Serverless PostgreSQL.

## Database Tables

### Users Table
- **Table Name**: `users`
- **Description**: Stores user account information

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL | Unique user identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User's email address |
| password_hash | VARCHAR(255) | NOT NULL | Hashed password using bcrypt |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Account creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

### Tasks Table
- **Table Name**: `tasks`
- **Description**: Stores user tasks

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL | Unique task identifier |
| title | VARCHAR(255) | NOT NULL | Task title |
| description | TEXT | NULL | Optional task description |
| completed | BOOLEAN | NOT NULL, DEFAULT FALSE | Completion status |
| user_id | UUID | FOREIGN KEY, NOT NULL | Owner of the task |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Task creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |
| completed_at | TIMESTAMP | NULL | Timestamp when task was marked complete |

### Indexes
- `users.email`: Unique index for fast email lookup during authentication
- `tasks.user_id`: Index for efficient user-based task queries
- `tasks.created_at`: Index for sorting tasks by creation date
- `tasks.completed`: Index for filtering completed tasks

## Relationships
- `tasks.user_id` → `users.id` (Many-to-One relationship)
- One user can have many tasks
- Tasks are deleted when user is deleted (CASCADE)

## SQLModel Definitions

### User Model
```python
from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid

class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False)

class User(UserBase, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    password_hash: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Task Model
```python
from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid
from typing import Optional

class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    __tablename__ = "tasks"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = Field(default=None)
```

## Constraints
- Email uniqueness: Prevents duplicate accounts
- Not-null constraints: Ensures essential fields are populated
- Foreign key constraints: Maintains referential integrity
- Default values: Automatically sets timestamps

## Security Considerations
- Passwords stored as bcrypt hashes, never plain text
- User ID association ensures data isolation
- Proper indexing for performance without exposing sensitive data

## Migration Strategy
- Initial migration creates both tables
- Future migrations will follow forward-only approach
- Backup strategy implemented before structural changes
- Rollback procedures documented for critical changes