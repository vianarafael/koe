from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from app.templates import get_templates
from app.auth import get_current_user
from app.db import get_db, get_user_engagements, get_user_total_score, get_top_engagements, get_user_engagement_breakdown
from app.models import User

router = APIRouter()

templates = get_templates()

@router.get("/", response_class=HTMLResponse)
async def index(request: Request, current_user: User = Depends(get_current_user), db=Depends(get_db)):
    """Display dashboard with authentication-aware content"""
    template = templates.get_template("index.html")
    
    # Get user engagement data if authenticated
    tweets = []
    total_score = 0
    top_engagements = []
    engagement_breakdown = {}
    
    if current_user:
        try:
            tweets = await get_user_engagements(db, current_user.id, limit=50)
            total_score = await get_user_total_score(db, current_user.id)
            top_engagements = await get_top_engagements(db, current_user.id, limit=5)
            engagement_breakdown = await get_user_engagement_breakdown(db, current_user.id)
        except Exception as e:
            print(f"Error fetching user data: {e}")
            tweets = []
            total_score = 0
            top_engagements = []
            engagement_breakdown = {}
    
    # Get upload success message from query params
    upload_success = request.query_params.get("upload_success") == "true"
    processed_count = request.query_params.get("processed", "0")
    stored_count = request.query_params.get("stored", "0")
    error_count = request.query_params.get("errors", "0")
    scoring_applied = request.query_params.get("scoring", "false") == "true"
    
    return HTMLResponse(template.render(
        request=request, 
        tweets=tweets, 
        total_score=total_score,
        current_user=current_user,
        upload_success=upload_success,
        processed_count=processed_count,
        stored_count=stored_count,
        error_count=error_count,
        scoring_applied=scoring_applied,
        top_engagements=top_engagements,
        engagement_breakdown=engagement_breakdown
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
