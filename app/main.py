from fastapi import FastAPI
from app.api.analyze import router as analyze_router

app = FastAPI(
    title="Trade Opportunities API",
    description="Market analysis by sector",
    version="1.0"
)

app.include_router(analyze_router)
