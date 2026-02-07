# Zero-Cost Deployment Guide

Follow these steps to deploy CodeViz AI to the internet for **$0**.

## Prerequisites
1.  **GitHub Account**: Push this code to a new GitHub repository.
2.  **Render Account**: [Sign up here](https://render.com/) (for Backend).
3.  **Vercel Account**: [Sign up here](https://vercel.com/) (for Frontend).

---

## Part 1: Deploy Backend (Render)

1.  Log in to **Render**.
2.  Click **New +** -> **Web Service**.
3.  Connect your GitHub repository.
4.  Render will automatically detect the `render.yaml` file in the repository.
5.  Click **Apply** or **Create Web Service**.
6.  **Important**: Go to the **Environment** tab and add these variables (copy from your local `.env`):
    *   `NEO4J_URI`
    *   `NEO4J_USER`
    *   `NEO4J_PASSWORD`
    *   `GEMINI_API_KEY`
    *   `TEMP_CLONE_DIR`: `/tmp/repos`
7.  Wait for the deployment to finish.
8.  **Copy the Backend URL** (e.g., `https://codeviz-backend.onrender.com`).

---

## Part 2: Deploy Frontend (Vercel)

1.  Log in to **Vercel**.
2.  Click **Add New...** -> **Project**.
3.  Import your GitHub repository.
4.  **Configure Project**:
    *   **Framework Preset**: Next.js
    *   **Root Directory**: `codeviz/frontend` (Click "Edit" next to Root Directory and select `frontend`).
5.  **Environment Variables**:
    *   Initialise a new variable called `NEXT_PUBLIC_API_URL`.
    *   Value: Your **Backend URL** from Part 1 (e.g., `https://codeviz-backend.onrender.com`).
    *   *Note: Do not add a trailing slash `/`.*
6.  Click **Deploy**.

---

## Part 3: Verify

1.  Open your new Vercel URL (e.g., `https://codeviz-frontend.vercel.app`).
2.  Paste a GitHub repository URL to analyze.
3.  If it works, you have successfully deployed CodeViz AI for free!

## Troubleshooting
*   **CORS Error**: If the frontend cannot talk to the backend, ensure your Backend allows the Vercel domain. The current `main.py` allows all origins (`["*"]`), so it should work out of the box.
*   **Build Failures**: Check the logs in Render/Vercel.
