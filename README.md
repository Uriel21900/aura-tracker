# Aura Tracker - Fragrance Dupe App

A premium, full-stack web application designed for fragrance enthusiasts to track their collection and discover new dupes. This app dynamically pulls data for tens of thousands of fragrances using the Kaggle API.

## Tech Stack
- **Frontend**: React, Vite, Custom CSS (Glassmorphism + Dark Mode Aesthetics)
- **Backend**: Python, FastAPI, SQLite
- **Data Source**: Kaggle API

## Running Locally

### 1. Setup Kaggle Data
Before running, you need a free Kaggle API key (`kaggle.json`). Place it in your home directory (e.g., `~/.kaggle/kaggle.json` or `C:\Users\YourUser\.kaggle\kaggle.json`).
```bash
cd backend
python update_database.py
```

### 2. Start the Backend API
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
The API will run on `http://localhost:8000`.

### 3. Start the Frontend App
Open a new terminal window:
```bash
cd frontend
npm install
npm run dev
```
The beautiful frontend will be available at `http://localhost:5173`.
