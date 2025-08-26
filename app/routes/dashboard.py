from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from datetime import datetime
from app.auth import get_current_user
from app.models import User
from app.templates import get_templates

router = APIRouter(prefix="/dashboard", tags=["dashboard"])
templates = get_templates()

@router.get("/", response_class=HTMLResponse)
async def dashboard_page(request: Request, current_user: User = Depends(get_current_user)):
    """Display simple dashboard for link tracking"""
    if not current_user:
        return RedirectResponse(url="/auth/login", status_code=302)
    
    template = templates.get_template("dashboard.html")
    return HTMLResponse(template.render(
        request=request,
        current_user=current_user,
        now=datetime.now()
    ))

@router.get("/api/links", response_class=JSONResponse)
async def get_links_api(current_user: User = Depends(get_current_user)):
    """API endpoint for getting tracked links"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # TODO: Implement link tracking functionality
    return {"message": "Link tracking coming soon", "links": []}
