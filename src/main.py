from fastapi import FastAPI

from src.metrics import router as metrics_router

app = FastAPI()

app.include_router(router=metrics_router.router, prefix="/metrics", tags=["metrics"])