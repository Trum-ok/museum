import asyncpg
import db.tables as tables


class Database:
    """Database"""

    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

        self.settings = tables.AdminSettingsTable(pool)
        """Admin settings"""
        self.items = tables.ExhibitsTable(pool)
        """Exhibits"""
        self.admins= tables.AdminsTable(pool, self.settings)
        """Admin"""


    async def create(self) -> None:
        """
        Create database tables.
        """
        await self.items.create()
        await self.settings.create()
        await self.admins.create()
