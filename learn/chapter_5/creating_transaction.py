"""
In asyncpg, the easiest way to deal with transactions is to use the connection
.transaction asynchronous context manager to start them. Then, if there is an
exception in the async with block, the transaction will automatically be rolled back.
If everything executes successfully, it will be automatically committed. Let’s look at how to create
a transaction and execute two simple insert statements to add a couple of brands.
"""
import asyncio
import logging

import asyncpg
import os
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
    try:
        async with connection.transaction():
            # start of the database transaction. It is happy case.
            # await connection.execute("INSERT INTO brand "
            #                          "VALUES (DEFAULT, 'brand_1')")
            # await connection.execute("INSERT INTO brand "
            #                          "VALUES (DEFAULT, 'brand_2')")

            # error case
            # This insert statement will
            # error because of a duplicate
            # primary key.
            await connection.execute("INSERT INTO brand "
                                     "VALUES (9999, 'error_1')")
            await connection.execute("INSERT INTO brand "
                                     "VALUES (9999, 'error_2')")
    except Exception:
        logging.exception("Something went wrong")
    finally:
        query = """SELECT brand_name FROM brand WHERE brand_name LIKE 'error%'"""

        results = await connection.fetch(query)
        print(f'Query result was: {results}')
        await connection.close()

asyncio.run(main())