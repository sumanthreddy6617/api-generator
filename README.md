# MockForge AI — AI-Enhanced Mock API Generator Platform

Final-year engineering project with FastAPI + MySQL backend, vanilla HTML/CSS/JS
frontend, scikit-learn ML category prediction, and Google Gemini documentation
generation.

## Project Layout

```
mock-api-platform/
├── Frontend/           # Static HTML/CSS/JS — open in any browser or static host
│   ├── index.html      # Landing page
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── create-api.html
│   ├── api-management.html
│   ├── api-testing.html
│   ├── ml-dashboard.html
│   ├── ai-docs.html
│   ├── profile.html
│   ├── css/style.css
│   └── js/{api,ui}.js
│
├── Backend/            # FastAPI app
│   ├── app.py          # Entrypoint
│   ├── database.py     # SQLAlchemy models (users, api_endpoints, api_logs, ml_predictions, ai_documents)
│   ├── auth.py         # JWT + bcrypt
│   ├── api_generator.py# Mock CRUD + public /mock/<name>
│   ├── ml_prediction.py# /ml/predict /ml/metrics /ml/history
│   ├── ai_generator.py # /ai/generate-docs (Gemini)
│   ├── stats.py        # Dashboard analytics
│   ├── config.py
│   ├── requirements.txt
│   └── .env.example
│
├── ML/
│   ├── dataset.csv         # 400-row synthetic dataset, 5 categories
│   ├── train_model.py      # Decision Tree → api_classifier.pkl
│   └── train_model.ipynb
│
└── Documentation/
    └── project_report.md   # Markdown report (print to PDF)
```

## Quick Start

### 1. Backend

```bash
cd Backend
python -m venv .venv && source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env                                 # edit DB url + GEMINI_API_KEY
```

Create the MySQL database:

```sql
CREATE DATABASE mockforge CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Train the ML model (one-time):

```bash
cd ../ML
pip install pandas scikit-learn joblib
python train_model.py
```

Run the API:

```bash
cd ../Backend
uvicorn app:app --reload --port 8000
```

OpenAPI docs: http://localhost:8000/docs

### 2. Frontend

The frontend is plain static HTML — just open it.

Option A (simplest):
```bash
cd Frontend
python -m http.server 5500
```
Then open http://localhost:5500/index.html

Option B: open `Frontend/index.html` directly in your browser.

Configure the API base URL on the **Profile** page after logging in
(default `http://localhost:8000`).

## API Routes

| Method | Path                  | Description                          |
|--------|-----------------------|--------------------------------------|
| POST   | /auth/register        | Register a new user                  |
| POST   | /auth/login           | Login → JWT                          |
| GET    | /auth/me              | Current user profile                 |
| POST   | /apis                 | Create mock endpoint                 |
| GET    | /apis                 | List user's APIs                     |
| GET    | /apis/{id}            | Get one                              |
| DELETE | /apis/{id}            | Delete                               |
| POST   | /apis/preview         | Preview mock JSON without saving     |
| ANY    | /mock/{endpoint_name} | Serve mock response (public)         |
| POST   | /ml/predict           | Predict API category                 |
| GET    | /ml/metrics           | Model metrics (acc/precision/recall/f1/CM) |
| GET    | /ml/history           | Prediction history                   |
| POST   | /ai/generate-docs     | Generate docs/schema via Gemini      |
| GET    | /stats/overview       | Dashboard analytics                  |

## Notes

* Passwords are hashed with bcrypt.
* JWT signed with HS256; expiry from `JWT_EXPIRE_MIN`.
* CORS allows `*` for local development — restrict in production.
* If `GEMINI_API_KEY` is missing, `/ai/generate-docs` falls back to a deterministic schema generator so the UI keeps working.



GITHUB LINK:https://github.com/sumanthreddy6617/AI-enhanced_mock_API_generator.git

LinkedIn profile:https://www.linkedin.com/in/sumanth-reddy-8b0a52291/