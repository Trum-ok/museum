from pydantic import BaseModel, Field
from asyncpg import Pool
from datetime import datetime

class EventType:
    ADD = "Add"
    EDIT = "Edit"
    DELETE = "Delete"
    RESTORE = "Restore"
    HIDE = "Hide"
    UNHIDE = "Unhide"
    C_EDIT = "Edit (contacts)"
    M_EDIT = "Edit (main)"
    

class Event(BaseModel):
    type_: str
    was: str = Field(default="")
    now: str = Field(default="")
    date: datetime = Field(default_factory=datetime.now)
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
            type_ TEXT,
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

        if not events:
            return []

        return [
            Event(
                type_=e['type_'],
                was=e['was'] if e['was'] is not None else "",
                now=e['now'] if e['now'] is not None else "",
                date=e['date'],
                admin=e['admin']
            )
            for e in events
        ]



    async def insert(self, event: Event) -> None:
        """Insert a new event"""
        await self.pool.execute(
            """
            INSERT INTO events (type_, was, now, date, admin)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT DO NOTHING
            """,
            event.type_,
            event.was,
            event.now,
            event.date,
            event.admin
        )
