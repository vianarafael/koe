from typing import List, Dict, Optional
from app.models import TweetEngagement, User
from app.db import get_db, store_tweet_engagement, get_user_engagements

class EngagementScoring:
    """Calculate engagement scores based on user-defined point values"""
    
    def __init__(self):
        self.default_point_values = {
            "like": 1,
            "retweet": 2,
            "reply": 3,
            "mention": 1
        }
    
    def calculate_engagement_score(
        self, 
        engagement: TweetEngagement, 
        point_values: Dict[str, int]
    ) -> int:
        """Calculate engagement score for a single tweet"""
        score = 0
        
        # Apply point values to each engagement type
        score += engagement.like_count * point_values.get("like", 1)
        score += engagement.retweet_count * point_values.get("retweet", 2)
        score += engagement.reply_count * point_values.get("reply", 3)
        score += engagement.mention_count * point_values.get("mention", 1)
        
        return score
    
    def calculate_scores_for_user(
        self, 
        user_id: str, 
        point_values: Dict[str, int]
    ) -> List[TweetEngagement]:
        """Calculate engagement scores for all tweets of a specific user"""
        # This would typically be called from a database context
        # For now, return empty list - will be implemented with db context
        return []
    
    async def recalculate_user_scores(
        self, 
        user_id: str, 
        point_values: Dict[str, int],
        db
    ) -> int:
        """Recalculate engagement scores for all tweets of a user with new point values"""
        updated_count = 0
        
        # Get all engagements for the user
        engagements = await get_user_engagements(db, user_id, limit=1000)
        
        for engagement in engagements:
            # Calculate new score
            new_score = self.calculate_engagement_score(engagement, point_values)
            
            # Update engagement score
            engagement.engagement_score = new_score
            
            # Store updated engagement
            if await store_tweet_engagement(db, engagement):
                updated_count += 1
        
        return updated_count
    
    def get_default_point_values(self) -> Dict[str, int]:
        """Get default point values for new users"""
        return self.default_point_values.copy()
    
    def validate_point_values(self, point_values: Dict[str, int]) -> bool:
        """Validate that point values are reasonable"""
        required_keys = {"like", "retweet", "reply", "mention"}
        
        # Check all required keys are present
        if not all(key in point_values for key in required_keys):
            return False
        
        # Check all values are non-negative integers
        for key, value in point_values.items():
            if not isinstance(value, int) or value < 0:
                return False
        
        return True

# Global scoring instance
scoring_engine = EngagementScoring()

async def calculate_and_store_score(
    engagement: TweetEngagement, 
    point_values: Dict[str, int],
    db
) -> bool:
    """Calculate engagement score and store it in the database"""
    try:
        # Calculate score
        score = scoring_engine.calculate_engagement_score(engagement, point_values)
        engagement.engagement_score = score
        
        # Store updated engagement
        return await store_tweet_engagement(db, engagement)
    except Exception as e:
        print(f"Error calculating score: {e}")
        return False

async def recalculate_all_user_scores(
    user_id: str, 
    point_values: Dict[str, int],
    db
) -> int:
    """Recalculate all engagement scores for a user"""
    return await scoring_engine.recalculate_user_scores(user_id, point_values, db)

async def process_csv_engagements_with_scoring(
    engagements: List[TweetEngagement], 
    user_id: str,
    point_values: Dict[str, int],
    db
) -> int:
    """Process CSV engagements and calculate scores in one operation"""
    processed_count = 0
    
    for engagement in engagements:
        # Set user ID
        engagement.user_id = user_id
        
        # Calculate and set engagement score
        score = scoring_engine.calculate_engagement_score(engagement, point_values)
        engagement.engagement_score = score
        
        # Store in database
        if await store_tweet_engagement(db, engagement):
            processed_count += 1
    
    return processed_count
