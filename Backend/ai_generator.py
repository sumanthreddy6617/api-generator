import json
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from database import AIDocument, User, get_db
from auth import current_user
from config import settings

try:
    import google.generativeai as genai
    if settings.GEMINI_API_KEY:
        genai.configure(api_key=settings.GEMINI_API_KEY)
    _GENAI_OK = True
except Exception:
    _GENAI_OK = False

router = APIRouter(prefix="/ai", tags=["ai"])

class DocIn(BaseModel):
    endpoint: str; method: str; fields: List[str]

PROMPT = """You are an API documentation generator. Given an endpoint, return ONLY a JSON object with these keys:
- documentation: a short markdown doc (3-6 lines) describing purpose, auth, and typical use.
- json_schema: a valid JSON Schema for the response body.
- request_example: an example request body object (use {{}} for GET).
- response_example: an example response object.

Endpoint: {method} /{endpoint}
Fields: {fields}

Return only valid JSON, no code fences.
"""

def _fallback(data: DocIn):
    sample = {f: f"<{f}>" for f in data.fields}
    return {
        "documentation": f"### {data.method} /{data.endpoint}\n\nThis endpoint operates on the `{data.endpoint}` resource.\n\n**Auth:** Bearer JWT required.\n\n**Fields:** {', '.join(data.fields)}.",
        "json_schema": {"type":"object","properties": {f:{"type":"string"} for f in data.fields}, "required": data.fields},
        "request_example": {} if data.method=="GET" else sample,
        "response_example": sample
    }

@router.post("/generate-docs")
def generate_docs(data: DocIn, u: User = Depends(current_user), db: Session = Depends(get_db)):
    result = None
    if _GENAI_OK and settings.GEMINI_API_KEY:
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            resp = model.generate_content(PROMPT.format(method=data.method, endpoint=data.endpoint, fields=", ".join(data.fields)))
            txt = resp.text.strip()
            if txt.startswith("```"): txt = txt.strip("`").lstrip("json").strip()
            result = json.loads(txt)
        except Exception as e:
            result = None
    if result is None:
        result = _fallback(data)
    db.add(AIDocument(user_id=u.id, endpoint=data.endpoint, payload=json.dumps(result)))
    db.commit()
    return result
