import aiosqlite
import uuid
from datetime import datetime, timedelta
from typing import List, Optional
from app.settings import settings
from app.models import User, UserCreate, UserResponse, TweetEngagement, CSVUpload

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
        
        await db.execute('''
            CREATE TABLE IF NOT EXISTS csv_uploads (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                filename TEXT NOT NULL,
                content BLOB NOT NULL,
                content_type TEXT NOT NULL DEFAULT 'text/csv',
                file_size INTEGER NOT NULL,
                uploaded_at TEXT NOT NULL,
                records_processed INTEGER NOT NULL DEFAULT 0,
                records_stored INTEGER NOT NULL DEFAULT 0,
                parse_errors TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
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

async def store_csv_upload(db: aiosqlite.Connection, csv_upload) -> str:
    """Store CSV file in database"""
    csv_upload.id = str(uuid.uuid4())
    
    await db.execute('''
        INSERT INTO csv_uploads (id, user_id, filename, content, content_type, file_size, uploaded_at, records_processed, records_stored, parse_errors)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        csv_upload.id, csv_upload.user_id, csv_upload.filename, csv_upload.content,
        csv_upload.content_type, csv_upload.file_size, csv_upload.uploaded_at.isoformat(),
        csv_upload.records_processed, csv_upload.records_stored, str(csv_upload.parse_errors)
    ))
    await db.commit()
    return csv_upload.id

async def get_csv_upload(db: aiosqlite.Connection, upload_id: str, user_id: str):
    """Get CSV upload by ID for a specific user"""
    async with db.execute('''
        SELECT * FROM csv_uploads WHERE id = ? AND user_id = ?
    ''', (upload_id, user_id)) as cursor:
        row = await cursor.fetchone()
        if row:
            from app.models import CSVUpload
            return CSVUpload(
                id=row['id'],
                user_id=row['user_id'],
                filename=row['filename'],
                content=row['content'],
                content_type=row['content_type'],
                file_size=row['file_size'],
                uploaded_at=datetime.fromisoformat(row['uploaded_at']),
                records_processed=row['records_processed'],
                records_stored=row['records_stored'],
                parse_errors=eval(row['parse_errors']) if row['parse_errors'] else []
            )
        return None

async def get_user_csv_uploads(db: aiosqlite.Connection, user_id: str, limit: int = 50) -> List[CSVUpload]:
    """Get list of CSV uploads for a user"""
    from app.models import CSVUpload
    uploads = []
    
    async with db.execute('''
        SELECT * FROM csv_uploads WHERE user_id = ? ORDER BY uploaded_at DESC LIMIT ?
    ''', (user_id, limit)) as cursor:
        async for row in cursor:
            uploads.append(CSVUpload(
                id=row['id'],
                user_id=row['user_id'],
                filename=row['filename'],
                content=row['content'],
                content_type=row['content_type'],
                file_size=row['file_size'],
                uploaded_at=datetime.fromisoformat(row['uploaded_at']),
                records_processed=row['records_processed'],
                records_stored=row['records_stored'],
                parse_errors=eval(row['parse_errors']) if row['parse_errors'] else []
            ))
    
    return uploads

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

async def update_engagement_score(db: aiosqlite.Connection, engagement_id: str, new_score: int) -> bool:
    """Update the engagement score for a specific engagement"""
    try:
        await db.execute('''
            UPDATE tweet_engagements 
            SET engagement_score = ?
            WHERE id = ?
        ''', (new_score, engagement_id))
        await db.commit()
        return True
    except Exception as e:
        print(f"Error updating engagement score: {e}")
        return False

async def get_engagements_by_score_range(
    db: aiosqlite.Connection, 
    user_id: str, 
    min_score: int = 0, 
    max_score: int = None,
    limit: int = 100
) -> List[TweetEngagement]:
    """Get engagements within a specific score range"""
    engagements = []
    
    if max_score is None:
        query = '''
            SELECT * FROM tweet_engagements 
            WHERE user_id = ? AND engagement_score >= ?
            ORDER BY engagement_score DESC 
            LIMIT ?
        '''
        params = (user_id, min_score, limit)
    else:
        query = '''
            SELECT * FROM tweet_engagements 
            WHERE user_id = ? AND engagement_score BETWEEN ? AND ?
            ORDER BY engagement_score DESC 
            LIMIT ?
        '''
        params = (user_id, min_score, max_score, limit)
    
    async with db.execute(query, params) as cursor:
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

async def get_top_engagements(db: aiosqlite.Connection, user_id: str, limit: int = 10) -> List[TweetEngagement]:
    """Get top performing engagements by score"""
    return await get_engagements_by_score_range(db, user_id, min_score=0, limit=limit)

async def get_user_engagement_breakdown(db: aiosqlite.Connection, user_id: str) -> dict:
    """Get breakdown of engagement counts and points by type for a user"""
    async with db.execute('''
        SELECT 
            COALESCE(SUM(like_count), 0) as total_likes,
            COALESCE(SUM(retweet_count), 0) as total_retweets,
            COALESCE(SUM(reply_count), 0) as total_replies,
            COALESCE(SUM(mention_count), 0) as total_mentions
        FROM tweet_engagements 
        WHERE user_id = ?
    ''', (user_id,)) as cursor:
        row = await cursor.fetchone()
        return {
            'likes': row['total_likes'],
            'retweets': row['total_retweets'],
            'replies': row['total_replies'],
            'mentions': row['total_mentions']
        }










