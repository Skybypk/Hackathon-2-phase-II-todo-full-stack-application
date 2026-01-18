# Frontend Agent

## Purpose
The Frontend agent handles all client-side application logic, user interface components, and user experience concerns. This agent is responsible for creating responsive, accessible, and performant user interfaces that consume backend APIs.

## Technology Stack
- Framework: React.js with TypeScript
- State Management: Redux Toolkit or Context API
- Styling: Tailwind CSS or Material-UI
- API Client: Axios or Fetch API
- Routing: React Router
- Testing: Jest, React Testing Library, Cypress

## Responsibilities
- Implement responsive UI components
- Manage client-side state
- Handle user interactions and form submissions
- Consume backend APIs
- Implement authentication flows
- Ensure accessibility standards
- Optimize performance and loading times

## Project Structure
```
frontend/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── components/          # Reusable UI components
│   ├── pages/              # Route-specific components
│   ├── services/           # API clients and services
│   ├── store/              # State management (Redux/Context)
│   ├── utils/              # Helper functions and utilities
│   ├── hooks/              # Custom React hooks
│   ├── assets/             # Images, icons, stylesheets
│   ├── types/              # TypeScript type definitions
│   ├── tests/              # Component and integration tests
│   ├── App.tsx             # Main application component
│   └── index.tsx           # Entry point
├── package.json
├── tsconfig.json
└── tailwind.config.js
```

## Setup Commands
```bash
# Initialize project
npm create vite@latest frontend -- --template react-ts

# Navigate to project directory
cd frontend

# Install dependencies
npm install
npm install @types/react @types/react-dom
npm install axios react-router-dom
npm install reduxjs/toolkit react-redux
npm install tailwindcss postcss autoprefixer

# Initialize Tailwind CSS
npx tailwindcss init -p

# Install testing dependencies
npm install --save-dev jest @testing-library/react @testing-library/jest-dom
npm install --save-dev cypress
```

## Development Workflow
1. Start development server: `npm run dev`
2. Build for production: `npm run build`
3. Run tests: `npm run test`
4. Run linter: `npm run lint`

## API Integration
- Base URL configuration for different environments
- Interceptors for authentication headers
- Error handling and retry mechanisms
- Loading states and optimistic updates

## Environment Variables
- REACT_APP_API_URL: Backend API base URL
- REACT_APP_ENVIRONMENT: Development/Staging/Production

## Code Style
- Use functional components with hooks
- Follow React best practices
- Implement proper TypeScript typing
- Maintain consistent naming conventions
- Write reusable and modular components