from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes_ads import router as ads_router
from app.api.routes_ai import router as ai_router

app = FastAPI(title="Ad Intelligence SaaS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ads_router, prefix="/ads")
app.include_router(ai_router, prefix="/ai")


@app.get("/")
def health():
    return {"status": "ok"}