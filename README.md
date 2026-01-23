# Hackathon-2-phse-II-todo-full-stack-application

Full stack web application

A comprehensive full-stack todo application built with modern technologies

## Features

- **Frontend**: Next.js 14+ (App Router), TypeScript, Tailwind CSS
- **Backend**: Python FastAPI
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Auth**: Better Auth (Frontend) + JWT
- **API Style**: REST
- **Architecture**: Clean, scalable monorepo structure

## Structure

- `frontend/` - Next.js application
- `backend/` - FastAPI application
- `specs/` - Specification files
- `.spec-kit/` - Spec-Kit Plus configuration

## Tech Stack

### Frontend Technologies
- **Next.js 14+** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **React** - Component-based UI library

### Backend Technologies
- **Python** - Programming language
- **FastAPI** - Modern, fast web framework
- **SQLModel** - SQL database modeling
- **Better Auth** - Authentication library
- **JWT** - Secure token-based authentication

### Database & Infrastructure
- **Neon Serverless PostgreSQL** - Cloud-native PostgreSQL
- **REST APIs** - Standardized API architecture

## Getting Started

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

## Architecture Overview

This project follows a **monorepo** architecture separating concerns between frontend and backend:

- **Frontend** - Handles user interface, authentication, and API calls
- **Backend** - Manages business logic, data persistence, and security
- **Database** - Stores application data with ACID compliance

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Deployment

- [Standard Deployment](DEPLOYMENT.md) - Traditional deployment to Render.com
- [Docker Deployment](DOCKER-RENDER.md) - Docker-based deployment to Render.com

## Built With

Made with passion during the Hackathon Phase II challenge!
