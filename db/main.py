import asyncpg
import db.tables as tables


class Database:
    """Database"""

    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

        self.settings = tables.AdminSettingsTable(self.pool)
        """Admin settings"""
        self.items = tables.ExhibitsTable(self.pool)
        """Exhibits"""
        self.admins= tables.AdminsTable(self.pool, self.settings)
        """Admin"""
        self.events = tables.EventsTable(self.pool)
        """Events"""


    async def create(self) -> None:
        """
        Create database tables.
        """
        await self.items.create()
        await self.settings.create()
        await self.admins.create()
        await self.events.create()
