import asyncio
import os

import asyncpg
from asyncpg.transaction import Transaction

from dotenv import load_dotenv

load_dotenv()


async def main():
    connection = await asyncpg.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        user=os.getenv("POSTGRES_USER"),
        database=os.getenv("POSTGRES_DB"),
        password=os.getenv("POSTGRES_PASSWORD", 'postgres'),
    )

    transaction: Transaction = await connection.transaction()

    await transaction.start()

    try:
        await connection.execute("INSERT INTO brand "
                                 "VALUES (DEFAULT, 'brand_1')")
        await connection.execute("INSERT INTO brand "
                                 "VALUES (DEFAULT, 'brand_2')")
    except asyncpg.PostgresError:
        print('Errors, rolling back transaction!')
        transaction.rollback()
    else:
        print('No errors, committing transaction!')

    query = """
        SELECT brand_name FROM brand
        WHERE brand_name LIKE '%brand%'    
    """

    brands = await connection.fetch(query)
    print(brands)

    await connection.close()

asyncio.run(main())