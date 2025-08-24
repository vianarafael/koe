import pytest
import io
import csv
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient
from fastapi import UploadFile
from app.main import app
from app.csv_parser import CSVParser, csv_parser
from app.models import TweetEngagement, CSVParseError
from app.db import init_db, get_db, store_tweet_engagement, store_multiple_engagements
from datetime import datetime

# Test client
client = TestClient(app)

@pytest.fixture
def sample_csv_content():
    """Sample CSV content for testing"""
    return """Tweet ID,Tweet text,Posted date,Likes,Retweets,Replies,Mentions
1234567890123456789,This is a sample tweet,2024-01-15 14:30:00,42,12,8,3
9876543210987654321,Another sample tweet with engagement,2024-01-14 10:15:00,128,45,23,7
5556667778889990000,Third sample tweet,2024-01-13 16:45:00,67,18,12,2"""

@pytest.fixture
def sample_csv_file(sample_csv_content):
    """Create a mock CSV file for testing"""
    file = MagicMock(spec=UploadFile)
    file.filename = "test.csv"
    file.content_type = "text/csv"
    file.file = io.BytesIO(sample_csv_content.encode('utf-8'))
    return file

@pytest.fixture
def csv_parser_instance():
    """Create a fresh CSV parser instance for testing"""
    return CSVParser()

def test_csv_parser_initialization():
    """Test CSV parser initialization"""
    parser = CSVParser()
    assert parser.column_mapping == {}
    assert parser.parse_errors == []

def test_detect_column_mapping_valid_headers():
    """Test column mapping detection with valid headers"""
    parser = CSVParser()
    headers = ["Tweet ID", "Tweet text", "Posted date", "Likes", "Retweets", "Replies", "Mentions"]
    
    mapping = parser.detect_column_mapping(headers)
    
    assert mapping["tweet_id"] == 0
    assert mapping["tweet_text"] == 1
    assert mapping["posted_date"] == 2
    assert mapping["like_count"] == 3
    assert mapping["retweet_count"] == 4
    assert mapping["reply_count"] == 5
    assert mapping["mention_count"] == 6

def test_detect_column_mapping_missing_essential_columns():
    """Test column mapping detection with missing essential columns"""
    parser = CSVParser()
    headers = ["Tweet ID", "Tweet text", "Posted date"]  # Missing engagement columns
    
    with pytest.raises(ValueError, match="Missing essential columns"):
        parser.detect_column_mapping(headers)

def test_detect_column_mapping_case_insensitive():
    """Test column mapping detection with different case variations"""
    parser = CSVParser()
    headers = ["tweet id", "tweet text", "posted date", "likes", "retweets", "replies"]
    
    mapping = parser.detect_column_mapping(headers)
    
    assert "tweet_id" in mapping
    assert "tweet_text" in mapping
    assert "like_count" in mapping
    assert "retweet_count" in mapping
    assert "reply_count" in mapping

def test_parse_date_valid_formats():
    """Test date parsing with various valid formats"""
    parser = CSVParser()
    
    # Test different date formats
    assert parser.parse_date("2024-01-15 14:30:00") == datetime(2024, 1, 15, 14, 30)
    assert parser.parse_date("2024-01-15") == datetime(2024, 1, 15)
    assert parser.parse_date("01/15/2024") == datetime(2024, 1, 15)
    assert parser.parse_date("15/01/2024") == datetime(2024, 1, 15)

def test_parse_date_invalid_formats():
    """Test date parsing with invalid formats"""
    parser = CSVParser()
    
    # Test invalid dates
    assert parser.parse_date("invalid-date") is None
    assert parser.parse_date("") is None
    assert parser.parse_date("   ") is None

def test_parse_integer_valid_values():
    """Test integer parsing with various valid formats"""
    parser = CSVParser()
    
    assert parser.parse_integer("42") == 42
    assert parser.parse_integer("1,234") == 1234
    assert parser.parse_integer("2.5K") == 2500
    assert parser.parse_integer("1.2M") == 1200000
    assert parser.parse_integer("0") == 0

def test_parse_integer_invalid_values():
    """Test integer parsing with invalid values"""
    parser = CSVParser()
    
    assert parser.parse_integer("") == 0
    assert parser.parse_integer("   ") == 0
    assert parser.parse_integer("invalid") == 0
    assert parser.parse_integer("abc123") == 0

def test_parse_row_valid_data():
    """Test parsing a valid CSV row"""
    parser = CSVParser()
    parser.column_mapping = {
        "tweet_id": 0,
        "tweet_text": 1,
        "posted_date": 2,
        "like_count": 3,
        "retweet_count": 4,
        "reply_count": 5,
        "mention_count": 6
    }
    
    row = ["123456789", "Sample tweet", "2024-01-15", "42", "12", "8", "3"]
    user_id = "test-user-id"
    
    engagement = parser.parse_row(row, 2, user_id)
    
    assert engagement.tweet_id == "123456789"
    assert engagement.tweet_text == "Sample tweet"
    assert engagement.like_count == 42
    assert engagement.retweet_count == 12
    assert engagement.reply_count == 8
    assert engagement.mention_count == 3
    assert engagement.user_id == user_id
    assert engagement.engagement_score == 0  # Default value

def test_parse_row_missing_optional_columns():
    """Test parsing row with missing optional columns"""
    parser = CSVParser()
    parser.column_mapping = {
        "tweet_id": 0,
        "like_count": 1,
        "retweet_count": 2,
        "reply_count": 3
    }
    
    row = ["123456789", "42", "12", "8"]
    user_id = "test-user-id"
    
    engagement = parser.parse_row(row, 2, user_id)
    
    assert engagement.tweet_id == "123456789"
    assert engagement.tweet_text is None
    assert engagement.posted_date is None
    assert engagement.mention_count == 0  # Default value

def test_parse_row_empty_tweet_id():
    """Test parsing row with empty tweet ID"""
    parser = CSVParser()
    parser.column_mapping = {
        "tweet_id": 0,
        "like_count": 1,
        "retweet_count": 2,
        "reply_count": 3
    }
    
    row = ["", "42", "12", "8"]
    user_id = "test-user-id"
    
    with pytest.raises(ValueError, match="Tweet ID cannot be empty"):
        parser.parse_row(row, 2, user_id)

@pytest.mark.asyncio
async def test_parse_csv_file_valid_content(sample_csv_file):
    """Test parsing a valid CSV file"""
    parser = CSVParser()
    user_id = "test-user-id"
    
    engagements, errors = await parser.parse_csv_file(sample_csv_file, user_id)
    
    assert len(engagements) == 3
    assert len(errors) == 0
    
    # Check first engagement
    first = engagements[0]
    assert first.tweet_id == "1234567890123456789"
    assert first.tweet_text == "This is a sample tweet"
    assert first.like_count == 42
    assert first.retweet_count == 12
    assert first.reply_count == 8
    assert first.mention_count == 3

@pytest.mark.asyncio
async def test_parse_csv_file_invalid_file_type():
    """Test parsing with invalid file type"""
    parser = CSVParser()
    file = MagicMock(spec=UploadFile)
    file.filename = "test.txt"
    user_id = "test-user-id"
    
    with pytest.raises(Exception, match="File must be a CSV"):
        await parser.parse_csv_file(file, user_id)

@pytest.mark.asyncio
async def test_parse_csv_file_empty_file():
    """Test parsing an empty CSV file"""
    parser = CSVParser()
    file = MagicMock(spec=UploadFile)
    file.filename = "empty.csv"
    file.file = io.BytesIO(b"")
    user_id = "test-user-id"
    
    with pytest.raises(Exception, match="CSV file is empty"):
        await parser.parse_csv_file(file, user_id)

@pytest.mark.asyncio
async def test_parse_csv_file_malformed_headers():
    """Test parsing CSV with malformed headers"""
    parser = CSVParser()
    file = MagicMock(spec=UploadFile)
    file.filename = "malformed.csv"
    file.file = io.BytesIO(b"Invalid,Headers\n1,2,3")
    user_id = "test-user-id"
    
    with pytest.raises(Exception, match="Invalid CSV format"):
        await parser.parse_csv_file(file, user_id)

def test_csv_parser_global_instance():
    """Test that global CSV parser instance works correctly"""
    assert csv_parser is not None
    assert isinstance(csv_parser, CSVParser)

@pytest.mark.asyncio
async def test_upload_csv_endpoint_authenticated(sample_csv_file):
    """Test CSV upload endpoint with authenticated user"""
    # Mock authentication
    with patch('app.routes.upload.get_current_user') as mock_auth, \
         patch('app.routes.upload.store_multiple_engagements') as mock_store:
        
        mock_user = MagicMock()
        mock_user.id = "test-user-id"
        mock_auth.return_value = mock_user
        
        mock_store.return_value = 3
        
        # Mock CSV parser
        with patch('app.routes.upload.csv_parser.parse_csv_file') as mock_parse:
            mock_parse.return_value = ([MagicMock() for _ in range(3)], [])
            
            # Test the endpoint
            response = client.post("/upload/csv", files={"file": ("test.csv", sample_csv_file.file, "text/csv")})
            
            # Should redirect to dashboard
            assert response.status_code == 302
            assert "upload_success=true" in response.headers["location"]

@pytest.mark.asyncio
async def test_upload_csv_endpoint_unauthenticated():
    """Test CSV upload endpoint without authentication"""
    response = client.post("/upload/csv", files={"file": ("test.csv", b"test", "text/csv")})
    
    # Should return 401
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_upload_page_authenticated():
    """Test upload page access with authenticated user"""
    with patch('app.routes.upload.get_current_user') as mock_auth:
        mock_user = MagicMock()
        mock_auth.return_value = mock_user
        
        response = client.get("/upload/")
        assert response.status_code == 200
        assert "Upload X Analytics CSV" in response.text

@pytest.mark.asyncio
async def test_upload_page_unauthenticated():
    """Test upload page access without authentication"""
    response = client.get("/upload/")
    
    # Should redirect to login
    assert response.status_code == 302
    assert "login" in response.headers["location"]

@pytest.mark.asyncio
async def test_sample_csv_download_authenticated():
    """Test sample CSV download with authenticated user"""
    with patch('app.routes.upload.get_current_user') as mock_auth:
        mock_user = MagicMock()
        mock_auth.return_value = mock_user
        
        response = client.get("/upload/sample")
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/csv"
        assert "sample_engagement_data.csv" in response.headers["content-disposition"]

@pytest.mark.asyncio
async def test_sample_csv_download_unauthenticated():
    """Test sample CSV download without authentication"""
    response = client.get("/upload/sample")
    
    # Should return 401
    assert response.status_code == 401

if __name__ == "__main__":
    pytest.main([__file__])
