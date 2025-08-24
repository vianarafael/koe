import asyncio
import aiosqlite

async def migrate():
    async with aiosqlite.connect("app.db") as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                twitter_id TEXT NOT NULL,
                twitter_username TEXT NOT NULL,
                access_token TEXT NOT NULL,
                refresh_token TEXT,
                point_like INTEGER DEFAULT 1,
                point_retweet INTEGER DEFAULT 2,
                point_reply INTEGER DEFAULT 3,
                point_mention INTEGER DEFAULT 1
            );
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS tweet_engagements (
                tweet_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                like_count INTEGER NOT NULL,
                retweet_count INTEGER NOT NULL,
                reply_count INTEGER NOT NULL,
                mention_count INTEGER NOT NULL,
                engagement_score INTEGER NOT NULL,
                fetched_at TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
        ''')
        await db.commit()

if __name__ == "__main__":
    asyncio.run(migrate())
