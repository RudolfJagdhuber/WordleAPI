#!/usr/bin/env python

"""The main 'Better Wordle' API script.

This script binds all endpoints to the fastapi client and serves it on the
host and port specified in the respective environment variables
"""

__author__ = 'Dr. Rudolf Jagdhuber'
__status__ = 'Development'

import os

import fastapi
import uvicorn

from src.helpers import DbEngine
from src.routes import (
    add_route_put_new_game, add_route_get_game, add_route_post_guess
)


tags = [
    {
        'name': 'Main Game Functionalities',
        'description': 'Requests needed for core game functionalities.'
    }
]

api = fastapi.FastAPI(
    title='Better Wordle API',
    description=('An API to handle requests for the "Better Wordle" App.'),
    openapi_tags=tags,
    docs_url=f'{os.environ["API_ROOT_PATH"]}/',
    openapi_url=f'{os.environ["API_ROOT_PATH"]}/openapi.json'
)

# Add all endpoints to the api
add_route_put_new_game(api)
add_route_get_game(api)
add_route_post_guess(api)


@api.on_event('startup')
async def on_start():
    DbEngine.instance()


# Run the app on the host and ports specified in the environment variables
uvicorn.run(
    app=api,
    host=os.environ['API_HOST'],
    port=int(os.environ['API_PORT'])
)
