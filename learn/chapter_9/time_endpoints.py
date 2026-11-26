from datetime import datetime

from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response

router = web.RouteTableDef()

# create a time GEt endpoint; when a client calls this endpoint, the time coroutine will run.
@router.get('/time')
async def time(request: Request) -> Response:
    today = datetime.today()

    result = {
        'month': today.month,
        'day': today.day,
        'time': str(today.time()),
    }

    # Take the result dictionary, and turn it into a JSON response.
    return web.json_response(result)

# Create the web application, register the routes, and run the application
app = web.Application()
app.add_routes(router)
web.run_app(app)