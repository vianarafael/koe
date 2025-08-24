from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class User(BaseModel):
    id: str  # UUID
    email: str
    username: str
    hashed_password: str
    point_values: dict = Field(default_factory=lambda: {"like": 1, "retweet": 2, "reply": 3, "mention": 1})
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    point_values: dict
    created_at: datetime

class TweetEngagement(BaseModel):
    tweet_id: str
    user_id: str
    like_count: int
    retweet_count: int
    reply_count: int
    mention_count: int
    engagement_score: int
    fetched_at: datetime

class SessionData(BaseModel):
    user_id: str
    email: str
    username: str
