import typing
from enum import Enum

from asyncpg import Pool
from pydantic import BaseModel, Field


class Settings(Enum):
    CAN_ADD = "add"
    CAN_EDIT = "edit"
    CAN_DELETE = "delete"


class AdminSettings(BaseModel):
    """Admin settings"""

    login: str
    """Admin login"""
    add: bool = Field(default=True)
    """Can add?"""
    edit: bool = Field(default=True)
    """Can edit?"""
    delete: bool = Field(default=True)
    """Can delete?"""


class AdminSettingsTable:
    def __init__(self, pool: Pool):
        self.pool = pool

    async def insert(
            self,         
            login: str,
            add: bool = True,
            edit: bool = True,
            delete: bool =  True
            ) -> None:
        """Insert admin settings"""
        await self.pool.execute(
            """
            INSERT INTO settings (login, add, edit, delete) 
            VALUES ($1, $2, $3, $4) 
            ON CONFLICT DO NOTHING""",
            login,
            add,
            edit,
            delete
        )

    async def update(self, login: int, settings: Settings, value: typing.Any) -> None:
        """Update admin settings"""
        await self.pool.execute(
            f"UPDATE settings SET {settings.value} = $1 WHERE login = $2",
            value,
            login,
        )

    async def get(self, login: int, settings: Settings) -> typing.Any:
        """Get admin settings"""
        val = await self.pool.fetchval(
            f"SELECT {settings.value} FROM settings WHERE login = $1", 
            login
        )
        if val is None:
            await self.insert(login)
            return await self.get(login, settings)

        return val

    async def get_all(self, login: int) -> AdminSettings:
        """Get all admin settings"""
        settings = await self.pool.fetchrow(
            "SELECT * FROM settings WHERE login = $1", 
            login
        )
        if settings is None:
            await self.insert(login)
            return await self.get_all(login)
        return AdminSettings(**settings)
    
    async def create(self) -> None:
        """Create the table"""
        await self.pool.execute(
            """
            CREATE TABLE IF NOT EXISTS settings (
                login TEXT,
                add BOOL DEFAULT TRUE,
                edit BOOL DEFAULT TRUE,
                delete BOOL DEFAULT TRUE
            )
            """
        )

    async def check_admin_exist(self, login: int) -> bool:
        """Check is admin exists and insert if not"""
        async with self.pool.acquire() as connection:
            query = "SELECT COUNT(*) FROM settings WHERE login = $1"
            result = await connection.fetchval(query, login)

            if not result:
                await self.insert(login)
            
            return True
        
    async def delete(self, login: int) -> None:
        """Delete an account"""
        await self.pool.execute(
            """
            DELETE FROM settings WHERE login = $1
            """,
            login,
        )
