import pytest
from app.routes.dashboard import sort_engagements, calculate_engagement_stats
from app.models import TweetEngagement
from datetime import datetime

@pytest.fixture
def sample_engagements():
    """Sample engagement data for testing"""
    return [
        TweetEngagement(
            id="1",
            tweet_id="tweet1",
            user_id="user123",
            tweet_text="First tweet with high engagement",
            like_count=50,
            retweet_count=25,
            reply_count=15,
            mention_count=5,
            engagement_score=150,
            posted_date=datetime(2024, 1, 15),
            fetched_at=datetime(2024, 1, 15, 10, 0)
        ),
        TweetEngagement(
            id="2",
            tweet_id="tweet2",
            user_id="user123",
            tweet_text="Second tweet with medium engagement",
            like_count=30,
            retweet_count=15,
            reply_count=10,
            mention_count=2,
            engagement_score=87,
            posted_date=datetime(2024, 1, 14),
            fetched_at=datetime(2024, 1, 14, 10, 0)
        ),
        TweetEngagement(
            id="3",
            tweet_id="tweet3",
            user_id="user123",
            tweet_text="Third tweet with low engagement",
            like_count=10,
            retweet_count=5,
            reply_count=3,
            mention_count=1,
            engagement_score=28,
            posted_date=datetime(2024, 1, 13),
            fetched_at=datetime(2024, 1, 13, 10, 0)
        )
    ]

class TestDashboardSorting:
    """Test dashboard sorting functionality"""
    
    def test_sort_engagements_by_score_desc(self, sample_engagements):
        """Test sorting engagements by score in descending order"""
        sorted_engagements = sort_engagements(sample_engagements, "score", "desc")
        
        assert len(sorted_engagements) == 3
        assert sorted_engagements[0].engagement_score == 150  # Highest score first
        assert sorted_engagements[1].engagement_score == 87
        assert sorted_engagements[2].engagement_score == 28
    
    def test_sort_engagements_by_score_asc(self, sample_engagements):
        """Test sorting engagements by score in ascending order"""
        sorted_engagements = sort_engagements(sample_engagements, "score", "asc")
        
        assert len(sorted_engagements) == 3
        assert sorted_engagements[0].engagement_score == 28  # Lowest score first
        assert sorted_engagements[1].engagement_score == 87
        assert sorted_engagements[2].engagement_score == 150
    
    def test_sort_engagements_by_date_desc(self, sample_engagements):
        """Test sorting engagements by date in descending order"""
        sorted_engagements = sort_engagements(sample_engagements, "date", "desc")
        
        assert len(sorted_engagements) == 3
        assert sorted_engagements[0].posted_date == datetime(2024, 1, 15)  # Latest date first
        assert sorted_engagements[1].posted_date == datetime(2024, 1, 14)
        assert sorted_engagements[2].posted_date == datetime(2024, 1, 13)
    
    def test_sort_engagements_by_engagement_desc(self, sample_engagements):
        """Test sorting engagements by total engagement count"""
        sorted_engagements = sort_engagements(sample_engagements, "engagement", "desc")
        
        # Total engagement: tweet1=95, tweet2=57, tweet3=19
        assert len(sorted_engagements) == 3
        assert sorted_engagements[0].tweet_id == "tweet1"  # Highest total engagement
        assert sorted_engagements[1].tweet_id == "tweet2"
        assert sorted_engagements[2].tweet_id == "tweet3"
    
    def test_sort_engagements_by_likes_desc(self, sample_engagements):
        """Test sorting engagements by likes count"""
        sorted_engagements = sort_engagements(sample_engagements, "likes", "desc")
        
        assert len(sorted_engagements) == 3
        assert sorted_engagements[0].like_count == 50  # Highest likes first
        assert sorted_engagements[1].like_count == 30
        assert sorted_engagements[2].like_count == 10
    
    def test_sort_engagements_by_retweets_desc(self, sample_engagements):
        """Test sorting engagements by retweets count"""
        sorted_engagements = sort_engagements(sample_engagements, "retweets", "desc")
        
        assert len(sorted_engagements) == 3
        assert sorted_engagements[0].retweet_count == 25  # Highest retweets first
        assert sorted_engagements[1].retweet_count == 15
        assert sorted_engagements[2].retweet_count == 5
    
    def test_sort_engagements_by_replies_desc(self, sample_engagements):
        """Test sorting engagements by replies count"""
        sorted_engagements = sort_engagements(sample_engagements, "replies", "desc")
        
        assert len(sorted_engagements) == 3
        assert sorted_engagements[0].reply_count == 15  # Highest replies first
        assert sorted_engagements[1].reply_count == 10
        assert sorted_engagements[2].reply_count == 3
    
    def test_sort_engagements_default(self, sample_engagements):
        """Test default sorting (by score, descending)"""
        sorted_engagements = sort_engagements(sample_engagements, "invalid", "invalid")
        
        assert len(sorted_engagements) == 3
        assert sorted_engagements[0].engagement_score == 150  # Should default to score desc

class TestDashboardStatistics:
    """Test dashboard statistics calculation"""
    
    def test_calculate_engagement_stats_with_data(self, sample_engagements):
        """Test statistics calculation with engagement data"""
        stats = calculate_engagement_stats(sample_engagements)
        
        assert stats["total_score"] == 265  # 150 + 87 + 28
        assert stats["average_score"] == 88.33  # 265 / 3
        assert stats["top_score"] == 150
        assert stats["engagement_breakdown"]["likes"] == 90  # 50 + 30 + 10
        assert stats["engagement_breakdown"]["retweets"] == 45  # 25 + 15 + 5
        assert stats["engagement_breakdown"]["replies"] == 28  # 15 + 10 + 3
        assert stats["engagement_breakdown"]["mentions"] == 8  # 5 + 2 + 1
    
    def test_calculate_engagement_stats_empty(self):
        """Test statistics calculation with empty data"""
        stats = calculate_engagement_stats([])
        
        assert stats["total_score"] == 0
        assert stats["average_score"] == 0
        assert stats["top_score"] == 0
        assert stats["engagement_breakdown"]["likes"] == 0
        assert stats["engagement_breakdown"]["retweets"] == 0
        assert stats["engagement_breakdown"]["replies"] == 0
        assert stats["engagement_breakdown"]["mentions"] == 0

if __name__ == "__main__":
    pytest.main([__file__])
