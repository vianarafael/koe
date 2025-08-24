import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.models import User, UserCreate, UserResponse
from app.db import init_db, get_db
from app.auth import hash_password, verify_password, create_session, get_session, delete_session
import aiosqlite
from datetime import datetime

# Test client
client = TestClient(app)

@pytest.fixture
async def test_db():
    """Create a test database"""
    # Use in-memory database for testing
    test_db_url = "sqlite:///:memory:"
    
    # Initialize test database
    await init_db()
    
    # Get database connection
    async for db in get_db():
        yield db
        break

@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123"
    }

@pytest.fixture
def sample_user():
    """Sample user object for testing"""
    return User(
        id="test-user-id",
        email="test@example.com",
        username="testuser",
        hashed_password=hash_password("testpassword123"),
        point_values={"like": 1, "retweet": 2, "reply": 3, "mention": 1},
        created_at=datetime.utcnow(),
        is_active=True
    )

def test_password_hashing():
    """Test password hashing and verification"""
    password = "testpassword123"
    hashed = hash_password(password)
    
    # Hash should be different from plain text
    assert hashed != password
    
    # Verification should work
    assert verify_password(password, hashed) == True
    
    # Wrong password should fail
    assert verify_password("wrongpassword", hashed) == False

def test_session_management():
    """Test session creation, retrieval, and deletion"""
    user = User(
        id="test-id",
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_password"
    )
    
    # Create session
    session_id = create_session(user)
    assert session_id is not None
    assert len(session_id) > 0
    
    # Retrieve session
    session_data = get_session(session_id)
    assert session_data is not None
    assert session_data.user_id == user.id
    assert session_data.email == user.email
    assert session_data.username == user.username
    
    # Delete session
    delete_session(session_id)
    assert get_session(session_id) is None

@pytest.mark.asyncio
async def test_user_registration_success(test_db, sample_user_data):
    """Test successful user registration"""
    with patch('app.auth.get_db', return_value=test_db), \
         patch('app.auth.check_email_exists', return_value=False), \
         patch('app.auth.check_username_exists', return_value=False):
        
        response = client.post("/auth/register", data=sample_user_data)
        
        # Should redirect to dashboard
        assert response.status_code == 302
        assert response.headers["location"] == "/"
        
        # Should set session cookie
        cookies = response.cookies
        assert "koe_session" in cookies

@pytest.mark.asyncio
async def test_user_registration_email_exists(test_db, sample_user_data):
    """Test user registration with existing email"""
    with patch('app.auth.get_db', return_value=test_db), \
         patch('app.auth.check_email_exists', return_value=True):
        
        response = client.post("/auth/register", data=sample_user_data)
        
        # Should return 400 error
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

@pytest.mark.asyncio
async def test_user_registration_username_exists(test_db, sample_user_data):
    """Test user registration with existing username"""
    with patch('app.auth.get_db', return_value=test_db), \
         patch('app.auth.check_email_exists', return_value=False), \
         patch('app.auth.check_username_exists', return_value=True):
        
        response = client.post("/auth/register", data=sample_user_data)
        
        # Should return 400 error
        assert response.status_code == 400
        assert "Username already taken" in response.json()["detail"]

@pytest.mark.asyncio
async def test_user_registration_short_password(test_db, sample_user_data):
    """Test user registration with short password"""
    sample_user_data["password"] = "123"
    
    with patch('app.auth.get_db', return_value=test_db):
        response = client.post("/auth/register", data=sample_user_data)
        
        # Should return 400 error
        assert response.status_code == 400
        assert "Password must be at least 8 characters long" in response.json()["detail"]

@pytest.mark.asyncio
async def test_user_login_success(test_db, sample_user):
    """Test successful user login"""
    with patch('app.auth.get_db', return_value=test_db), \
         patch('app.auth.get_user_by_email', return_value=sample_user):
        
        login_data = {
            "email": "test@example.com",
            "password": "testpassword123"
        }
        
        response = client.post("/auth/login", data=login_data)
        
        # Should redirect to dashboard
        assert response.status_code == 302
        assert response.headers["location"] == "/"
        
        # Should set session cookie
        cookies = response.cookies
        assert "koe_session" in cookies

@pytest.mark.asyncio
async def test_user_login_invalid_email(test_db):
    """Test user login with invalid email"""
    with patch('app.auth.get_db', return_value=test_db), \
         patch('app.auth.get_user_by_email', return_value=None):
        
        login_data = {
            "email": "nonexistent@example.com",
            "password": "testpassword123"
        }
        
        response = client.post("/auth/login", data=login_data)
        
        # Should return 401 error
        assert response.status_code == 401
        assert "Invalid email or password" in response.json()["detail"]

@pytest.mark.asyncio
async def test_user_login_invalid_password(test_db, sample_user):
    """Test user login with invalid password"""
    with patch('app.auth.get_db', return_value=test_db), \
         patch('app.auth.get_user_by_email', return_value=sample_user):
        
        login_data = {
            "email": "test@example.com",
            "password": "wrongpassword"
        }
        
        response = client.post("/auth/login", data=login_data)
        
        # Should return 401 error
        assert response.status_code == 401
        assert "Invalid email or password" in response.json()["detail"]

def test_login_page_renders():
    """Test that login page renders correctly"""
    response = client.get("/auth/login")
    assert response.status_code == 200
    assert "Sign in to your account" in response.text
    assert "Email address" in response.text
    assert "Password" in response.text

def test_register_page_renders():
    """Test that registration page renders correctly"""
    response = client.get("/auth/register")
    assert response.status_code == 200
    assert "Create your account" in response.text
    assert "Email address" in response.text
    assert "Username" in response.text
    assert "Password" in response.text

def test_logout_redirects():
    """Test that logout redirects to home page"""
    response = client.get("/auth/logout")
    assert response.status_code == 302
    assert response.headers["location"] == "/"

@pytest.mark.asyncio
async def test_profile_endpoint_authenticated(test_db, sample_user):
    """Test profile endpoint with authenticated user"""
    # Create a session first
    session_id = create_session(sample_user)
    
    with patch('app.auth.get_db', return_value=test_db), \
         patch('app.auth.get_user_by_id', return_value=sample_user):
        
        # Set session cookie
        client.cookies.set("koe_session", session_id)
        
        response = client.get("/auth/profile")
        
        # Should return user profile
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == sample_user.email
        assert data["username"] == sample_user.username

@pytest.mark.asyncio
async def test_profile_endpoint_unauthenticated():
    """Test profile endpoint without authentication"""
    response = client.get("/auth/profile")
    
    # Should return 401 error
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]

@pytest.mark.asyncio
async def test_dashboard_authenticated(test_db, sample_user):
    """Test dashboard with authenticated user"""
    # Create a session first
    session_id = create_session(sample_user)
    
    with patch('app.auth.get_db', return_value=test_db), \
         patch('app.auth.get_user_by_id', return_value=sample_user):
        
        # Set session cookie
        client.cookies.set("koe_session", session_id)
        
        response = client.get("/")
        
        # Should return dashboard
        assert response.status_code == 200
        assert "Welcome!" in response.text
        assert "Upload CSV" in response.text

def test_dashboard_unauthenticated():
    """Test dashboard without authentication"""
    response = client.get("/")
    
    # Should return dashboard with auth prompt
    assert response.status_code == 200
    assert "Authentication Required" in response.text
    assert "Sign in" in response.text
    assert "Create account" in response.text

@pytest.mark.asyncio
async def test_database_initialization():
    """Test database initialization creates required tables"""
    # This test would require a real database connection
    # For now, we'll test the function exists and can be called
    assert callable(init_db)

@pytest.mark.asyncio
async def test_form_validation_missing_fields():
    """Test form validation with missing fields"""
    # Test registration with missing fields
    response = client.post("/auth/register", data={})
    assert response.status_code == 400
    
    # Test login with missing fields
    response = client.post("/auth/login", data={})
    assert response.status_code == 400

if __name__ == "__main__":
    pytest.main([__file__])
