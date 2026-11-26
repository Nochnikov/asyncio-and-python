import asyncpg
from aiohttp import web
from aiohttp.web_app import Application
from aiohttp.web_request import Request
from aiohttp.web_response import Response

from asyncpg import Pool
from asyncpg.protocol.record import Record

routes = web.RouteTableDef()
DB_KEY = 'database'

# Create the database pool, and store it in the application instance.
async def create_database_pool(app: Application):
    print('Creating database pool.')
    pool: Pool = await asyncpg.create_pool(
        host='127.0.0.1',
        user='postgres',
        password='postgres',
        database='asyncio_db',
        min_size=6,
        max_size=6,
    )
    app[DB_KEY] = pool

# Destroy the pool in the application instance.
async def destroy_database_pool(app: Application):
    print('Destroying database pool.')
    pool: Pool = app[DB_KEY]
    await pool.close()

# Query all brands and return results to the client
@routes.get('/brands')
async def brands(request: Request) -> Response:
    connection: Pool = request.app[DB_KEY]
    brand_query = 'SELECT brand_id, brand_name FROM brand'

    result: list[Record] = await connection.fetch(brand_query)
    result_as_dict: list[dict] = [dict(brand) for brand in result]
    return web.json_response(result_as_dict)

@routes.get('/products/{id}')
async def get_product(request: Request) -> Response:
    try:
        # Get the product_id parameter from the URL
        str_id = request.match_info['id']
        product_id = int(str_id)

        query = """SELECT product_id, product_name, brand_id FROM product WHERE product_id = $1"""
        connection: Pool = request.app[DB_KEY]

        # Running the query for a single product.
        result: Record = await connection.fetchrow(query, product_id)

        if result is not None:
            # If we have a result, convert it to JSON and send to
            # the client; otherwise, send a "404" not found.
            return web.json_response(dict(result))
        else:
            raise web.HTTPNotFound()
    except ValueError:
        raise web.HTTPBadRequest()

@routes.post('/products')
async def create_product(request: Request) -> Response:
    PRODUCT_NAME = 'product_name'
    BRAND_ID = 'brand_id'

    if not request.can_read_body:
        raise web.HTTPBadRequest()

    body = await request.json()

    if PRODUCT_NAME in body and BRAND_ID in body:
        db = request.app[DB_KEY]
        await db.execute(
            """INSERT INTO product (product_id, product_name, brand_id) VALUES (DEFAULT, $2, $3)""",
            body[PRODUCT_NAME],
            int(body[BRAND_ID]),
        )
        return web.Response(status=201)
    else:
        raise web.HTTPBadRequest()


# Add the create and destroy pool coroutines to startup and cleanup
app = web.Application()
app.on_startup.append(create_database_pool)
app.on_cleanup.append(destroy_database_pool)

app.add_routes(routes)
web.run_app(app)