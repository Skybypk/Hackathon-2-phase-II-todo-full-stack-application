# Full Stack Deployment Guide

This guide explains how to deploy the full stack application with the frontend on Vercel and backend on Render.

## Architecture Overview
- **Frontend**: Next.js application hosted on Vercel
- **Backend**: FastAPI application hosted on Render
- **Database**: Neon PostgreSQL (managed separately)

## Deployment Order
1. Deploy the Backend first
2. Deploy the Frontend second (with backend URL)

## Step-by-Step Deployment

### 1. Prepare Your Database
- Sign up at [Neon.tech](https://neon.tech) for a free PostgreSQL database
- Create a new project and copy the connection string
- Keep this string ready for backend deployment

### 2. Generate a JWT Secret
- Create a strong random string (at least 32 characters) for `BETTER_AUTH_SECRET`
- You can use an online generator or run: `openssl rand -hex 32`

### 3. Deploy Backend to Render
- Follow the instructions in RENDER_DEPLOYMENT.md
- Use your Neon database connection string as `NEON_DB_URL`
- Use your generated secret as `BETTER_AUTH_SECRET`
- Note the deployed backend URL (e.g., `https://your-app.onrender.com`)

### 4. Deploy Frontend to Vercel
- Follow the instructions in VERCEL_DEPLOYMENT.md
- Use your deployed backend URL as `NEXT_PUBLIC_API_BASE_URL`
- Example: `NEXT_PUBLIC_API_BASE_URL=https://your-app.onrender.com`

## Configuration Summary

### Backend Environment Variables (on Render):
- `BETTER_AUTH_SECRET`: [Your generated secret]
- `NEON_DB_URL`: [Your Neon database connection string]

### Frontend Environment Variables (on Vercel):
- `NEXT_PUBLIC_API_BASE_URL`: [Your deployed backend URL]

## Testing Your Deployment
1. Visit your frontend URL (on Vercel)
2. Register a new account
3. Log in and create tasks
4. Verify that all functionality works as expected

## Troubleshooting
- If you get CORS errors, ensure your backend allows requests from your Vercel domain
- If API calls fail, check that your frontend is pointing to the correct backend URL
- Check the browser console and network tabs for specific error messages
- Check the server logs on Render for backend errors

## Maintaining Your Deployment
- Updates to the backend require redeploying the Render service
- Updates to the frontend require redeploying the Vercel service
- Both services automatically redeploy when you push to the main branch (if configured)