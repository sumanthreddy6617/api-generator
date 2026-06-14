import json, random
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from database import APIEndpoint, User, get_db
from auth import current_user
from faker import Faker

fake = Faker()
router = APIRouter(tags=["apis"])

class Field(BaseModel):
    name: str; type: str
class APIIn(BaseModel):
    endpoint_name: str
    request_method: str
    category: str = ""
    fields: List[Field] = []

def _fake_value(name: str, t: str):
    n = name.lower()
    if t == "string":
        if "email" in n: return fake.email()
        if "name" in n: return fake.name()
        if "phone" in n: return fake.phone_number()
        if "address" in n: return fake.address()
        if "status" in n: return random.choice(["active","inactive","pending"])
        if "city" in n: return fake.city()
        if "country" in n: return fake.country()
        return fake.word()
    if t == "integer":
        if "id" in n: return random.randint(100, 999)
        if "age" in n: return random.randint(18, 80)
        return random.randint(1, 1000)
    if t == "float": return round(random.uniform(1, 1000), 2)
    if t == "boolean": return random.choice([True, False])
    if t == "array": return [fake.word() for _ in range(3)]
    if t == "object": return {"key": fake.word(), "value": fake.word()}
    return None

def build_mock(fields: List[Field]) -> Dict[str, Any]:
    return {f.name: _fake_value(f.name, f.type) for f in fields}

@router.post("/apis/preview")
def preview(data: APIIn, _: User = Depends(current_user)):
    return {"mock_response": build_mock(data.fields)}

@router.post("/apis")
def create_api(data: APIIn, u: User = Depends(current_user), db: Session = Depends(get_db)):
    mock = build_mock(data.fields)
    api = APIEndpoint(
        endpoint_name=data.endpoint_name, request_method=data.request_method,
        category=data.category, fields=json.dumps([f.dict() for f in data.fields]),
        mock_response=json.dumps(mock), created_by=u.id)
    db.add(api); db.commit(); db.refresh(api)
    return _to_dict(api)

@router.get("/apis")
def list_apis(u: User = Depends(current_user), db: Session = Depends(get_db)):
    return [_to_dict(a) for a in db.query(APIEndpoint).filter(APIEndpoint.created_by==u.id).order_by(APIEndpoint.created_at.desc()).all()]

@router.get("/apis/{api_id}")
def get_api(api_id: int, u: User = Depends(current_user), db: Session = Depends(get_db)):
    a = db.query(APIEndpoint).filter(APIEndpoint.id==api_id, APIEndpoint.created_by==u.id).first()
    if not a: raise HTTPException(404, "Not found")
    return _to_dict(a)

@router.delete("/apis/{api_id}")
def delete_api(api_id: int, u: User = Depends(current_user), db: Session = Depends(get_db)):
    a = db.query(APIEndpoint).filter(APIEndpoint.id==api_id, APIEndpoint.created_by==u.id).first()
    if not a: raise HTTPException(404, "Not found")
    db.delete(a); db.commit()
    return {"ok": True}

# Public mock execution: /mock/<endpoint_name>
public_router = APIRouter(tags=["mock"])

@public_router.api_route("/mock/{endpoint_name}", methods=["GET","POST","PUT","DELETE"])
def serve_mock(endpoint_name: str, db: Session = Depends(get_db)):
    a = db.query(APIEndpoint).filter(APIEndpoint.endpoint_name==endpoint_name).first()
    if not a: raise HTTPException(404, "Mock not found")
    return json.loads(a.mock_response or "{}")

def _to_dict(a: APIEndpoint):
    return {"id": a.id, "endpoint_name": a.endpoint_name, "request_method": a.request_method,
            "category": a.category, "fields": json.loads(a.fields or "[]"),
            "mock_response": a.mock_response, "created_at": a.created_at}
