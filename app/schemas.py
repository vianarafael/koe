from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class AuthenticateUserRequest(BaseModel):
    oauth_token: str
    oauth_verifier: str

class SetPointValuesRequest(BaseModel):
    like: int
    retweet: int
    reply: int
    mention: int

class TweetData(BaseModel):
    tweet_id: str
    text: Optional[str] = None
    engagement_score: int
    like_count: int
    retweet_count: int
    reply_count: int
    mention_count: int
    created_at: datetime

class EngagementDashboardResponse(BaseModel):
    tweets: List[TweetData]
    total_score: int
