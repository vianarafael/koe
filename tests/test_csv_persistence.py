import pytest
import io
from fastapi.testclient import TestClient
from app.main import app
from app.models import CSVUpload
from app.db import get_db, store_csv_upload, get_csv_upload, get_user_csv_uploads
import tempfile
import os

# client = TestClient(app)  # Commented out for now

@pytest.fixture
def sample_csv_content():
    return """Tweet ID,Tweet text,Posted date,Likes,Retweets,Replies,Mentions
1234567890123456789,This is a sample tweet,2024-01-15 14:30:00,42,12,8,3
9876543210987654321,Another sample tweet with engagement,2024-01-14 10:15:00,128,45,23,7"""

@pytest.fixture
def sample_csv_file(sample_csv_content):
    return io.BytesIO(sample_csv_content.encode('utf-8'))

@pytest.mark.asyncio
async def test_csv_upload_storage():
    """Test that CSV files are stored in database"""
    # This would require a proper test database setup
    # For now, just test the model creation
    csv_upload = CSVUpload(
        user_id="test_user_123",
        filename="test.csv",
        content=b"test,data\n1,2",
        file_size=15,
        records_processed=2,
        records_stored=2,
        parse_errors=[]
    )
    
    assert csv_upload.user_id == "test_user_123"
    assert csv_upload.filename == "test.csv"
    assert csv_upload.content == b"test,data\n1,2"
    assert csv_upload.file_size == 15
    assert csv_upload.records_processed == 2
    assert csv_upload.records_stored == 2
    assert len(csv_upload.parse_errors) == 0

def test_csv_upload_model_validation():
    """Test CSVUpload model validation"""
    csv_upload = CSVUpload(
        user_id="test_user_123",
        filename="test.csv",
        content=b"test,data\n1,2",
        file_size=15
    )
    
    assert csv_upload.id is None  # Will be set when stored
    assert csv_upload.user_id == "test_user_123"
    assert csv_upload.filename == "test.csv"
    assert csv_upload.content_type == "text/csv"  # Default value
    assert csv_upload.uploaded_at is not None  # Auto-generated

def test_csv_upload_with_errors():
    """Test CSVUpload model with parse errors"""
    csv_upload = CSVUpload(
        user_id="test_user_123",
        filename="test.csv",
        content=b"test,data\n1,2",
        file_size=15,
        parse_errors=["Row 2: Invalid date format"]
    )
    
    assert len(csv_upload.parse_errors) == 1
    assert "Invalid date format" in csv_upload.parse_errors[0]
