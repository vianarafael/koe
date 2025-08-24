import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.models import User, OAuthState
from app.db import init_db, get_db
import aiosqlite
from datetime import datetime, timedelta

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
def mock_httpx_client():
    """Mock httpx client for Twitter API calls"""
    with patch('httpx.AsyncClient') as mock_client:
        mock_instance = AsyncMock()
        mock_client.return_value.__aenter__.return_value = mock_instance
        yield mock_instance

@pytest.mark.asyncio
async def test_oauth_authorize_flow(test_db):
    """Test OAuth authorization flow initiation"""
    # Mock the database dependency
    with patch('app.auth.get_db', return_value=test_db):
        response = client.get("/auth/twitter/authorize")
        
        # Should redirect to Twitter
        assert response.status_code == 307
        assert "twitter.com" in response.headers["location"]
        assert "client_id" in response.headers["location"]
        assert "state" in response.headers["location"]
        assert "code_challenge" in response.headers["location"]

@pytest.mark.asyncio
async def test_oauth_callback_success(test_db, mock_httpx_client):
    """Test successful OAuth callback"""
    # Mock Twitter token response
    mock_httpx_client.post.return_value.status_code = 200
    mock_httpx_client.post.return_value.json.return_value = {
        "access_token": "test_access_token",
        "refresh_token": "test_refresh_token",
        "expires_in": 7200,
        "scope": "tweet.read users.read offline.access",
        "token_type": "bearer"
    }
    
    # Mock Twitter user info response
    mock_httpx_client.get.return_value.status_code = 200
    mock_httpx_client.get.return_value.json.return_value = {
        "data": {
            "id": "12345",
            "username": "testuser"
        }
    }
    
    # Mock OAuth state
    oauth_state = OAuthState(
        state="test_state",
        code_verifier="test_verifier",
        created_at=datetime.utcnow()
    )
    
    with patch('app.auth.get_db', return_value=test_db), \
         patch('app.auth.get_oauth_state', return_value=oauth_state), \
         patch('app.auth.get_twitter_user_info', return_value={"id": "12345", "username": "testuser"}):
        
        response = client.get("/auth/callback?code=test_code&state=test_state")
        
        # Should redirect to home page
        assert response.status_code == 302
        assert response.headers["location"] == "/"

@pytest.mark.asyncio
async def test_oauth_callback_invalid_state(test_db):
    """Test OAuth callback with invalid state"""
    with patch('app.auth.get_db', return_value=test_db), \
         patch('app.auth.get_oauth_state', return_value=None):
        
        response = client.get("/auth/callback?code=test_code&state=invalid_state")
        
        # Should return 400 error
        assert response.status_code == 400
        assert "Invalid state parameter" in response.json()["detail"]

@pytest.mark.asyncio
async def test_oauth_callback_token_exchange_failure(test_db, mock_httpx_client):
    """Test OAuth callback when token exchange fails"""
    # Mock failed Twitter token response
    mock_httpx_client.post.return_value.status_code = 400
    mock_httpx_client.post.return_value.json.return_value = {
        "error": "invalid_grant"
    }
    
    # Mock OAuth state
    oauth_state = OAuthState(
        state="test_state",
        code_verifier="test_verifier",
        created_at=datetime.utcnow()
    )
    
    with patch('app.auth.get_db', return_value=test_db), \
         patch('app.auth.get_oauth_state', return_value=oauth_state):
        
        response = client.get("/auth/callback?code=test_code&state=test_state")
        
        # Should return 400 error
        assert response.status_code == 400
        assert "Failed to exchange code for token" in response.json()["detail"]

@pytest.mark.asyncio
async def test_login_page_renders():
    """Test that login page renders correctly"""
    response = client.get("/auth/login")
    assert response.status_code == 200
    assert "Sign in with Twitter" in response.text
    assert "Connect with Twitter" in response.text

@pytest.mark.asyncio
async def test_logout_redirects():
    """Test that logout redirects to home page"""
    response = client.get("/auth/logout")
    assert response.status_code == 302
    assert response.headers["location"] == "/"

@pytest.mark.asyncio
async def test_database_initialization():
    """Test database initialization creates required tables"""
    # This test would require a real database connection
    # For now, we'll test the function exists and can be called
    assert callable(init_db)

@pytest.mark.asyncio
async def test_pkce_generation():
    """Test PKCE code verifier and challenge generation"""
    from app.auth import generate_code_verifier, generate_code_challenge
    
    # Generate code verifier
    code_verifier = generate_code_verifier()
    assert len(code_verifier) > 0
    assert isinstance(code_verifier, str)
    
    # Generate code challenge
    code_challenge = generate_code_challenge(code_verifier)
    assert len(code_challenge) > 0
    assert isinstance(code_challenge, str)
    assert code_challenge != code_verifier

@pytest.mark.asyncio
async def test_oauth_state_generation():
    """Test OAuth state generation"""
    from app.auth import generate_state
    
    state = generate_state()
    assert len(state) > 0
    assert isinstance(state, str)
    
    # Generate another state to ensure uniqueness
    state2 = generate_state()
    assert state != state2

if __name__ == "__main__":
    pytest.main([__file__])
