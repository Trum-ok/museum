from pydantic import BaseModel, Field
from asyncpg import Pool
from datetime import datetime

class EventType:
    ADD = "Add"
    EDIT = "Edit"
    DELETE = "Delete"
    HIDE = "Hide"
    UNHIDE = "Unhide"
    RESTORE = "Restore"


class Event(BaseModel):
    type_: str
    was: str = Field(default="")
    now: str = Field(default="")
    date: datetime
    admin: str


class EventsTable:
    """Events Table"""

    def __init__(self, pool: Pool) -> None:
        self.pool = pool


    async def create(self) -> None:
        """Create the table"""
        await self.pool.execute(
            """
        CREATE TABLE IF NOT EXISTS events (
            type TEXT,
            was TEXT,
            now TEXT,
            date TIMESTAMP,
            admin TEXT
        )
        """
        )
    

    async def get_all(self) -> list[Event]:
        """Get all events"""
        events = await self.pool.fetch(
            """
            SELECT * FROM events
            """
        )
        return [
            Event(
                **{
                    key: value if value is not None else ""
                    for key, value in e.items()
                }
            )
            for e in events
        ]


    async def insert(self, event: Event) -> None:
        """Insert a new event"""
        await self.pool.execute(
            """
            INSERT INTO events (type, was, now, date, admin)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT DO NOTHING
            """,
            event.type_,
            event.was,
            event.now,
            event.date,
            event.admin
        )
