from datetime import datetime, timedelta
from collections import Counter
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import APIEndpoint, MLPrediction, AIDocument, APILog, User, get_db
from auth import current_user

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("/overview")
def overview(u: User = Depends(current_user), db: Session = Depends(get_db)):
    total_apis = db.query(APIEndpoint).filter(APIEndpoint.created_by==u.id).count()
    total_preds = db.query(MLPrediction).filter(MLPrediction.user_id==u.id).count()
    total_docs = db.query(AIDocument).filter(AIDocument.user_id==u.id).count()
    total_resp = db.query(APILog).count()

    # trends - last 7 days
    days = [(datetime.utcnow().date() - timedelta(days=i)) for i in range(6, -1, -1)]
    labels = [d.strftime("%a") for d in days]
    rows = db.query(APIEndpoint).filter(APIEndpoint.created_by==u.id).all()
    counts = Counter(r.created_at.date() for r in rows if r.created_at)
    trend_values = [counts.get(d, 0) for d in days]

    cat_counter = Counter(r.category or "Uncategorized" for r in rows)
    return {
        "total_apis": total_apis, "total_responses": total_resp,
        "total_ai_docs": total_docs, "total_predictions": total_preds,
        "trend": {"labels": labels, "values": trend_values},
        "categories": {"labels": list(cat_counter.keys()) or ["None"],
                       "values": list(cat_counter.values()) or [0]},
        "activity": {"labels": labels, "values": trend_values}
    }
