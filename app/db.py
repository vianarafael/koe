import aiosqlite
import uuid
from datetime import datetime, timedelta
from app.settings import settings
from app.models import User, UserCreate, UserResponse

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
                tweet_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                like_count INTEGER NOT NULL,
                retweet_count INTEGER NOT NULL,
                reply_count INTEGER NOT NULL,
                mention_count INTEGER NOT NULL,
                engagement_score INTEGER NOT NULL,
                fetched_at TEXT NOT NULL,
                PRIMARY KEY (tweet_id, user_id)
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
