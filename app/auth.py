import uuid
import secrets
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Request, Depends, HTTPException, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBearer
from passlib.context import CryptContext
from app.db import get_db, init_db, create_user, get_user_by_email, get_user_by_id, check_email_exists, check_username_exists
from app.models import User, UserCreate, UserLogin, UserResponse, SessionData
from app.settings import settings
from app.templates import get_templates

router = APIRouter(prefix="/auth", tags=["authentication"])
templates = get_templates()
security = HTTPBearer()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# In-memory session storage (in production, use Redis or database)
sessions = {}

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def create_session(user: User) -> str:
    """Create a new session for a user"""
    session_id = secrets.token_urlsafe(32)
    sessions[session_id] = SessionData(
        user_id=user.id,
        email=user.email,
        username=user.username
    )
    return session_id

def get_session(session_id: str) -> Optional[SessionData]:
    """Get session data by session ID"""
    return sessions.get(session_id)

def delete_session(session_id: str):
    """Delete a session"""
    if session_id in sessions:
        del sessions[session_id]

async def get_current_user(request: Request, db=Depends(get_db)) -> Optional[User]:
    """Get current authenticated user from session"""
    session_id = request.cookies.get(settings.SESSION_COOKIE_NAME)
    if not session_id:
        return None
    
    session_data = get_session(session_id)
    if not session_data:
        return None
    
    user = await get_user_by_id(db, session_data.user_id)
    return user

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Display login page"""
    template = templates.get_template("auth.html")
    return HTMLResponse(template.render(request=request, mode="login"))

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Display registration page"""
    template = templates.get_template("auth.html")
    return HTMLResponse(template.render(request=request, mode="register"))

@router.post("/register")
async def register(
    request: Request,
    email: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    db=Depends(get_db)
):
    """Handle user registration"""
    # Validate input
    if not email or not username or not password:
        template = templates.get_template("auth.html")
        return HTMLResponse(template.render(
            request=request, 
            mode="register", 
            error="All fields are required",
            email=email,
            username=username
        ))
    
    if len(password) < 8:
        template = templates.get_template("auth.html")
        return HTMLResponse(template.render(
            request=request, 
            mode="register", 
            error="Password must be at least 8 characters long",
            email=email,
            username=username
        ))
    
    # Check if email or username already exists
    if await check_email_exists(db, email):
        template = templates.get_template("auth.html")
        return HTMLResponse(template.render(
            request=request, 
            mode="register", 
            error="Email already registered",
            email=email,
            username=username
        ))
    
    if await check_username_exists(db, username):
        template = templates.get_template("auth.html")
        return HTMLResponse(template.render(
            request=request, 
            mode="register", 
            error="Username already taken",
            email=email,
            username=username
        ))
    
    # Create user
    user_data = UserCreate(email=email, username=username, password=password)
    hashed_password = hash_password(password)
    
    try:
        user = await create_user(db, user_data, hashed_password)
        
        # Create session and redirect to dashboard
        session_id = create_session(user)
        response = RedirectResponse(url="/", status_code=302)
        response.set_cookie(
            key=settings.SESSION_COOKIE_NAME,
            value=session_id,
            httponly=settings.SESSION_COOKIE_HTTPONLY,
            secure=settings.SESSION_COOKIE_SECURE,
            samesite=settings.SESSION_COOKIE_SAMESITE,
            max_age=3600 * 24 * 7  # 7 days
        )
        return response
        
    except Exception as e:
        template = templates.get_template("auth.html")
        return HTMLResponse(template.render(
            request=request, 
            mode="register", 
            error="Failed to create user. Please try again.",
            email=email,
            username=username
        ))

@router.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db=Depends(get_db)
):
    """Handle user login"""
    # Validate input
    if not email or not password:
        template = templates.get_template("auth.html")
        return HTMLResponse(template.render(
            request=request, 
            mode="login", 
            error="Email and password are required",
            email=email
        ))
    
    # Get user by email
    user = await get_user_by_email(db, email)
    if not user:
        template = templates.get_template("auth.html")
        return HTMLResponse(template.render(
            request=request, 
            mode="login", 
            error="Invalid email or password",
            email=email
        ))
    
    # Verify password
    if not verify_password(password, user.hashed_password):
        template = templates.get_template("auth.html")
        return HTMLResponse(template.render(
            request=request, 
            mode="login", 
            error="Invalid email or password",
            email=email
        ))
    
    # Create session and redirect to dashboard
    session_id = create_session(user)
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(
        key=settings.SESSION_COOKIE_NAME,
        value=session_id,
        httponly=settings.SESSION_COOKIE_HTTPONLY,
        secure=settings.SESSION_COOKIE_SECURE,
        samesite=settings.SESSION_COOKIE_SAMESITE,
        max_age=3600 * 24 * 7  # 7 days
    )
    return response

@router.get("/logout")
async def logout(request: Request):
    """Logout user and clear session"""
    session_id = request.cookies.get(settings.SESSION_COOKIE_NAME)
    if session_id:
        delete_session(session_id)
    
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie(settings.SESSION_COOKIE_NAME)
    return response

@router.get("/profile")
async def profile(request: Request, current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        point_values=current_user.point_values,
        created_at=current_user.created_at
    )

# Middleware to initialize database on startup
@router.on_event("startup")
async def startup_event():
    await init_db()
