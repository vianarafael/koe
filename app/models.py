from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
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
    id: Optional[str] = None  # UUID for database record
    tweet_id: str
    user_id: str
    tweet_text: Optional[str] = None
    like_count: int = 0
    retweet_count: int = 0
    reply_count: int = 0
    mention_count: int = 0
    engagement_score: int = 0
    posted_date: Optional[datetime] = None
    fetched_at: datetime = Field(default_factory=datetime.utcnow)

class CSVUploadResponse(BaseModel):
    message: str
    records_processed: int
    records_stored: int
    errors: List[str] = []

class CSVParseError(BaseModel):
    row: int
    error: str
    data: dict

class SessionData(BaseModel):
    user_id: str
    email: str
    username: str

class SetPointValuesRequest(BaseModel):
    like: int = Field(ge=0, description="Points for each like")
    retweet: int = Field(ge=0, description="Points for each retweet")
    reply: int = Field(ge=0, description="Points for each reply")
    mention: int = Field(ge=0, description="Points for each mention")

class PointValuesResponse(BaseModel):
    message: str
    updated_point_values: dict
    recalculated_count: int

class EngagementScoreCalculation(BaseModel):
    tweet_id: str
    like_score: int
    retweet_score: int
    reply_score: int
    mention_score: int
    total_score: int
    calculation_details: dict

# Goal System Models (Sprint 2)
class GoalTemplate(BaseModel):
    id: str
    name: str
    description: str
    category: str
    primary_metric: str
    secondary_metrics: List[str] = []
    default_targets: dict
    coaching_tips: List[str] = []

class UserGoal(BaseModel):
    id: Optional[str] = None
    user_id: str
    goal_type: str
    target_value: int
    start_date: datetime
    end_date: datetime
    current_value: int = 0
    unit: str
    is_primary: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class GoalProgress(BaseModel):
    current_value: int
    target_value: int
    progress_percentage: float
    current_pace: float
    needed_pace: float
    on_track: bool
    days_remaining: int
    trend: str

class CreateGoalRequest(BaseModel):
    goal_type: str
    target_value: int
    timeframe_days: int
    is_custom: bool = False
    custom_metric: Optional[str] = None

class GoalResponse(BaseModel):
    message: str
    goal: UserGoal
    progress: GoalProgress
    coaching_feedback: Optional[str] = None
