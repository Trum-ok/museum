from pydantic import BaseModel, Field
from asyncpg import Pool


class InventoryNumber(BaseModel):
    number: int
    collection: str
    fund: str


class Exhibit(BaseModel):
    name: str
    quantity: int = Field(default="")
    obtaining: str = Field(default="")
    discovery: str = Field(default="")
    description: str = Field(default="")
    assignment: str = Field(default="")
    inventory_number: InventoryNumber = None
    image: str = Field(default="")


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
        return [
            Exhibit(
                **{
                    key: value if value is not None else ""
                    for key, value in item.items()
                },
                inventory_number=InventoryNumber(
                    number=item["number"],
                    collection=item["collection"],
                    fund=item["fund"]
                ) if all(item.get(key) for key in ("number", "collection", "fund")) else None
            )
            for item in exhibits
        ]


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
            exhibit.inventory_number.number if exhibit.inventory_number else None,
            exhibit.inventory_number.collection if exhibit.inventory_number else None,
            exhibit.inventory_number.fund if exhibit.inventory_number else None,
            exhibit.image
        )
