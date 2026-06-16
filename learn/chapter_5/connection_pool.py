import asyncio
import asyncpg
import os
from dotenv import load_dotenv

from learn.util.async_timer import async_timed

load_dotenv()

product_query = """
SELECT
p.product_id,
p.product_name,
p.brand_id,
s.sku_id,
pc.product_color_name,
ps.product_size_name
FROM product as p
JOIN sku as s on s.product_id = p.product_id
JOIN product_color as pc on pc.product_color_id = s.product_color_id
JOIN product_size as ps on ps.product_size_id = s.product_size_id
WHERE p.product_id = 100
"""

async def query_product(pool: asyncpg.Pool):
    async with pool.acquire() as conn:
        """once we leave the block, the connection will be returned to the pool."""
        return await conn.fetchrow(product_query)

@async_timed()
async def query_products_synchronously(pool, queries):
    return [await query_product(pool) for _ in range(queries)]

@async_timed()
async def query_products_concurrently(pool, queries):
    queries = [query_product(pool) for _ in range(queries)]
    return await asyncio.gather(*queries)

async def main():
    async with asyncpg.create_pool(
        host=os.getenv("POSTGRES_HOST"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        database=os.getenv("POSTGRES_DB"),
        port=int(os.getenv("POSTGRES_PORT")),
        min_size=6,
        max_size=6,
    ) as pool:
        # await asyncio.gather(
        #     query_product(pool),
        #     query_product(pool),
        # )
        await query_products_synchronously(pool, 10000)
        await query_products_concurrently(pool, 10000)

asyncio.run(main())