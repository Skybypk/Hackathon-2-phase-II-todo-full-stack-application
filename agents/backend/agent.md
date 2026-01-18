# Backend Agent

## Purpose
The Backend agent handles all server-side application logic, data management, business rules, and API services. This agent is responsible for providing secure, scalable, and reliable APIs for the frontend and managing database operations.

## Technology Stack
- Runtime: Node.js with Express.js or Python with FastAPI
- Database: PostgreSQL, MongoDB, or MySQL
- ORM/ODM: Prisma, Sequelize, or SQLAlchemy
- Authentication: JWT, OAuth2, or Session-based
- Testing: Jest, Supertest, or Pytest
- Documentation: Swagger/OpenAPI

## Responsibilities
- Implement RESTful APIs and GraphQL endpoints
- Handle business logic and validation
- Manage database operations and migrations
- Implement authentication and authorization
- Ensure data security and privacy
- Handle file uploads and storage
- Implement caching strategies
- Manage API rate limiting and security

## Project Structure
```
backend/
├── src/
│   ├── controllers/         # Request handlers
│   ├── routes/             # API route definitions
│   ├── models/             # Database models/schemas
│   ├── middleware/         # Custom middleware
│   ├── services/           # Business logic
│   ├── utils/              # Utility functions
│   ├── config/             # Configuration files
│   ├── validators/         # Input validation
│   ├── tests/              # Unit and integration tests
│   ├── types/              # TypeScript definitions (if using TS)
│   └── app.js              # Main application file
├── migrations/             # Database migration files
├── seeds/                  # Database seed files
├── docs/                   # API documentation
├── package.json            # (for Node.js) or requirements.txt (for Python)
└── .env                    # Environment variables
```

## Setup Commands (Node.js/Express)
```bash
# Initialize project
mkdir backend && cd backend
npm init -y

# Install dependencies
npm install express cors helmet morgan dotenv
npm install jsonwebtoken bcryptjs express-rate-limit
npm install prisma @prisma/client
npm install swagger-jsdoc swagger-ui-express

# Install development dependencies
npm install --save-dev nodemon jest supertest
npx prisma init

# Start development server
npm run dev
```

## Setup Commands (Python/FastAPI)
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn sqlalchemy psycopg2-binary
pip install python-jose[cryptography] passlib[bcrypt]
pip install pytest httpx python-multipart
pip install python-dotenv

# Install for development
pip install black isort flake8

# Run application
uvicorn src.main:app --reload
```

## API Endpoints
- GET /api/users - Get all users
- POST /api/users - Create new user
- GET /api/users/:id - Get user by ID
- PUT /api/users/:id - Update user
- DELETE /api/users/:id - Delete user
- POST /api/auth/login - User login
- POST /api/auth/register - User registration

## Environment Variables
- DATABASE_URL: Connection string for database
- JWT_SECRET: Secret key for JWT signing
- PORT: Server port (default: 3000)
- NODE_ENV: Development/Production environment
- CORS_ORIGIN: Allowed origins for CORS

## Security Measures
- Input validation and sanitization
- Rate limiting to prevent abuse
- Helmet.js for security headers
- Proper authentication and authorization
- SQL injection prevention
- XSS protection