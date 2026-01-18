---
description: Create and initialize a full-stack application with Frontend, Backend, and Integration components following spec-driven development principles.
---

## User Input

```text
$ARGUMENTS
```

## Full-Stack Application Generator

This skill creates a complete full-stack application setup with:
- Frontend agent (React/TypeScript)
- Backend agent (Node.js/Express or Python/FastAPI)
- Integration agent (API gateway and orchestration)
- Complete SP (Spec-Plus) configuration
- Proper project structure and documentation

## Execution Steps

1. **Validate Input**
   - Check if project name is provided
   - Verify target directory doesn't exist or is empty

2. **Create Project Structure**
   - Initialize main project directory
   - Set up .specify, specs, agents directories
   - Create proper subdirectories for each component

3. **Initialize SP Components**
   - Create project constitution
   - Set up template files
   - Configure memory and scripts

4. **Create Agent Configurations**
   - Frontend agent with React/TS setup
   - Backend agent with API framework
   - Integration agent for service orchestration

5. **Generate Documentation**
   - Create README with setup instructions
   - Document API contracts
   - Add deployment guides

## Implementation

```bash
# Create main project structure
mkdir -p "$PROJECT_NAME"/{agents/{frontend,backend,integration},specs/{features,api,database},.specify/{memory,scripts,templates},history/{prompts,adr}}

# Copy configuration files
cp .specify/memory/constitution.md "$PROJECT_NAME/.specify/memory/constitution.md" 2>/dev/null || echo "# Project Constitution" > "$PROJECT_NAME/.specify/memory/constitution.md"

# Create agent configurations (they already exist in our project)
echo "Agent configurations already created."

# Create initial feature specification
cat > "$PROJECT_NAME/specs/features/main.feature.md" << 'EOF'
# Main Application Feature

## Overview
Full-stack application with user authentication, CRUD operations, and real-time features.

## User Stories
- As a user, I want to register and login securely
- As a user, I want to create, read, update, and delete items
- As an admin, I want to manage user accounts

## Acceptance Criteria
- User authentication with JWT tokens
- RESTful API endpoints
- Responsive frontend interface
- Real-time notifications (optional)

## Constraints
- Must support 1000+ concurrent users
- Response time under 200ms
- Mobile-responsive design
EOF

# Create initial API specification
mkdir -p "$PROJECT_NAME/specs/api/v1"
cat > "$PROJECT_NAME/specs/api/v1/users.yaml" << 'EOF'
openapi: 3.0.0
info:
  title: User Management API
  version: 1.0.0
  description: API for user management operations
paths:
  /api/users:
    get:
      summary: Get all users
      responses:
        '200':
          description: List of users
    post:
      summary: Create a new user
      responses:
        '201':
          description: User created successfully
EOF

# Create README
cat > "$PROJECT_NAME/README.md" << 'EOF'
# Full-Stack Application

This project implements a full-stack application with Frontend, Backend, and Integration layers.

## Architecture

### Frontend
- Built with React and TypeScript
- Responsive design with Tailwind CSS
- State management with Redux Toolkit

### Backend
- RESTful API with Express.js or FastAPI
- PostgreSQL database with Prisma ORM
- JWT-based authentication

### Integration
- API gateway for request routing
- Cross-service communication layer
- Health monitoring and logging

## Quick Start

1. Navigate to frontend directory: `cd agents/frontend`
2. Install dependencies: `npm install`
3. Start development server: `npm run dev`

1. Navigate to backend directory: `cd agents/backend`
2. Install dependencies: `npm install` or `pip install -r requirements.txt`
3. Start server: `npm run dev` or `uvicorn main:app --reload`

## Development Workflow

This project follows Spec-Driven Development (SDD) methodology:
- Define specifications first in `specs/` directory
- Generate plans with `/sp.plan`
- Create tasks with `/sp.tasks`
- Implement with `/sp.implement`

## Commands

Use the following SP commands for development:
- `/sp.specify <feature>` - Create feature specification
- `/sp.plan <feature>` - Generate implementation plan
- `/sp.tasks` - Generate development tasks
- `/sp.implement` - Execute implementation
- `/sp.adr <title>` - Create architectural decision record
EOF

echo "Full-stack application structure initialized successfully!"
echo ""
echo "Next steps:"
echo "1. Review and customize the generated specifications"
echo "2. Use /sp.plan to generate detailed implementation plans"
echo "3. Use /sp.tasks to break plans into actionable tasks"
echo "4. Use /sp.implement to execute the implementation"
```

## Next Steps

After running this skill:

1. Review the generated specifications in `specs/features/`
2. Customize the API contracts in `specs/api/`
3. Update the constitution in `.specify/memory/` if needed
4. Generate implementation plans using `/sp.plan`
5. Begin development following the spec-driven approach

## PHR Creation

As the main request completes, you MUST create and complete a PHR (Prompt History Record).

1) Determine Stage: `general`
2) Generate Title: "Full-Stack App Initialization"
3) Route: `history/prompts/general/`
4) Create PHR with details of this initialization