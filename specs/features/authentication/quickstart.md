# Quickstart Guide: User Authentication System

## Overview
This guide explains how to get the user authentication system up and running quickly.

## Prerequisites
- Node.js 18+ installed
- PostgreSQL database running
- npm or yarn package manager

## Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables by copying the example:
```bash
cp .env.example .env
```

4. Update the `.env` file with your database connection details and JWT secret:
```
DATABASE_URL="postgresql://username:password@localhost:5432/auth_db"
JWT_SECRET="your-super-secret-jwt-key"
PORT=3000
```

5. Run database migrations:
```bash
npx prisma migrate dev
```

6. Start the backend server:
```bash
npm run dev
```

The backend server will start on `http://localhost:3000`

## Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables by copying the example:
```bash
cp .env.example .env
```

4. Update the `.env` file with your backend API URL:
```
REACT_APP_API_URL=http://localhost:3000
```

5. Start the frontend development server:
```bash
npm run dev
```

The frontend will start on `http://localhost:3000` (or the next available port)

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Authenticate a user
- `POST /api/auth/logout` - Logout a user
- `POST /api/auth/refresh` - Refresh JWT token
- `POST /api/auth/reset-password` - Request password reset

### Example Registration Request
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "firstName": "John",
  "lastName": "Doe"
}
```

### Example Login Request
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

## Running Tests

### Backend Tests
```bash
# Run all tests
npm test

# Run unit tests
npm run test:unit

# Run integration tests
npm run test:integration
```

### Frontend Tests
```bash
# Run all tests
npm test

# Run component tests
npm run test:components
```

## Development Commands

### Backend Commands
```bash
# Start development server with hot reload
npm run dev

# Build for production
npm run build

# Run linting
npm run lint

# Run security audit
npm audit
```

### Frontend Commands
```bash
# Start development server
npm run dev

# Build for production
npm run build

# Run linting
npm run lint

# Run type checking
npm run type-check
```

## Environment Configuration

### Development
- Set `NODE_ENV=development` in backend `.env`
- API calls go to local backend server

### Production
- Set `NODE_ENV=production` in backend `.env`
- Update API URL in frontend `.env` to production backend

## Troubleshooting

### Common Issues
1. **Database Connection**: Ensure PostgreSQL is running and credentials are correct in `.env`
2. **Port Conflicts**: Change PORT in `.env` if 3000 is already in use
3. **CORS Errors**: Check that frontend and backend ports are properly configured
4. **JWT Issues**: Ensure JWT_SECRET is the same in both backend and any shared configurations

### Resetting Database
```bash
npx prisma migrate reset
```

## Next Steps

1. Implement additional user stories from the tasks.md file
2. Add more comprehensive tests
3. Set up CI/CD pipeline
4. Deploy to staging environment
5. Conduct security review