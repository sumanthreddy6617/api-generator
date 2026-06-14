# ML Module

Trains a Decision Tree classifier (scikit-learn) to predict API category from
endpoint name + HTTP method + number of fields.

## Train

```
pip install pandas scikit-learn joblib
python train_model.py
```

Outputs `api_classifier.pkl` (pickled model + metrics). The FastAPI backend
loads this file via `ML_MODEL_PATH` in `Backend/.env`.

Categories: User Management API, Product API, Payment API, Authentication API, Analytics API.
