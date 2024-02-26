from asyncpg import Pool

from db.tables.item import Exhibit, InventoryNumber


class DeletedExhibitsTable:
    """Deleted Exhibits Table"""

    def __init__(self, pool: Pool) -> None:
        self.pool = pool


    async def create(self) -> None:
        """Create the table"""
        await self.pool.execute(
            """
        CREATE TABLE IF NOT EXISTS deleted_exhibits (
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
            visible BOOL
        )
        """
        )


    async def get_all(self) -> list[Exhibit]:
        """Get all deleted exhibits"""
        exhibits = await self.pool.fetch(
            """
            SELECT * FROM deleted_exhibits
            """
        )

        if not exhibits:
            return []

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
        """Insert a deleted exhibits"""
        await self.pool.execute(
            """
            INSERT INTO deleted_exhibits (name, quantity, obtaining, discovery, description, assignment, number, collection, fund, image, visible)
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


    async def delete(self, id: int) -> None:
        """Delete an exhibit from recently deleted exhibits table by id"""
        await self.pool.execute(
            """
            DELETE FROM deleted_exhibits WHERE id = $1
            """,
            id
        )
