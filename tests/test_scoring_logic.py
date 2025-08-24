import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.scoring import EngagementScoring, scoring_engine, calculate_and_store_score, recalculate_all_user_scores
from app.models import TweetEngagement, User
from app.db import get_db, store_tweet_engagement, get_user_engagements
from datetime import datetime

class TestEngagementScoring:
    """Test the engagement scoring functionality"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.scoring = EngagementScoring()
        self.sample_engagement = TweetEngagement(
            id="test-id-123",
            tweet_id="123456789",
            user_id="user-123",
            tweet_text="Test tweet",
            like_count=10,
            retweet_count=5,
            reply_count=3,
            mention_count=2,
            engagement_score=0,
            fetched_at=datetime.utcnow()
        )
        self.sample_point_values = {
            "like": 1,
            "retweet": 2,
            "reply": 3,
            "mention": 1
        }
    
    def test_default_point_values(self):
        """Test default point values are set correctly"""
        default_values = self.scoring.get_default_point_values()
        
        assert default_values["like"] == 1
        assert default_values["retweet"] == 2
        assert default_values["reply"] == 3
        assert default_values["mention"] == 1
        
        # Ensure it's a copy, not the original
        default_values["like"] = 999
        assert self.scoring.default_point_values["like"] == 1
    
    def test_calculate_engagement_score_basic(self):
        """Test basic engagement score calculation"""
        score = self.scoring.calculate_engagement_score(
            self.sample_engagement, 
            self.sample_point_values
        )
        
        # Expected: (10 * 1) + (5 * 2) + (3 * 3) + (2 * 1) = 10 + 10 + 9 + 2 = 31
        expected_score = 31
        assert score == expected_score
    
    def test_calculate_engagement_score_zero_counts(self):
        """Test score calculation with zero engagement counts"""
        zero_engagement = TweetEngagement(
            id="zero-id",
            tweet_id="000000000",
            user_id="user-123",
            like_count=0,
            retweet_count=0,
            reply_count=0,
            mention_count=0,
            engagement_score=0,
            fetched_at=datetime.utcnow()
        )
        
        score = self.scoring.calculate_engagement_score(
            zero_engagement, 
            self.sample_point_values
        )
        
        assert score == 0
    
    def test_calculate_engagement_score_custom_points(self):
        """Test score calculation with custom point values"""
        custom_points = {
            "like": 5,
            "retweet": 10,
            "reply": 15,
            "mention": 5
        }
        
        score = self.scoring.calculate_engagement_score(
            self.sample_engagement, 
            custom_points
        )
        
        # Expected: (10 * 5) + (5 * 10) + (3 * 15) + (2 * 5) = 50 + 50 + 45 + 10 = 155
        expected_score = 155
        assert score == expected_score
    
    def test_calculate_engagement_score_missing_point_values(self):
        """Test score calculation with missing point values (should use defaults)"""
        partial_points = {
            "like": 2,
            "retweet": 4
            # Missing reply and mention
        }
        
        score = self.scoring.calculate_engagement_score(
            self.sample_engagement, 
            partial_points
        )
        
        # Expected: (10 * 2) + (5 * 4) + (3 * 3) + (2 * 1) = 20 + 20 + 9 + 2 = 51
        expected_score = 51
        assert score == expected_score
    
    def test_validate_point_values_valid(self):
        """Test point value validation with valid values"""
        valid_points = {
            "like": 1,
            "retweet": 2,
            "reply": 3,
            "mention": 1
        }
        
        assert self.scoring.validate_point_values(valid_points) == True
    
    def test_validate_point_values_missing_keys(self):
        """Test point value validation with missing keys"""
        invalid_points = {
            "like": 1,
            "retweet": 2
            # Missing reply and mention
        }
        
        assert self.scoring.validate_point_values(invalid_points) == False
    
    def test_validate_point_values_negative_values(self):
        """Test point value validation with negative values"""
        invalid_points = {
            "like": 1,
            "retweet": -2,  # Negative value
            "reply": 3,
            "mention": 1
        }
        
        assert self.scoring.validate_point_values(invalid_points) == False
    
    def test_validate_point_values_non_integer_values(self):
        """Test point value validation with non-integer values"""
        invalid_points = {
            "like": 1.5,  # Float value
            "retweet": 2,
            "reply": 3,
            "mention": 1
        }
        
        assert self.scoring.validate_point_values(invalid_points) == False
    
    def test_validate_point_values_zero_values(self):
        """Test point value validation with zero values (should be valid)"""
        valid_points = {
            "like": 0,
            "retweet": 0,
            "reply": 0,
            "mention": 0
        }
        
        assert self.scoring.validate_point_values(valid_points) == True

class TestScoringFunctions:
    """Test the scoring utility functions"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.sample_engagement = TweetEngagement(
            id="test-id-123",
            tweet_id="123456789",
            user_id="user-123",
            tweet_text="Test tweet",
            like_count=10,
            retweet_count=5,
            reply_count=3,
            mention_count=2,
            engagement_score=0,
            fetched_at=datetime.utcnow()
        )
        self.sample_point_values = {
            "like": 1,
            "retweet": 2,
            "reply": 3,
            "mention": 1
        }
    
    @pytest.mark.asyncio
    async def test_calculate_and_store_score_success(self):
        """Test successful score calculation and storage"""
        mock_db = AsyncMock()
        mock_db.commit = AsyncMock()
        
        # Mock successful storage
        with patch('app.scoring.store_tweet_engagement', return_value=True):
            result = await calculate_and_store_score(
                self.sample_engagement, 
                self.sample_point_values, 
                mock_db
            )
        
        assert result == True
        assert self.sample_engagement.engagement_score == 31  # Expected score
    
    @pytest.mark.asyncio
    async def test_calculate_and_store_score_storage_failure(self):
        """Test score calculation with storage failure"""
        mock_db = AsyncMock()
        
        # Mock failed storage
        with patch('app.scoring.store_tweet_engagement', return_value=False):
            result = await calculate_and_store_score(
                self.sample_engagement, 
                self.sample_point_values, 
                mock_db
            )
        
        assert result == False
        # Score should still be calculated even if storage fails
        assert self.sample_engagement.engagement_score == 31
    
    @pytest.mark.asyncio
    async def test_calculate_and_store_score_exception(self):
        """Test score calculation with exception handling"""
        mock_db = AsyncMock()
        
        # Mock exception in storage
        with patch('app.scoring.store_tweet_engagement', side_effect=Exception("DB Error")):
            result = await calculate_and_store_score(
                self.sample_engagement, 
                self.sample_point_values, 
                mock_db
            )
        
        assert result == False

class TestScoringIntegration:
    """Test scoring integration with database operations"""
    
    @pytest.mark.asyncio
    async def test_recalculate_user_scores(self):
        """Test recalculating scores for all user engagements"""
        mock_db = AsyncMock()
        
        # Mock user engagements
        mock_engagements = [
            TweetEngagement(
                id="1",
                tweet_id="tweet1",
                user_id="user123",
                like_count=5,
                retweet_count=2,
                reply_count=1,
                mention_count=0,
                engagement_score=0,
                fetched_at=datetime.utcnow()
            ),
            TweetEngagement(
                id="2",
                tweet_id="tweet2",
                user_id="user123",
                like_count=10,
                retweet_count=5,
                reply_count=3,
                mention_count=2,
                engagement_score=0,
                fetched_at=datetime.utcnow()
            )
        ]
        
        # Mock database operations
        with patch('app.scoring.get_user_engagements', return_value=mock_engagements), \
             patch('app.scoring.store_tweet_engagement', return_value=True):
            
            scoring = EngagementScoring()
            updated_count = await scoring.recalculate_user_scores(
                "user123", 
                {"like": 1, "retweet": 2, "reply": 3, "mention": 1}, 
                mock_db
            )
        
        assert updated_count == 2
        
        # Check scores were calculated correctly
        # Tweet 1: (5*1) + (2*2) + (1*3) + (0*1) = 5 + 4 + 3 + 0 = 12
        assert mock_engagements[0].engagement_score == 12
        
        # Tweet 2: (10*1) + (5*2) + (3*3) + (2*1) = 10 + 10 + 9 + 2 = 31
        assert mock_engagements[1].engagement_score == 31

class TestGlobalScoringEngine:
    """Test the global scoring engine instance"""
    
    def test_global_scoring_engine_exists(self):
        """Test that global scoring engine is properly initialized"""
        assert scoring_engine is not None
        assert isinstance(scoring_engine, EngagementScoring)
    
    def test_global_scoring_engine_default_values(self):
        """Test global scoring engine has correct default values"""
        default_values = scoring_engine.get_default_point_values()
        
        assert default_values["like"] == 1
        assert default_values["retweet"] == 2
        assert default_values["reply"] == 3
        assert default_values["mention"] == 1
    
    def test_global_scoring_engine_calculation(self):
        """Test global scoring engine calculation"""
        sample_engagement = TweetEngagement(
            id="test",
            tweet_id="123",
            user_id="user",
            like_count=2,
            retweet_count=1,
            reply_count=1,
            mention_count=0,
            engagement_score=0,
            fetched_at=datetime.utcnow()
        )
        
        point_values = {"like": 1, "retweet": 2, "reply": 3, "mention": 1}
        score = scoring_engine.calculate_engagement_score(sample_engagement, point_values)
        
        # Expected: (2*1) + (1*2) + (1*3) + (0*1) = 2 + 2 + 3 + 0 = 7
        assert score == 7

if __name__ == "__main__":
    pytest.main([__file__])
