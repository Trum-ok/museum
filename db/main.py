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
        """Admins"""
        self.events = tables.EventsTable(self.pool)
        """Events"""
        self.deleted = tables.DeletedExhibitsTable(self.pool)
        """Recently removed exhibits"""


    async def create(self) -> None:
        """
        Create database tables.
        """
        await self.items.create()
        await self.settings.create()
        await self.admins.create()
        await self.events.create()
        await self.deleted.create()


class Contacts:
    """Contacts and work time"""

    def __init__(self) -> None:
        self.contacts = tables.ContactsTable()


    def create(self) -> None:
        """
        Create contacts file.
        """
        self.contacts.create()
