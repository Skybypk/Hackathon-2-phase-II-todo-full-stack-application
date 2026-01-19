# Deploying Backend to Render

Follow these steps to deploy the FastAPI backend to Render:

## Prerequisites
- Sign up for a Render account at [render.com](https://render.com)

## Deployment Steps

### Option 1: Using Git Integration (Recommended)
1. Push your updated code to GitHub (if not already):
   ```bash
   git add .
   git commit -m "Add Render deployment configurations"
   git push origin main
   ```

2. Go to [dashboard.render.com](https://dashboard.render.com)
3. Click "New +" and select "Web Service"
4. Connect your GitHub account and select your repository
5. Configure the following settings:
   - Environment: Python
   - Branch: main
   - Runtime: Select the latest Python version
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host=0.0.0.0 --port=$PORT`
   - Region: Choose your preferred region

6. Add the following environment variables:
   - `BETTER_AUTH_SECRET`: A random secret string for JWT (use a strong random string)
   - `NEON_DB_URL`: Your Neon PostgreSQL database connection string
   - `DATABASE_URL`: Same as NEON_DB_URL (if required by your app)

7. Give your service a name (e.g., `todo-api`)
8. Click "Create Web Service"

### Option 2: Manual Deployment
1. Create a new Web Service on Render
2. Point it to your GitHub repository
3. Set the runtime to Python
4. Use the following configuration:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python -m uvicorn main:app --host=0.0.0.0 --port=$PORT`
   - Root Directory: `backend`

## Required Environment Variables
- `BETTER_AUTH_SECRET`: A strong secret key for JWT token signing (generate a random 32+ character string)
- `NEON_DB_URL`: Connection string for your Neon PostgreSQL database

## Database Setup
1. Create a free PostgreSQL database on [Neon.tech](https://neon.tech)
2. Copy the connection string and use it as the `NEON_DB_URL` environment variable

## Important Notes
- The backend is configured to accept CORS requests from Vercel deployments (`https://*.vercel.app`)
- Your backend will be deployed at a URL like `https://your-service.onrender.com`
- Make sure to update the `NEXT_PUBLIC_API_BASE_URL` in your frontend deployment with this URL
- The application automatically creates database tables on startup
- Render will restart your service when it receives a new push to the specified branch