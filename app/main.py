from fastapi import FastAPI, Request
from jinja2 import Environment, FileSystemLoader
from fastapi.staticfiles import StaticFiles
from app.routes import home
from app.auth import router as auth_router
from app.routes.upload import router as upload_router
from app.settings import settings

app = FastAPI(title="Koe - Engagement Tracker")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Environment(loader=FileSystemLoader("app/templates"))

app.include_router(home.router)
app.include_router(auth_router)
app.include_router(upload_router)

@app.get("/health")
async def health():
    return {"status": "ok"}
