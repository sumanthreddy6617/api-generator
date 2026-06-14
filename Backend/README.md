# MockForge AI — FastAPI Backend

## Setup

1. Install MySQL and create a database:
   ```
   CREATE DATABASE mockforge CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and fill in your values
   (DATABASE_URL, JWT_SECRET, GEMINI_API_KEY).

4. Train the ML model (one-time):
   ```
   cd ../ML
   python train_model.py
   ```

5. Run:
   ```
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

OpenAPI docs available at: http://localhost:8000/docs
