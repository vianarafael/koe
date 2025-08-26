#!/usr/bin/env python3
"""
Database migration script for EngageMeter.co MVP
This script will create the new database schema with sites, tracked_links, and events tables.
"""

import asyncio
import aiosqlite
import os
from datetime import datetime, timezone

async def migrate_database():
    """Migrate database to new MVP schema"""
    
    # Database file path
    db_path = 'engagemeter.db'
    
    # Check if database exists
    if os.path.exists(db_path):
        print(f"Database {db_path} exists. Backing up...")
        backup_path = f"{db_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.rename(db_path, backup_path)
        print(f"Backup created: {backup_path}")
    
    print("Creating new database with MVP schema...")
    
    # Create new database
    async with aiosqlite.connect(db_path) as db:
        # Create users table
        await db.execute('''
            CREATE TABLE users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                username TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL,
                created_at TEXT NOT NULL,
                is_active BOOLEAN NOT NULL DEFAULT 1
            )
        ''')
        print("✓ Users table created")
        
        # Create sites table
        await db.execute('''
            CREATE TABLE sites (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                domain TEXT NOT NULL,
                created_at TEXT NOT NULL,
                is_active BOOLEAN NOT NULL DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        print("✓ Sites table created")
        
        # Create tracked_links table
        await db.execute('''
            CREATE TABLE tracked_links (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                site_id TEXT NOT NULL,
                original_url TEXT NOT NULL,
                source TEXT NOT NULL CHECK (source IN ('x', 'reddit', 'linkedin', 'other')),
                short_code TEXT UNIQUE NOT NULL,
                utm_source TEXT NOT NULL,
                utm_medium TEXT NOT NULL DEFAULT 'social',
                utm_campaign TEXT NOT NULL DEFAULT 'link_tracking',
                created_at TEXT NOT NULL,
                is_active BOOLEAN NOT NULL DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (site_id) REFERENCES sites (id)
            )
        ''')
        print("✓ Tracked links table created")
        
        # Create events table
        await db.execute('''
            CREATE TABLE events (
                id TEXT PRIMARY KEY,
                tracked_link_id TEXT,
                site_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                kind TEXT NOT NULL CHECK (kind IN ('click', 'pageview')),
                ts TEXT NOT NULL,
                ip_hash TEXT,
                ua_hash TEXT,
                referer TEXT,
                utm_source TEXT,
                utm_medium TEXT,
                utm_campaign TEXT,
                country TEXT,
                path TEXT,
                session_id TEXT,
                FOREIGN KEY (tracked_link_id) REFERENCES tracked_links (id),
                FOREIGN KEY (site_id) REFERENCES sites (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        print("✓ Events table created")
        
        # Create indexes
        await db.execute('CREATE INDEX idx_sites_user_id ON sites(user_id)')
        await db.execute('CREATE INDEX idx_tracked_links_user_id ON tracked_links(user_id)')
        await db.execute('CREATE INDEX idx_tracked_links_site_id ON tracked_links(site_id)')
        await db.execute('CREATE INDEX idx_tracked_links_short_code ON tracked_links(short_code)')
        await db.execute('CREATE INDEX idx_events_ts ON events(ts)')
        await db.execute('CREATE INDEX idx_events_site_id ON events(site_id)')
        await db.execute('CREATE INDEX idx_events_tracked_link_id ON events(tracked_link_id)')
        await db.execute('CREATE INDEX idx_events_session_id ON events(session_id)')
        print("✓ Indexes created")
        
        # Commit all changes
        await db.commit()
        
        print("\n🎉 Database migration completed successfully!")
        print(f"New database created: {db_path}")
        
        # Show table structure
        print("\n📊 Database Schema:")
        async with db.execute("SELECT name FROM sqlite_master WHERE type='table'") as cursor:
            async for row in cursor:
                print(f"  - {row[0]}")
        
        # Show indexes
        print("\n🔍 Indexes:")
        async with db.execute("SELECT name FROM sqlite_master WHERE type='index'") as cursor:
            async for row in cursor:
                print(f"  - {row[0]}")

if __name__ == "__main__":
    print("🚀 EngageMeter.co Database Migration")
    print("=" * 40)
    
    try:
        asyncio.run(migrate_database())
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        exit(1)
