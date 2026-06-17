from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
import auth, api_generator, ml_prediction, ai_generator, stats

app = FastAPI(title="MockForge AI Backend", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://api-generator-fmih2pz4b-placement1.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], allow_credentials=False,
)

@app.on_event("startup")
def _startup():
    init_db()

app.include_router(auth.router)
app.include_router(api_generator.router)
app.include_router(api_generator.public_router)
app.include_router(ml_prediction.router)
app.include_router(ai_generator.router)
app.include_router(stats.router)

@app.get("/")
def root(): return {"name":"MockForge AI", "status":"ok"}
