import csv
import io
import uuid
from datetime import datetime, timezone
from typing import List, Tuple, Dict, Any
from fastapi import UploadFile, HTTPException
from app.models import TweetEngagement, CSVParseError

class CSVParser:
    """Parser for X Analytics CSV files"""
    
    # Common column names in X Analytics exports
    EXPECTED_COLUMNS = {
        'tweet_id': ['Tweet ID', 'tweet_id', 'id'],
        'tweet_text': ['Tweet text', 'Tweet Text', 'Text', 'text', 'tweet_text', 'content'],
        'posted_date': ['Posted date', 'Posted Date', 'Date', 'date', 'posted_date', 'created_at'],
        'like_count': ['Likes', 'likes', 'Like count', 'like_count', 'likes_count'],
        'retweet_count': ['Retweets', 'retweets', 'Retweet count', 'retweet_count', 'retweets_count', 'Reposts', 'reposts'],
        'reply_count': ['Replies', 'replies', 'Reply count', 'reply_count', 'replies_count'],
        'mention_count': ['Mentions', 'mentions', 'Mention count', 'mention_count', 'mentions_count']
    }
    
    def __init__(self):
        self.column_mapping = {}
        self.parse_errors = []
    
    def detect_column_mapping(self, header_row: List[str]) -> Dict[str, int]:
        """Detect which columns contain the expected data"""
        mapping = {}
        
        for expected_key, possible_names in self.EXPECTED_COLUMNS.items():
            for col_idx, col_name in enumerate(header_row):
                if col_name.strip() in possible_names:
                    mapping[expected_key] = col_idx
                    break
        
        # Check if this is account overview data (daily summaries)
        if self._is_account_overview_format(header_row):
            # For account overview, we can work with just date and engagement metrics
            # We'll create synthetic tweet records for each day
            return self._create_account_overview_mapping(header_row)
        
        # Validate that we have at least the essential columns for tweet-level data
        essential_columns = ['tweet_id', 'like_count', 'retweet_count', 'reply_count']
        missing_columns = [col for col in essential_columns if col not in mapping]
        
        if missing_columns:
            raise ValueError(f"Missing essential columns: {missing_columns}")
        
        return mapping
    
    def _is_account_overview_format(self, header_row: List[str]) -> bool:
        """Check if this is account overview data (daily summaries)"""
        account_overview_indicators = ['Impressions', 'Engagements', 'Profile visits', 'Create Post']
        return any(indicator in header_row for indicator in account_overview_indicators)
    
    def _create_account_overview_mapping(self, header_row: List[str]) -> Dict[str, int]:
        """Create column mapping for account overview format"""
        mapping = {}
        
        # Map the columns we can find
        for expected_key, possible_names in self.EXPECTED_COLUMNS.items():
            for col_idx, col_name in enumerate(header_row):
                if col_name.strip() in possible_names:
                    mapping[expected_key] = col_idx
                    break
        
        # For account overview, we don't need tweet_id or tweet_text
        # We'll generate synthetic ones for each day
        return mapping
    
    def parse_date(self, date_str: str) -> datetime:
        """Parse various date formats from X Analytics"""
        if not date_str or date_str.strip() == '':
            return None
        
        date_str = date_str.strip()
        
        # Common X Analytics date formats
        date_formats = [
            '%Y-%m-%d %H:%M:%S',  # 2024-01-15 14:30:00
            '%Y-%m-%d',           # 2024-01-15
            '%m/%d/%Y',           # 01/15/2024
            '%d/%m/%Y',           # 15/01/2024
            '%Y-%m-%dT%H:%M:%S', # 2024-01-15T14:30:00
            '%Y-%m-%dT%H:%M:%S.%fZ', # 2024-01-15T14:30:00.000Z
        ]
        
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        # If no format matches, return None
        return None
    
    def parse_integer(self, value: str, default: int = 0) -> int:
        """Parse integer values from CSV, handling various formats"""
        if not value or value.strip() == '':
            return default
        
        try:
            # Remove common non-numeric characters
            cleaned = value.strip().replace(',', '').replace('K', '000').replace('M', '000000')
            return int(float(cleaned))
        except (ValueError, TypeError):
            return default
    
    def parse_row(self, row: List[str], row_number: int, user_id: str) -> TweetEngagement:
        """Parse a single CSV row into a TweetEngagement object"""
        try:
            # Check if this is account overview data (missing tweet_id)
            is_account_overview = 'tweet_id' not in self.column_mapping
            
            if is_account_overview:
                # For account overview, create synthetic tweet data for each day
                return self._parse_account_overview_row(row, row_number, user_id)
            else:
                # For regular tweet data, parse normally
                return self._parse_tweet_row(row, row_number, user_id)
                
        except Exception as e:
            # Record parse error
            error = CSVParseError(
                row=row_number,
                error=str(e),
                data={col: row[idx] if idx < len(row) else '' for col, idx in self.column_mapping.items()}
            )
            self.parse_errors.append(error)
            raise
    
    def _parse_tweet_row(self, row: List[str], row_number: int, user_id: str) -> TweetEngagement:
        """Parse a regular tweet row with all required fields"""
        # Extract values using column mapping
        tweet_id = row[self.column_mapping['tweet_id']].strip()
        if not tweet_id:
            raise ValueError("Tweet ID cannot be empty")
        
        # Extract optional tweet text
        tweet_text = None
        if 'tweet_text' in self.column_mapping:
            tweet_text = row[self.column_mapping['tweet_text']].strip()
        
        # Parse engagement counts
        like_count = self.parse_integer(row[self.column_mapping['like_count']])
        retweet_count = self.parse_integer(row[self.column_mapping['retweet_count']])
        reply_count = self.parse_integer(row[self.column_mapping['reply_count']])
        
        # Parse mention count (optional)
        mention_count = 0
        if 'mention_count' in self.column_mapping:
            mention_count = self.parse_integer(row[self.column_mapping['mention_count']])
        
        # Parse posted date (optional)
        posted_date = None
        if 'posted_date' in self.column_mapping:
            posted_date = self.parse_date(row[self.column_mapping['posted_date']])
        
        return TweetEngagement(
            id=str(uuid.uuid4()),
            tweet_id=tweet_id,
            user_id=user_id,
            tweet_text=tweet_text,
            like_count=like_count,
            retweet_count=retweet_count,
            reply_count=reply_count,
            mention_count=mention_count,
            engagement_score=0,  # Will be calculated later
            posted_date=posted_date,
            fetched_at=datetime.now(timezone.utc)
        )
    
    def _parse_account_overview_row(self, row: List[str], row_number: int, user_id: str) -> TweetEngagement:
        """Parse an account overview row (daily summary) into a synthetic tweet record"""
        # Generate synthetic tweet ID for this day
        synthetic_tweet_id = f"daily_summary_{row_number}_{user_id}"
        
        # Create synthetic tweet text describing the day's performance
        date_str = row[self.column_mapping['posted_date']].strip() if 'posted_date' in self.column_mapping else f"Day {row_number}"
        likes = self.parse_integer(row[self.column_mapping['like_count']]) if 'like_count' in self.column_mapping else 0
        replies = self.parse_integer(row[self.column_mapping['reply_count']]) if 'reply_count' in self.column_mapping else 0
        reposts = self.parse_integer(row[self.column_mapping['retweet_count']]) if 'retweet_count' in self.column_mapping else 0
        
        synthetic_tweet_text = f"Daily summary for {date_str}: {likes} likes, {replies} replies, {reposts} reposts"
        
        # Parse engagement counts
        like_count = likes
        retweet_count = reposts
        reply_count = replies
        mention_count = 0  # Not available in account overview
        
        # Parse posted date
        posted_date = None
        if 'posted_date' in self.column_mapping:
            posted_date = self.parse_date(row[self.column_mapping['posted_date']])
        
        return TweetEngagement(
            id=str(uuid.uuid4()),
            tweet_id=synthetic_tweet_id,
            user_id=user_id,
            tweet_text=synthetic_tweet_text,
            like_count=like_count,
            retweet_count=retweet_count,
            reply_count=reply_count,
            mention_count=mention_count,
            engagement_score=0,  # Will be calculated later
            posted_date=posted_date,
            fetched_at=datetime.now(timezone.utc)
        )
    
    async def parse_csv_file(self, file: UploadFile, user_id: str) -> Tuple[List[TweetEngagement], List[CSVParseError]]:
        """Parse uploaded CSV file and extract engagement data"""
        if not file.filename.lower().endswith('.csv'):
            raise HTTPException(status_code=400, detail="File must be a CSV")
        
        try:
            # Read file content
            content = await file.read()
            content_str = content.decode('utf-8')
            
            # Parse CSV
            csv_reader = csv.reader(io.StringIO(content_str))
            
            # Read header row
            try:
                header_row = next(csv_reader)
            except StopIteration:
                raise HTTPException(status_code=400, detail="CSV file is empty")
            
            # Detect column mapping
            try:
                self.column_mapping = self.detect_column_mapping(header_row)
            except ValueError as e:
                raise HTTPException(status_code=400, detail=f"Invalid CSV format: {str(e)}")
            
            # Parse data rows
            engagements = []
            self.parse_errors = []
            
            for row_number, row in enumerate(csv_reader, start=2):  # Start at 2 (after header)
                if not row or all(cell.strip() == '' for cell in row):
                    continue  # Skip empty rows
                
                try:
                    engagement = self.parse_row(row, row_number, user_id)
                    engagements.append(engagement)
                except Exception as e:
                    # Record parse error with more detail
                    error = CSVParseError(
                        row=row_number,
                        error=str(e),
                        data={col: row[idx] if idx < len(row) else '' for col, idx in self.column_mapping.items()}
                    )
                    self.parse_errors.append(error)
                    continue
            
            return engagements, self.parse_errors
            
        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail="CSV file must be UTF-8 encoded")
        except Exception as e:
            # More detailed error logging
            import traceback
            error_details = f"Error parsing CSV: {str(e)}\nTraceback: {traceback.format_exc()}"
            print(f"CSV parsing error: {error_details}")  # Debug logging
            raise HTTPException(status_code=500, detail=f"Error parsing CSV: {str(e)}")

# Global parser instance
csv_parser = CSVParser()
