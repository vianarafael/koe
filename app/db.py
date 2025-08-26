import aiosqlite
import uuid
from datetime import datetime, timezone
from app.models import User, UserCreate

async def get_db():
    """Get database connection"""
    db = await aiosqlite.connect('engagemeter.db')
    db.row_factory = aiosqlite.Row
    return db

async def init_db():
    """Initialize database with required tables"""
    db = await get_db()
    
    # Create users table
    await db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            username TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            created_at TEXT NOT NULL,
            is_active BOOLEAN NOT NULL DEFAULT 1
        )
    ''')
    
    await db.commit()
    print("Database initialized successfully")

async def create_user(db: aiosqlite.Connection, user_data: UserCreate, hashed_password: str) -> User:
    """Create a new user account"""
    user_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    
    await db.execute('''
        INSERT INTO users (id, email, username, hashed_password, created_at, is_active)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, user_data.email, user_data.username, hashed_password, now, True))
    
    await db.commit()
    
    return User(
        id=user_id,
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,
        created_at=datetime.fromisoformat(now),
        is_active=True
    )

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
                created_at=datetime.fromisoformat(row['created_at']),
                is_active=bool(row['is_active'])
            )
        return None

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










