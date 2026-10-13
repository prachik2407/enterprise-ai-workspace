"""Run with: python test_db.py (from the backend directory)."""
import asyncio

from sqlalchemy import text
from app.database.session import engine


async def main() -> None:
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))
    print("Database connection successful.")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
