import os, joblib, json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import MLPrediction, User, get_db
from auth import current_user
from config import settings

router = APIRouter(prefix="/ml", tags=["ml"])

_model_cache = {"model": None, "meta": None}

def _load():
    if _model_cache["model"] is not None: return
    path = settings.ML_MODEL_PATH
    if not os.path.exists(path):
        raise HTTPException(503, f"ML model not found at {path}. Run ML/train_model.py first.")
    bundle = joblib.load(path)
    _model_cache["model"] = bundle["model"]
    _model_cache["meta"] = bundle.get("meta", {})

class PredictIn(BaseModel):
    endpoint: str; method: str; fields: int

METHOD_MAP = {"GET":0,"POST":1,"PUT":2,"DELETE":3}

def _features(p: PredictIn):
    name_hash = sum(ord(c) for c in p.endpoint.lower()) % 100
    return [[METHOD_MAP.get(p.method.upper(), 0), p.fields, name_hash]]

@router.post("/predict")
def predict(data: PredictIn, u: User = Depends(current_user), db: Session = Depends(get_db)):
    _load()
    model = _model_cache["model"]
    X = _features(data)
    pred = model.predict(X)[0]
    proba = model.predict_proba(X)[0]
    conf = float(max(proba)) * 100
    record = MLPrediction(user_id=u.id, endpoint=data.endpoint, method=data.method,
                          fields=data.fields, predicted_category=pred, confidence=round(conf,2))
    db.add(record); db.commit()
    return {"predicted_category": pred, "confidence": round(conf, 2)}

@router.get("/metrics")
def metrics():
    _load()
    return _model_cache["meta"]

@router.get("/history")
def history(u: User = Depends(current_user), db: Session = Depends(get_db)):
    rows = db.query(MLPrediction).filter(MLPrediction.user_id==u.id).order_by(MLPrediction.created_at.desc()).limit(50).all()
    return [{"endpoint": r.endpoint, "method": r.method, "fields": r.fields,
             "predicted_category": r.predicted_category, "confidence": r.confidence,
             "created_at": r.created_at} for r in rows]
