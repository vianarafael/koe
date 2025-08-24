import aiosqlite
import uuid
from datetime import datetime, timedelta
from typing import List, Optional
from app.settings import settings
from app.models import User, UserCreate, UserResponse, TweetEngagement

async def get_db():
    db = await aiosqlite.connect(settings.DATABASE_URL.replace('sqlite:///', ''))
    db.row_factory = aiosqlite.Row
    try:
        yield db
    finally:
        await db.close()

async def init_db():
    """Initialize database with required tables"""
    async with aiosqlite.connect(settings.DATABASE_URL.replace('sqlite:///', '')) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                username TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL,
                point_values TEXT NOT NULL,
                created_at TEXT NOT NULL,
                is_active BOOLEAN NOT NULL DEFAULT 1
            )
        ''')
        
        await db.execute('''
            CREATE TABLE IF NOT EXISTS tweet_engagements (
                id TEXT PRIMARY KEY,
                tweet_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                tweet_text TEXT,
                like_count INTEGER NOT NULL DEFAULT 0,
                retweet_count INTEGER NOT NULL DEFAULT 0,
                reply_count INTEGER NOT NULL DEFAULT 0,
                mention_count INTEGER NOT NULL DEFAULT 0,
                engagement_score INTEGER NOT NULL DEFAULT 0,
                posted_date TEXT,
                fetched_at TEXT NOT NULL,
                UNIQUE(tweet_id, user_id)
            )
        ''')
        
        await db.commit()

async def create_user(db: aiosqlite.Connection, user_data: UserCreate, hashed_password: str) -> User:
    """Create a new user in the database"""
    user = User(
        id=str(uuid.uuid4()),
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password
    )
    
    await db.execute('''
        INSERT INTO users (id, email, username, hashed_password, point_values, created_at, is_active)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        user.id, user.email, user.username, user.hashed_password,
        str(user.point_values), user.created_at.isoformat(), user.is_active
    ))
    await db.commit()
    return user

async def get_user_by_email(db: aiosqlite.Connection, email: str) -> User | None:
    """Get user by email"""
    async with db.execute('''
        SELECT * FROM users WHERE email = ? AND is_active = 1
    ''', (email,)) as cursor:
        row = await cursor.fetchone()
        if row:
            return User(
                id=row['id'],
                email=row['email'],
                username=row['username'],
                hashed_password=row['hashed_password'],
                point_values=eval(row['point_values']),
                created_at=datetime.fromisoformat(row['created_at']),
                is_active=bool(row['is_active'])
            )
        return None

async def get_user_by_id(db: aiosqlite.Connection, user_id: str) -> User | None:
    """Get user by ID"""
    async with db.execute('''
        SELECT * FROM users WHERE id = ? AND is_active = 1
    ''', (user_id,)) as cursor:
        row = await cursor.fetchone()
        if row:
            return User(
                id=row['id'],
                email=row['email'],
                username=row['username'],
                hashed_password=row['hashed_password'],
                point_values=eval(row['point_values']),
                created_at=datetime.fromisoformat(row['created_at']),
                is_active=bool(row['is_active'])
            )
        return None

async def update_user_point_values(db: aiosqlite.Connection, user_id: str, point_values: dict) -> bool:
    """Update user's point values"""
    await db.execute('''
        UPDATE users 
        SET point_values = ?
        WHERE id = ?
    ''', (str(point_values), user_id))
    await db.commit()
    return True

async def check_email_exists(db: aiosqlite.Connection, email: str) -> bool:
    """Check if email already exists"""
    async with db.execute('''
        SELECT COUNT(*) as count FROM users WHERE email = ?
    ''', (email,)) as cursor:
        row = await cursor.fetchone()
        return row['count'] > 0

async def check_username_exists(db: aiosqlite.Connection, username: str) -> bool:
    """Check if username already exists"""
    async with db.execute('''
        SELECT COUNT(*) as count FROM users WHERE username = ?
    ''', (username,)) as cursor:
        row = await cursor.fetchone()
        return row['count'] > 0

async def store_tweet_engagement(db: aiosqlite.Connection, engagement: TweetEngagement) -> bool:
    """Store a single tweet engagement record"""
    try:
        await db.execute('''
            INSERT OR REPLACE INTO tweet_engagements 
            (id, tweet_id, user_id, tweet_text, like_count, retweet_count, reply_count, mention_count, 
             engagement_score, posted_date, fetched_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            engagement.id or str(uuid.uuid4()),
            engagement.tweet_id,
            engagement.user_id,
            engagement.tweet_text,
            engagement.like_count,
            engagement.retweet_count,
            engagement.reply_count,
            engagement.mention_count,
            engagement.engagement_score,
            engagement.posted_date.isoformat() if engagement.posted_date else None,
            engagement.fetched_at.isoformat()
        ))
        await db.commit()
        return True
    except Exception as e:
        print(f"Error storing engagement: {e}")
        return False

async def store_multiple_engagements(db: aiosqlite.Connection, engagements: List[TweetEngagement]) -> int:
    """Store multiple tweet engagement records"""
    stored_count = 0
    for engagement in engagements:
        if await store_tweet_engagement(db, engagement):
            stored_count += 1
    return stored_count

async def get_user_engagements(db: aiosqlite.Connection, user_id: str, limit: int = 100) -> List[TweetEngagement]:
    """Get engagement records for a specific user"""
    engagements = []
    async with db.execute('''
        SELECT * FROM tweet_engagements 
        WHERE user_id = ? 
        ORDER BY fetched_at DESC 
        LIMIT ?
    ''', (user_id, limit)) as cursor:
        async for row in cursor:
            engagement = TweetEngagement(
                id=row['id'],
                tweet_id=row['tweet_id'],
                user_id=row['user_id'],
                tweet_text=row['tweet_text'],
                like_count=row['like_count'],
                retweet_count=row['retweet_count'],
                reply_count=row['reply_count'],
                mention_count=row['mention_count'],
                engagement_score=row['engagement_score'],
                posted_date=datetime.fromisoformat(row['posted_date']) if row['posted_date'] else None,
                fetched_at=datetime.fromisoformat(row['fetched_at'])
            )
            engagements.append(engagement)
    return engagements

async def get_user_total_score(db: aiosqlite.Connection, user_id: str) -> int:
    """Get total engagement score for a user"""
    async with db.execute('''
        SELECT COALESCE(SUM(engagement_score), 0) as total_score 
        FROM tweet_engagements 
        WHERE user_id = ?
    ''', (user_id,)) as cursor:
        row = await cursor.fetchone()
        return row['total_score']

async def delete_user_engagements(db: aiosqlite.Connection, user_id: str) -> bool:
    """Delete all engagement records for a user (for cleanup)"""
    try:
        await db.execute('''
            DELETE FROM tweet_engagements WHERE user_id = ?
        ''', (user_id,))
        await db.commit()
        return True
    except Exception as e:
        print(f"Error deleting engagements: {e}")
        return False
