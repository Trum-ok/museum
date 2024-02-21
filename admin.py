import os
import asyncio
import asyncpg
from dotenv import load_dotenv
from db.main import Database
from db.tables.admin import Admin

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


async def main() -> asyncpg.Pool:
    """Database connection"""
    try:
        pool = await asyncpg.create_pool(DATABASE_URL)
    except Exception as e:
        # logging.warning("Failed to connect to database", exc_info=e)
        return
    if not pool:
        raise AssertionError
    return pool


async def setup_db():
    """Database setup"""
    # try:
    pool = await main()
    db = Database(pool)
    await db.create()
    # except Exception as e:
    #     # logging.warning(exc_info=e)
    #     return


async def add_admin(login: str, password: str):
    pool = await main()
    db = Database(pool)

    await db.admins.insert(login, password)


if __name__ == '__main__':    
    asyncio.run(setup_db())
    asyncio.run(add_admin("Sonata", "Sonata"))


    import secrets

    # Генерируем секретный ключ длиной 64 байта
    secret_key = secrets.token_urlsafe(64)

    print(secret_key)
