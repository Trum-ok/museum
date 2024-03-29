from pydantic import BaseModel, Field
from asyncpg import Pool


class InventoryNumber(BaseModel):
    number: int
    collection: str
    fund: str


class Exhibit(BaseModel):
    id: int
    name: str
    quantity: int = Field(default="")
    obtaining: str = Field(default="")
    discovery: str = Field(default="")
    description: str = Field(default="")
    assignment: str = Field(default="")
    inventory_number: InventoryNumber = None
    image: str = Field(default="")
    visible: bool = Field(default=True)


class ExhibitColumns:
    ID = "id"
    NAME = "name",
    QUANTITY = "quantity",
    OBTAINING = "obtaining",
    DISCOVERY = "discovery",
    DESCRIPTION = "description",
    ASSIGNMENT = "assignment",
    INVENTORY = ["number", "collection", "fund"],
    IMAGE = "image",
    VISIBLE = "visible"


class ExhibitsTable:
    """Exhibits Table"""

    def __init__(self, pool: Pool) -> None:
        self.pool = pool


    async def create(self) -> None:
        """Create the table"""
        await self.pool.execute(
            """
        CREATE TABLE IF NOT EXISTS exhibits (
            id SERIAL PRIMARY KEY,
            name TEXT,
            quantity INT,
            obtaining TEXT,
            discovery TEXT,
            description TEXT,
            assignment TEXT,
            number INT,
            collection TEXT,
            fund TEXT,
            image TEXT,
            visible BOOL NOT NULL DEFAULT TRUE
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
            INSERT INTO exhibits (name, quantity, obtaining, discovery, description, assignment, number, collection, fund, image, visible)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
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
            exhibit.image,
            exhibit.visible
        )
    

    async def get(self, name: str, columns: list) -> list:
        exhibit = await self.pool.fetchval(
            "SELECT " 
            + ", ".join(column for column in columns)
            + " FROM exhibits"
            + " WHERE name = $1",
            name
        )
        return exhibit


    async def update(self, id: int, **kwargs) -> None:
        await self.pool.execute(
            "UPDATE exhibits SET "
            + ", ".join(f"{key} = ${i}" for i, key in enumerate(kwargs, 2))
            + " WHERE id = $1",
            id,
            *kwargs.values(),
        )
    

    async def delete(self, id: int) -> None:
        """Delete an exhibit from exhibits table by id"""
        await self.pool.execute(
            """
            DELETE FROM exhibits WHERE id = $1
            """,
            id
        )
