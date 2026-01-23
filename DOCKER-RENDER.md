# Docker Deployment to Render.com

This guide explains how to deploy your full-stack application to Render.com using Docker containers.

## Overview

Your application is already configured for Docker deployment. The setup includes:
- Backend service (FastAPI) with Dockerfile
- Frontend service (Next.js) with Dockerfile
- PostgreSQL database
- Pre-configured render.yaml for Docker deployment

## Prerequisites

1. A GitHub repository containing your code
2. A Render account
3. Dockerfiles for both frontend and backend (already created)
4. Updated render.yaml for Docker deployment (already configured)

## Deployment Steps

### Step 1: Prepare Your Repository

1. Ensure your code is pushed to a GitHub repository
2. Make sure the following files are in your repository:
   - `backend/Dockerfile`
   - `frontend/Dockerfile`
   - `render.yaml` (updated for Docker deployment)

### Step 2: Deploy to Render

1. Log in to [Render Dashboard](https://dashboard.render.com/)
2. Click **New +** and select **Blueprint** (or **Web Service** depending on your preference)
3. Connect your GitHub account and select your repository
4. Render will automatically detect the `render.yaml` file
5. Click **Apply** or **Create**

### Step 3: Configure Environment Variables (if needed)

Render will automatically create:
- A PostgreSQL database instance
- Backend service running your FastAPI application
- Frontend service running your Next.js application

The services are configured to communicate with each other using Render's internal networking.

### Step 4: Monitor Deployment

1. Watch the deployment logs in the Render dashboard
2. Wait for all services to show as "Healthy"
3. Access your application using the provided frontend URL

## Docker Configuration Details

### Backend Dockerfile (`backend/Dockerfile`)
- Uses Python 3.11-slim as base image
- Installs Python dependencies from requirements.txt
- Runs Uvicorn server on port 8000 (configured in render.yaml to use port 10000)

### Frontend Dockerfile (`frontend/Dockerfile`)
- Uses Node 18-alpine as base image
- Installs Node dependencies
- Builds the Next.js application
- Runs the production server

### Render Configuration (`render.yaml`)
- Defines two web services (backend and frontend)
- Configures the database connection
- Sets up environment variables for inter-service communication
- Uses Docker runtime for both services

## Alternative: Direct Docker Image Deployment

If you prefer to build and push Docker images directly:

1. Build your images locally:
   ```bash
   docker build -f backend/Dockerfile -t your-repo/backend .
   docker build -f frontend/Dockerfile -t your-repo/frontend .
   ```

2. Push to a container registry (Docker Hub, GitHub Container Registry, etc.)

3. Deploy to Render using the container registry option

## Troubleshooting

- **Service unhealthy**: Check the logs in Render dashboard for error messages
- **Database connection issues**: Verify the DATABASE_URL is correctly passed from the database service
- **Frontend can't reach backend**: Ensure NEXT_PUBLIC_API_BASE_URL is set correctly
- **Build failures**: Check that all dependencies are correctly specified in your Dockerfiles

## Scaling

- Adjust instance types in Render dashboard based on traffic needs
- Monitor resource usage through Render's metrics
- Consider using Render's autoscaling features for high-traffic applications