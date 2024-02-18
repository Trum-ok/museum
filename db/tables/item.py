import asyncio
from asyncpg import Pool, create_pool


class InventoryNumber:
    number: int = None
    collection: str = None
    fund: str = None


class Exhibit:
    name: str
    quantity: int = None
    obtaining: str = None
    discovery: str = None
    description: str = None
    assignment: str = None
    inventory_number: InventoryNumber
    image: str


class ExhibitsTable:
    """Exhibits Table"""

    def __init__(self, pool: Pool) -> None:
        self.pool = pool


    async def create(self) -> None:
        """Create the table"""
        await self.pool.execute(
            """
        CREATE TABLE IF NOT EXISTS exhibits (
            name TEXT,
            quantity INT,
            obtaining TEXT,
            discovery TEXT,
            description TEXT,
            assignment TEXT,
            number INT,
            collection TEXT,
            fund TEXT,
            image TEXT
        )
        """
        )


    async def get_all(self) -> list[Exhibit]:
        """Get all exhibits"""
        exhibits = await self.pool.fetch(
            """
            SELECT * FROM exhibits
            """
        )
        return exhibits
    

    async def insert(self, exhibit: Exhibit) -> None:
        """Insert a new exhibit"""
        await self.pool.execute(
            """
            INSERT INTO exhibits (name, quantity, obtaining, discovery, description, assignment, number, collection, fund, image)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
            ON CONFLICT DO NOTHING
            """,
            exhibit.name,
            exhibit.quantity,
            exhibit.obtaining,
            exhibit.discovery,
            exhibit.description,
            exhibit.assignment,
            exhibit.inventory_number.number,
            exhibit.inventory_number.collection,
            exhibit.inventory_number.fund,
            exhibit.image
        )
