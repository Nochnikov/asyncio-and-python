import logging
import asyncio
import os
from dotenv import load_dotenv
import asyncpg

load_dotenv()

async def main():
    connection = await asyncpg.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        user=os.getenv("POSTGRES_USER"),
        database=os.getenv("POSTGRES_DB"),
        password=os.getenv("POSTGRES_PASSWORD", 'postgres'),
    )

    async with connection.transaction():
        await connection.execute("INSERT INTO brand VALUES (DEFAULT, 'my_new_brand')")

        try:
            async with connection.transaction():
                await connection.execute("INSERT INTO product_color VALUES (1, 'black')")
        except Exception as ex:
            logging.warning('Ignoring error inserting product color', exc_info=ex)

    await connection.close()

asyncio.run(main())