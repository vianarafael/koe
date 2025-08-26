from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

class User(BaseModel):
    id: str  # UUID
    email: str
    username: str
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class UserLogin(BaseModel):
    email: str
    username: str

class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    created_at: datetime

# Site Management Models
class Site(BaseModel):
    id: Optional[str] = None
    user_id: str
    domain: str
    created_at: Optional[datetime] = None
    is_active: bool = True

class SiteCreate(BaseModel):
    domain: str

class SiteResponse(BaseModel):
    id: str
    domain: str
    created_at: datetime
    is_active: bool

# Link Tracking Models
class SourceType(str, Enum):
    x = "x"
    reddit = "reddit"
    linkedin = "linkedin"
    other = "other"

class EventKind(str, Enum):
    click = "click"
    pageview = "pageview"

class TrackedLink(BaseModel):
    id: Optional[str] = None
    user_id: str
    site_id: str
    original_url: str
    source: SourceType
    short_code: str
    utm_source: str
    utm_medium: str = "social"
    utm_campaign: str = "link_tracking"
    created_at: Optional[datetime] = None
    is_active: bool = True

class TrackedLinkCreate(BaseModel):
    site_id: str
    original_url: str
    source: SourceType
    campaign: Optional[str] = None

class TrackedLinkResponse(BaseModel):
    id: str
    original_url: str
    short_url: str
    source: str
    clicks_24h: int
    created_at: datetime
    is_active: bool

# Event Tracking Models
class Event(BaseModel):
    id: Optional[str] = None
    tracked_link_id: Optional[str] = None
    site_id: str
    user_id: str
    kind: EventKind
    ts: datetime
    ip_hash: Optional[str] = None
    ua_hash: Optional[str] = None
    referer: Optional[str] = None
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    country: Optional[str] = None
    path: Optional[str] = None
    session_id: Optional[str] = None

class EventCreate(BaseModel):
    tracked_link_id: Optional[str] = None
    site_id: str
    user_id: str
    kind: EventKind
    path: Optional[str] = None
    referer: Optional[str] = None
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    session_id: Optional[str] = None

# Analytics Models
class TrafficSummary(BaseModel):
    date: str  # YYYY-MM-DD
    source: str
    clicks: int

class HourlyTraffic(BaseModel):
    hour: str  # 00-23
    source: str
    visits: int

class Analytics24h(BaseModel):
    total_visits: int
    by_source: dict[str, int]
    hourly_data: List[HourlyTraffic]

# Session Management
class SessionData(BaseModel):
    user_id: str
    email: str
    username: str








