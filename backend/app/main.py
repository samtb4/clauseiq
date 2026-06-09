from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.contracts import router as contracts_router

app = FastAPI(title="ClauseIQ")

app.include_router(health_router)
app.include_router(contracts_router)