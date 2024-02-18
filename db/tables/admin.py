# import asyncio
from asyncpg import Pool, create_pool
from dev.exceptions import AdminNotFound


class Admin:
    login: str
    password: str


class AdminsTable:
    """Admins Table"""

    def __init__(self, pool: Pool) -> None:
        self.pool = pool


    async def create(self) -> None:
        """Create the table"""
        await self.pool.execute(
            """
        CREATE TABLE IF NOT EXISTS admins (
            login TEXT,
            password INT
        )
        """
        )


    async def get_all(self) -> list[Admin]:
        """Get all admins"""
        admins = await self.pool.fetch(
            """
            SELECT * FROM admins
            """
        )
        return [Admin(**admin) for admin in admins]
    

    async def insert(self, admin: Admin) -> None:
        """Insert a new admin user"""
        await self.pool.execute(
            """
            INSERT INTO adminss (login, password)
            VALUES ($1, $2)
            ON CONFLICT DO NOTHING
            """,
            admin.login,
            admin.password
        )
    
    async def delete(self, login: str) -> None:
        """Delete admin user"""
        result = await self.pool.execute(
            """
            DELETE FROM admins WHERE login = $1
            RETURNING login
            """,
            login,
        )

        if not result:
            raise AdminNotFound(login)
        


# async def main():
#     DATABASE = 'exhibits'
#     USER = 'postgres'
#     PASSWORD = 'Aa01011991TrumaA'
#     HOST = 'localhost'
#     PORT = '5432'

#     pool = await create_pool(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
#     return pool

# async def run_create():
#     pool = await main()
#     table = AdminsTable(pool)
#     await table.create()

# if __name__ == "__main__":
#     asyncio.run(run_create())
