# Deploying Frontend to Vercel

Follow these steps to deploy the Next.js frontend to Vercel:

## Prerequisites
- Sign up for a Vercel account at [vercel.com](https://vercel.com)
- Install the Vercel CLI (optional): `npm i -g vercel`

## Deployment Steps

### Option 1: Using Vercel CLI
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Deploy to Vercel:
   ```bash
   vercel --prod
   ```

4. Follow the prompts to connect your GitHub account and configure the project.

### Option 2: Using Vercel Dashboard
1. Go to [vercel.com/dashboard/new](https://vercel.com/dashboard/new)
2. Click "Import Project"
3. Select your GitHub repository (the one containing this project)
4. Choose the `frontend` directory as the root
5. Set the build command to: `npm run build`
6. Set the output directory to: `out`
7. Set the development command to: `npm run dev`
8. Add the following environment variables:
   - `NEXT_PUBLIC_API_BASE_URL`: Your deployed backend URL (e.g., `https://your-backend-name.onrender.com`)
9. Click "Deploy"

## Environment Variables Required
- `NEXT_PUBLIC_API_BASE_URL`: URL of your deployed backend API (e.g., `https://your-backend.onrender.com`)

## Important Notes
- The frontend expects the backend API to be accessible from the deployed URL
- Make sure your backend allows CORS requests from your Vercel deployment URL (should be `https://*.vercel.app`)
- After deployment, you'll get a URL like `https://your-project.vercel.app`