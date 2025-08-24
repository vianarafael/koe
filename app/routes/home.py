from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from app.templates import get_templates
from app.auth import get_current_user
from app.models import User

router = APIRouter()

templates = get_templates()

@router.get("/", response_class=HTMLResponse)
async def index(request: Request, current_user: User = Depends(get_current_user)):
    """Display dashboard with authentication-aware content"""
    # Example HTMX usage: simple dashboard placeholder
    template = templates.get_template("index.html")
    
    # For now, we'll show empty data - this will be populated in T02/T03
    tweets = []
    total_score = 0
    
    return HTMLResponse(template.render(
        request=request, 
        tweets=tweets, 
        total_score=total_score,
        current_user=current_user
    ))

@router.get("/login", response_class=HTMLResponse)
async def login_redirect(request: Request):
    """Redirect to auth login page"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/auth/login", status_code=302)

@router.get("/register", response_class=HTMLResponse)
async def register_redirect(request: Request):
    """Redirect to auth register page"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/auth/register", status_code=302)
