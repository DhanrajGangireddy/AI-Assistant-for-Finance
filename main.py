from fastapi import FastAPI
from routering.routes import router as api_router
from configure.config import settings
import uvicorn,os


app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
async def welcome():
    return {"message": "Welcome"} 
