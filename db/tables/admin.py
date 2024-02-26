from pydantic import BaseModel, Field
from asyncpg import Pool
from typing import Optional

from dev.exceptions import AdminNotFound
from .admin_settings import AdminSettings, AdminSettingsTable


class Admin(BaseModel):
    login: str = Field(default="")
    password: str = Field(default="")
    cookie: str = Field(default="")

    settings_db: AdminSettingsTable
    """Admin settings database"""

    internal_settings: Optional[AdminSettings]
    """User settings"""

    class Config:
        arbitrary_types_allowed = True
        

class AdminsTable:
    """Admins Table"""

    def __init__(self, pool: Pool, settings_db: AdminSettingsTable) -> None:
        self.pool = pool
        self.settings_db = settings_db


    async def create(self) -> None:
        """Create the table"""
        await self.pool.execute(
            """
        CREATE TABLE IF NOT EXISTS admins (
            login TEXT,
            password TEXT,
            cookie TEXT
        )
        """
        )


    async def get_all(self) -> list[Admin]:
        """Get all admins"""
        admins = await self.pool.fetch(
            """
            SELECT * FROM admins
            """
        )
        return [Admin(**admin) for admin in admins]
    

    async def insert(self, login: str = None, password: str = None, cookie: str = None) -> None:  # noqa: E501
        """Insert a new admin user"""
        await self.pool.execute(
            """
            INSERT INTO admins (login, password,cookie)
            VALUES ($1, $2, $3)
            ON CONFLICT DO NOTHING
            """,
            login,
            password,
            cookie
        )
    
    
    async def delete(self, login: str) -> None:
        """Delete admin user"""
        result = await self.pool.execute(
            """
            DELETE FROM admins WHERE login = $1
            RETURNING login
            """,
            login,
        )

        if not result:
            raise AdminNotFound(login)
        

    async def check_lp(self, login: str, password: str) -> bool:
        """Verifies correctness by login and password"""
        return await self.pool.fetchval(
            """
            SELECT EXISTS(SELECT 1 FROM admins WHERE login = $1 and password = $2)
            """,
            login,
            password,
        )

    async def check_cookie(self, cookie: str) -> bool:
        """Verifies correctness by cookie"""
        return await self.pool.fetchval(
            """
            SELECT EXISTS(SELECT 1 FROM admins WHERE cookie = $1)
            """,
            cookie,
        )
    

    async def update(self, login: str, password: str = None, cookie: str = None) -> None:  # noqa: E501
        ...
