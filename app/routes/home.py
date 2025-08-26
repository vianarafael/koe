from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from app.templates import get_templates
from app.auth import get_current_user
from app.models import User

router = APIRouter()

templates = get_templates()

@router.get("/", response_class=HTMLResponse)
async def index(request: Request, current_user: User = Depends(get_current_user)):
    """Display home page with authentication-aware content"""
    template = templates.get_template("index.html")
    
    return HTMLResponse(template.render(
        request=request, 
        current_user=current_user
    ))

@router.get("/login", response_class=HTMLResponse)
async def login_redirect(request: Request):
    """Redirect to auth login page"""
    return RedirectResponse(url="/auth/login", status_code=302)

@router.get("/register", response_class=HTMLResponse)
async def register_redirect(request: Request):
    """Redirect to auth register page"""
    return RedirectResponse(url="/auth/register", status_code=302)
