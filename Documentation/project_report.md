# MockForge AI — Project Report

## 1. Abstract
MockForge AI is an AI-enhanced platform for generating, testing, managing, and
documenting Mock REST APIs. It combines a vanilla-JS frontend with a FastAPI +
MySQL backend, a scikit-learn Decision Tree classifier for category prediction,
and Google Gemini for documentation generation.

## 2. Objectives
1. Allow developers to create mock REST endpoints instantly with dynamic fields.
2. Provide a built-in testing console similar to Postman.
3. Use machine learning to predict the category of an API from minimal input.
4. Use generative AI to produce documentation, JSON Schema, and examples.
5. Track usage analytics in a dashboard.

## 3. Technology Stack
Frontend — HTML5, CSS3, Vanilla JavaScript, Bootstrap 5, Chart.js
Backend  — Python 3, FastAPI, SQLAlchemy, Pydantic, JWT, bcrypt
Database — MySQL
ML       — Scikit-Learn (Decision Tree), Joblib, Pandas, NumPy
GenAI    — Google Gemini (google-generativeai)

## 4. Architecture
Three-tier: static frontend ↔ REST API (FastAPI) ↔ MySQL. ML model is loaded
from a joblib pickle at request time. Gemini is called via the official Python
SDK.

## 5. Database Schema
- users(id, name, email, password, created_at)
- api_endpoints(id, endpoint_name, request_method, category, fields, mock_response, created_by, created_at)
- api_logs(id, endpoint_id, request_data, response_data, status_code, response_time_ms, timestamp)
- ml_predictions(id, user_id, endpoint, method, fields, predicted_category, confidence, created_at)
- ai_documents(id, user_id, endpoint, payload, created_at)

## 6. Machine Learning
- Input features: HTTP method (encoded), number of fields, hashed endpoint name.
- Output: one of {User Management, Product, Payment, Authentication, Analytics}.
- Algorithm: DecisionTreeClassifier (max_depth=8).
- Metrics tracked: accuracy, precision, recall, f1, confusion matrix.

## 7. Generative AI
Prompted Gemini 1.5 Flash to return strict JSON with documentation, JSON
Schema, request example, and response example. Falls back to deterministic
synthesis when no API key is configured.

## 8. Security
- Bcrypt password hashing.
- JWT bearer tokens (HS256).
- Per-user resource ownership checks on every protected route.

## 9. Future Work
- WebSocket-based live API testing.
- Public mock sharing with short URLs.
- Switch classifier to a small neural network for accuracy gains.
