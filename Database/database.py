import aiosqlite

db = None

async def init():
    global db
    db = await aiosqlite.connect("userdata.db")
    await db.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            user_name TEXT DEFAULT 'Нет',
            user_age INTEGER DEFAULT 0,
            user_description TEXT DEFAULT 'Нет',
            join_value INTEGER DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS user_stats (
            user_id INTEGER NOT NULL,
            user_level INTEGER DEFAULT 1,
            user_level_role INTEGER DEFAULT 1476451132560773161,
            user_exp INTEGER DEFAULT 0,
            user_stars INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS user_bio (
            user_id INTEGER NOT NULL,
            user_langs TEXT DEFAULT 'Нет',
            user_tech TEXT DEFAULT 'Нет',
            user_experience INTEGER DEFAULT 0,
            user_status TEXT DEFAULT 'Нет',
            user_github TEXT DEFAULT 'Не указано',
            user_gitlab TEXT DEFAULT 'Не указано',
            user_achievements TEXT DEFAULT 'Нет',
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS threads (
            thread_id INTEGER PRIMARY KEY,
            owner_id INTEGER NOT NULL,
            message_id INTEGER NOT NULL,
            channel_id INTEGER NOT NULL
        );
        CREATE INDEX IF NOT EXISTS index_user_id ON users(user_id);
        CREATE INDEX IF NOT EXISTS index_user_stats_id ON user_stats(user_id);
        CREATE INDEX IF NOT EXISTS index_user_bio_id ON user_bio(user_id);
        """
    )
    await db.commit()
