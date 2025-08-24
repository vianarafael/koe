import asyncio
from typing import Dict, List, Optional
from app.models import TweetEngagement
from app.db import get_user_engagements, update_engagement_score

class EngagementScoring:
    """Engine for calculating engagement scores based on configurable point values"""
    
    def __init__(self):
        self.default_point_values = {
            "like": 1,
            "retweet": 2,
            "reply": 3,
            "mention": 1
        }
    
    def calculate_engagement_score(self, engagement: TweetEngagement, point_values: Dict[str, int]) -> int:
        """
        Calculate engagement score using the formula:
        (likes × like_points) + (retweets × retweet_points) + (replies × reply_points) + (mentions × mention_points)
        """
        like_score = engagement.like_count * point_values.get("like", 0)
        retweet_score = engagement.retweet_count * point_values.get("retweet", 0)
        reply_score = engagement.reply_count * point_values.get("reply", 0)
        mention_score = engagement.mention_count * point_values.get("mention", 0)
        
        return like_score + retweet_score + reply_score + mention_score
    
    async def recalculate_user_scores(self, user_id: str, point_values: Dict[str, int], db) -> int:
        """
        Recalculate engagement scores for all user engagements using new point values
        Returns the number of scores recalculated
        """
        try:
            # Get all user engagements
            engagements = await get_user_engagements(db, user_id, limit=10000)
            
            if not engagements:
                return 0
            
            # Recalculate scores for each engagement
            recalculated_count = 0
            for engagement in engagements:
                new_score = self.calculate_engagement_score(engagement, point_values)
                
                # Update the engagement score in the database
                await update_engagement_score(db, engagement.id, new_score)
                recalculated_count += 1
            
            return recalculated_count
            
        except Exception as e:
            print(f"Error recalculating user scores: {e}")
            raise
    
    def get_default_point_values(self) -> Dict[str, int]:
        """Get default point values for engagement types"""
        return self.default_point_values.copy()
    
    def validate_point_values(self, point_values: Dict[str, int]) -> bool:
        """Validate that point values are valid (non-negative integers)"""
        required_keys = {"like", "retweet", "reply", "mention"}
        
        # Check if all required keys are present
        if not all(key in point_values for key in required_keys):
            return False
        
        # Check if all values are non-negative integers
        for key, value in point_values.items():
            if not isinstance(value, int) or value < 0:
                return False
        
        return True

# Global scoring engine instance
scoring_engine = EngagementScoring()

async def calculate_and_store_score(engagement: TweetEngagement, point_values: Dict[str, int], db) -> bool:
    """Calculate engagement score and store it in the database"""
    try:
        score = scoring_engine.calculate_engagement_score(engagement, point_values)
        await update_engagement_score(db, engagement.id, score)
        return True
    except Exception as e:
        print(f"Error calculating and storing score: {e}")
        return False

async def recalculate_all_user_scores(user_id: str, point_values: Dict[str, int], db) -> int:
    """Recalculate all engagement scores for a user"""
    return await scoring_engine.recalculate_user_scores(user_id, point_values, db)

async def process_csv_engagements_with_scoring(engagements: List[TweetEngagement], point_values: Dict[str, int], db) -> int:
    """Process CSV engagements and calculate scores for each"""
    processed_count = 0
    
    for engagement in engagements:
        try:
            # Calculate score using current point values
            score = scoring_engine.calculate_engagement_score(engagement, point_values)
            
            # Update the engagement with the calculated score
            engagement.engagement_score = score
            
            # Store in database
            await update_engagement_score(db, engagement.id, score)
            processed_count += 1
            
        except Exception as e:
            print(f"Error processing engagement {engagement.id}: {e}")
            continue
    
    return processed_count
