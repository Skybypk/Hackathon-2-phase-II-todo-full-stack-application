# Hackathon Todo Full-Stack Web Application

This is a monorepo for a Todo application with the following architecture:

- **Frontend**: Next.js 14+ (App Router), TypeScript, Tailwind CSS
- **Backend**: Python FastAPI
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Auth**: Better Auth (Frontend) + JWT
- **API Style**: REST

## Structure
- `frontend/` - Next.js application
- `backend/` - FastAPI application
- `specs/` - Specification files
- `.spec-kit/` - Spec-Kit Plus configuration

## Getting Started

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```