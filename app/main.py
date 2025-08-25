from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from datetime import datetime
import uvicorn

from app.routes import home, upload, dashboard, settings
from app import auth
from app.scoring import scoring_engine

app = FastAPI(
    title="Koe - Social Media Engagement Analytics",
    description="Track, analyze, and optimize your social media engagement with intelligent scoring and insights",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(home.router)
app.include_router(auth.router)
app.include_router(upload.router)
app.include_router(dashboard.router)
app.include_router(settings.router)

# Health check endpoint for production monitoring
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.on_event("startup")
async def startup_event():
    # Ensure scoring engine is initialized
    assert scoring_engine is not None

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
