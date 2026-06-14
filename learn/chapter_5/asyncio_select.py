import asyncio
import os

import asyncpg

from dotenv import load_dotenv

load_dotenv()

product_query = """
    SELECT 
    p.product_id, 
    p.product_name, 
    p.brand_id, 
    p.sku_id, 
    pc.product_color_name, 
    pc.product_size_name
    FROM product p
    JOIN sku as s on s.product_id = p.product_id
    JOIN product_color as pc on pc.product_color_id = s.product_color_id
    JOIN product_size as ps on ps.product_size_id = s.product_size_id
    WHERE p.product_id = 100
"""

async def main():
    connection = await asyncpg.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        user=os.getenv("POSTGRES_USER"),
        database=os.getenv("POSTGRES_DB"),
        password=os.getenv("POSTGRES_PASSWORD", 'postgres'),
    )

    print('Creating the product database...')
    queries = [
        connection.execute(product_query),
        connection.execute(product_query),
    ]
    results = await asyncio.gather(*queries)

    print(results)

"""However, if we run this we’ll be greeted with an error:
RuntimeError: readexactly() called while another coroutine is already waiting
for incoming data
Why is this? In the SQL world, one connection means one socket connection to our
database. Since we have only one connection and we’re trying to read the results of
multiple queries concurrently, we experience an error. We can resolve this by creating
multiple connections to our database and executing one query per connection. Since
creating connections is resource expensive, caching them so we can access them when
needed makes sense. This is commonly known as a connection pool."""