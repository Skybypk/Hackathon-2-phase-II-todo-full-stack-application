# Deployment Walkthrough

I have prepared your application for a seamless deployment on **Render.com**. By adding a `render.yaml` Blueprint configuration and updating your code to be environment-aware, you can now deploy your Database, Backend, and Frontend in one go.

## Changes Made
1.  **Created `render.yaml`**: This file tells Render how to build and run your services.
2.  **Updated Frontend API Config**: Modified `custom-auth.ts` and `api-client.ts` to look for the `NEXT_PUBLIC_API_BASE_URL` environment variable, ensuring the frontend connects to the backend in production.
3.  **Updated Backend CORS**: Configured `main.py` to accept requests from your deployed frontend URL.
4.  **Added Build Script**: Created `backend/build.sh` to handle Python dependency installation.

## How to Deploy

### Step 1: Push to GitHub
Commit and push all the changes I made to your repository.

```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### Step 2: Create Blueprint on Render
1.  Log in to [Render.com](https://dashboard.render.com/).
2.  Click **New +** and select **Blueprint**.
3.  Connect your GitHub Trusted Account and select this repository.
4.  Render will automatically detect the `render.yaml` file.
5.  Click **Apply**.

### Step 3: Final Configuration
Render might ask you to confirm the plan (Free tier is usually fine for testing).
- `todo-db`: PostgreSQL Database
- `todo-backend`: FastApi Backend
- `todo-frontend`: Next.js Site

Once verified, click **Create Resources**. Render will start building everything.

### Step 4: Verification
Once the deployment is green:
1.  Click on the `todo-frontend` service in the Render dashboard.
2.  Open the provided URL.
3.  Try creating an account or logging in. This will test the Frontend -> Backend -> Database connection.
