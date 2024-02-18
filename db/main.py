import asyncpg
import db.tables as tables


class Database:
    """Database"""

    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

        self.items = tables.ExhibitsTable(pool)
        """Exhibits"""
        self.admins= tables.AdminsTable(pool)
        """Admin"""


    async def create(self) -> None:
        """
        Create database tables.
        """
        await self.items.create()
        await self.admins.create()
