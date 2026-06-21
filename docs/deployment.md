# Deployment Plan: Railway (Backend) & Vercel (Frontend)

This document outlines the strategy for deploying the Zomato AI Recommendation application across two separate hosting providers: **Railway** for the FastAPI backend and **Vercel** for the vanilla JS frontend.

## User Review Required

> [!WARNING]
> **API Keys & URLs:** You will need to create the projects on Railway and Vercel first to get their respective URLs. 
> 1. The Railway URL is needed to configure the `fetch` request in the frontend.
> 2. The Vercel URL is needed to properly configure CORS in the backend.

> [!IMPORTANT]
> **Dataset Handling:** The `zomato_dataset.parquet` file has been removed from the repository due to its size. Fortunately, the backend is already programmed to download the dataset from Hugging Face on startup if it's not found locally. This will slightly increase the backend startup time on Railway but ensures a smooth deployment without manual data transfers.

## Open Questions

1. **CORS Security:** Do you want to temporarily allow all origins (`*`) for CORS during the initial deployment phase, or would you prefer to strictly lock it down to your Vercel URL right away?
2. **Environment Variables:** Do you have any other environment variables besides `GROQ_API_KEY` that need to be set on the backend?

## Proposed Changes

### Backend Adjustments (Railway)

We need to configure the backend to accept requests from the frontend and bind to the correct port provided by Railway.

#### [MODIFY] [main.py](file:///d:/NEXTLEAP%20GEN%20AI/Zomato%20recommendation%20system/src/api/main.py)
- Update `CORSMiddleware` to allow requests from the Vercel domain (or `*` temporarily) instead of just `localhost:5173`.
- (Optional) We can pull the allowed CORS origins from an environment variable `FRONTEND_URL` for better security.

#### [NEW] [Procfile](file:///d:/NEXTLEAP%20GEN%20AI/Zomato%20recommendation%20system/Procfile)
- Create a `Procfile` at the root of the project to tell Railway how to start the FastAPI server:
  ```text
  web: uvicorn src.api.main:app --host 0.0.0.0 --port $PORT
  ```

---

### Frontend Adjustments (Vercel)

Since the frontend and backend will be hosted on different domains, the frontend must make requests to the absolute Railway URL.

#### [MODIFY] [app.js](file:///d:/NEXTLEAP%20GEN%20AI/Zomato%20recommendation%20system/frontend/app.js)
- Define a constant for the API Base URL (e.g., `const API_BASE_URL = 'https://your-railway-app.up.railway.app';`).
- Update the `fetch('/api/recommend')` call to use `fetch(`${API_BASE_URL}/api/recommend`)`.

#### [NEW] [vercel.json](file:///d:/NEXTLEAP%20GEN%20AI/Zomato%20recommendation%20system/vercel.json) (Optional)
- Create a configuration file if needed to explicitly tell Vercel to route traffic or handle rewrites, though simply setting the "Root Directory" to `frontend` in the Vercel dashboard is usually sufficient.

## Verification Plan

### Railway Deployment Steps
1. Push the code changes (CORS update and Procfile) to GitHub.
2. In Railway, create a new project from your GitHub repository.
3. Add the `GROQ_API_KEY` environment variable in the Railway dashboard.
4. Wait for the build and deployment. Railway will automatically detect the Python environment and run the `Procfile`.
5. Verify the backend is up by visiting `https://your-railway-url.up.railway.app/docs`.

### Vercel Deployment Steps
1. In Vercel, import your GitHub repository.
2. Set the **Root Directory** to `frontend`.
3. Vercel will automatically deploy the static files (`index.html`, `app.js`, `style.css`).
4. Verify the frontend is accessible and can successfully fetch recommendations from the deployed Railway backend.
