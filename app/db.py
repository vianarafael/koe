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
    
    # Create tracked_links table
    await db.execute('''
        CREATE TABLE IF NOT EXISTS tracked_links (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            original_url TEXT NOT NULL,
            short_code TEXT UNIQUE NOT NULL,
            source TEXT NOT NULL,
            utm_source TEXT NOT NULL,
            utm_medium TEXT NOT NULL DEFAULT 'social',
            utm_campaign TEXT NOT NULL DEFAULT 'link_tracking',
            created_at TEXT NOT NULL,
            is_active BOOLEAN NOT NULL DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create click_events table
    await db.execute('''
        CREATE TABLE IF NOT EXISTS click_events (
            id TEXT PRIMARY KEY,
            link_id TEXT NOT NULL,
            user_agent TEXT,
            referrer TEXT,
            ip_address TEXT,
            clicked_at TEXT NOT NULL,
            FOREIGN KEY (link_id) REFERENCES tracked_links (id)
        )
    ''')
    
    # Create indexes
    await db.execute('CREATE INDEX IF NOT EXISTS idx_tracked_links_user_id ON tracked_links(user_id)')
    await db.execute('CREATE INDEX IF NOT EXISTS idx_tracked_links_short_code ON tracked_links(short_code)')
    await db.execute('CREATE INDEX IF NOT EXISTS idx_click_events_link_id ON click_events(link_id)')
    await db.execute('CREATE INDEX IF NOT EXISTS idx_click_events_clicked_at ON click_events(clicked_at)')
    
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

# Site Management Operations
async def create_site(db: aiosqlite.Connection, user_id: str, domain: str):
    """Create a new site for a user"""
    from app.models import Site
    
    site_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    
    await db.execute('''
        INSERT INTO sites (id, user_id, domain, created_at, is_active)
        VALUES (?, ?, ?, ?, ?)
    ''', (site_id, user_id, domain, now, True))
    
    await db.commit()
    
    return Site(
        id=site_id,
        user_id=user_id,
        domain=domain,
        created_at=datetime.fromisoformat(now),
        is_active=True
    )

async def get_user_sites(db: aiosqlite.Connection, user_id: str):
    """Get all sites for a user"""
    from app.models import Site
    
    sites = []
    async with db.execute('''
        SELECT * FROM sites WHERE user_id = ? AND is_active = 1 ORDER BY created_at DESC
    ''', (user_id,)) as cursor:
        async for row in cursor:
            sites.append(Site(
                id=row['id'],
                user_id=row['user_id'],
                domain=row['domain'],
                created_at=datetime.fromisoformat(row['created_at']),
                is_active=bool(row['is_active'])
            ))
    return sites

async def get_site_by_id(db: aiosqlite.Connection, site_id: str, user_id: str):
    """Get a specific site by ID (user must own it)"""
    from app.models import Site
    
    async with db.execute('''
        SELECT * FROM sites WHERE id = ? AND user_id = ? AND is_active = 1
    ''', (site_id, user_id)) as cursor:
        row = await cursor.fetchone()
        if row:
            return Site(
                id=row['id'],
                user_id=row['user_id'],
                domain=row['domain'],
                created_at=datetime.fromisoformat(row['created_at']),
                is_active=bool(row['is_active'])
            )
        return None

async def update_site(db: aiosqlite.Connection, site_id: str, user_id: str, domain: str):
    """Update a site's domain"""
    from app.models import Site
    
    await db.execute('''
        UPDATE sites SET domain = ? WHERE id = ? AND user_id = ? AND is_active = 1
    ''', (domain, site_id, user_id))
    
    if db.total_changes > 0:
        await db.commit()
        return await get_site_by_id(db, site_id, user_id)
    return None

async def delete_site(db: aiosqlite.Connection, site_id: str, user_id: str) -> bool:
    """Soft delete a site (set is_active = 0)"""
    await db.execute('''
        UPDATE sites SET is_active = 0 WHERE id = ? AND user_id = ? AND is_active = 1
    ''', (site_id, user_id))
    
    if db.total_changes > 0:
        await db.commit()
        return True
    return False

# Link Tracking Operations
async def create_tracked_link(db: aiosqlite.Connection, user_id: str, site_id: str, 
                            original_url: str, source: str, short_code: str, 
                            utm_source: str, utm_medium: str = "social", 
                            utm_campaign: str = "link_tracking"):
    """Create a new tracked link"""
    from app.models import TrackedLink
    
    link_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    
    await db.execute('''
        INSERT INTO tracked_links (id, user_id, site_id, original_url, source, short_code, 
                                 utm_source, utm_medium, utm_campaign, created_at, is_active)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (link_id, user_id, site_id, original_url, source, short_code, 
          utm_source, utm_medium, utm_campaign, now, True))
    
    await db.commit()
    
    return TrackedLink(
        id=link_id,
        user_id=user_id,
        site_id=site_id,
        original_url=original_url,
        source=source,
        short_code=short_code,
        utm_source=utm_source,
        utm_medium=utm_medium,
        utm_campaign=utm_campaign,
        created_at=datetime.fromisoformat(now),
        is_active=True
    )

async def get_tracked_link_by_short_code(db: aiosqlite.Connection, short_code: str):
    """Get a tracked link by its short code"""
    from app.models import TrackedLink
    
    async with db.execute('''
        SELECT * FROM tracked_links WHERE short_code = ? AND is_active = 1
    ''', (short_code,)) as cursor:
        row = await cursor.fetchone()
        if row:
            return TrackedLink(
                id=row['id'],
                user_id=row['user_id'],
                site_id=row['site_id'],
                original_url=row['original_url'],
                source=row['source'],
                short_code=row['short_code'],
                utm_source=row['utm_source'],
                utm_medium=row['utm_medium'],
                utm_campaign=row['utm_campaign'],
                created_at=datetime.fromisoformat(row['created_at']),
                is_active=bool(row['is_active'])
            )
        return None

async def get_user_tracked_links(db: aiosqlite.Connection, user_id: str, site_id=None):
    """Get all tracked links for a user (optionally filtered by site)"""
    from app.models import TrackedLink
    
    links = []
    query = '''
        SELECT * FROM tracked_links WHERE user_id = ? AND is_active = 1
    '''
    params = [user_id]
    
    if site_id:
        query += ' AND site_id = ?'
        params.append(site_id)
    
    query += ' ORDER BY created_at DESC'
    
    async with db.execute(query, params) as cursor:
        async for row in cursor:
            links.append(TrackedLink(
                id=row['id'],
                user_id=row['user_id'],
                site_id=row['site_id'],
                original_url=row['original_url'],
                source=row['source'],
                short_code=row['short_code'],
                utm_source=row['utm_source'],
                utm_medium=row['utm_medium'],
                utm_campaign=row['utm_campaign'],
                created_at=datetime.fromisoformat(row['created_at']),
                is_active=bool(row['is_active'])
            ))
    return links

async def delete_tracked_link(db: aiosqlite.Connection, link_id: str, user_id: str) -> bool:
    """Soft delete a tracked link (set is_active = 0)"""
    await db.execute('''
        UPDATE tracked_links SET is_active = 0 WHERE id = ? AND user_id = ? AND is_active = 1
    ''', (link_id, user_id))
    
    if db.total_changes > 0:
        await db.commit()
        return True
    return False

# Event Tracking Operations
async def create_event(db: aiosqlite.Connection, event_data: dict) -> str:
    """Create a new event record"""
    event_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    
    await db.execute('''
        INSERT INTO events (id, tracked_link_id, site_id, user_id, kind, ts, ip_hash, ua_hash,
                          referer, utm_source, utm_medium, utm_campaign, country, path, session_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (event_id, event_data.get('tracked_link_id'), event_data['site_id'], event_data['user_id'],
          event_data['kind'], now, event_data.get('ip_hash'), event_data.get('ua_hash'),
          event_data.get('referer'), event_data.get('utm_source'), event_data.get('utm_medium'),
          event_data.get('utm_campaign'), event_data.get('country'), event_data.get('path'),
          event_data.get('session_id')))
    
    await db.commit()
    return event_id

async def get_24h_traffic_by_source(db: aiosqlite.Connection, site_id: str):
    """Get 24-hour traffic data by source for a site"""
    async with db.execute('''
        SELECT 
            strftime('%H', ts) as hour,
            COALESCE(utm_source, 
                CASE 
                    WHEN referer LIKE '%twitter.com%' OR referer LIKE '%t.co%' THEN 'x'
                    WHEN referer LIKE '%linkedin.com%' THEN 'linkedin'
                    WHEN referer LIKE '%reddit.com%' THEN 'reddit'
                    ELSE 'other'
                END
            ) as source,
            COUNT(*) as visits
        FROM events 
        WHERE site_id = ? 
            AND ts >= datetime('now', '-24 hours')
            AND kind = 'pageview'
        GROUP BY hour, source
        ORDER BY hour, source
    ''', (site_id,)) as cursor:
        results = []
        async for row in cursor:
            results.append({
                'hour': row['hour'],
                'source': row['source'],
                'visits': row['visits']
            })
        return results

async def get_24h_clicks_by_link(db: aiosqlite.Connection, site_id: str):
    """Get 24-hour click data by tracked link for a site"""
    async with db.execute('''
        SELECT 
            tl.original_url,
            tl.source,
            COUNT(e.id) as clicks_24h
        FROM tracked_links tl
        LEFT JOIN events e ON tl.id = e.tracked_link_id 
            AND e.kind = 'click' 
            AND e.ts >= datetime('now', '-24 hours')
        WHERE tl.site_id = ? AND tl.is_active = 1
        GROUP BY tl.id, tl.original_url, tl.source
        ORDER BY clicks_24h DESC
    ''', (site_id,)) as cursor:
        results = []
        async for row in cursor:
            results.append({
                'original_url': row['original_url'],
                'source': row['source'],
                'clicks_24h': row['clicks_24h']
            })
        return results










