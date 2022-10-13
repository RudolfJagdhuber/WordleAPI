#!/usr/bin/env python

"""The main 'Open Wordle' API script.

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
    add_route_post_register_generic, add_route_post_update_password,
    add_route_post_update_username, add_route_post_login,
    add_route_post_new_game, add_route_get_game, add_route_post_guess
)


tags = [
    {
        'name': 'User Management',
        'description': 'Requests regarding user data, login, or registration.'
    },
    {
        'name': 'Main Game Functionalities',
        'description': 'Requests needed for core game functionalities.'
    }
]

api = fastapi.FastAPI(
    title='Open Wordle API',
    description=('An API to handle requests for the "Open Wordle" App.'),
    openapi_tags=tags,
    docs_url=f'{os.environ["API_ROOT_PATH"]}/',
    openapi_url=f'{os.environ["API_ROOT_PATH"]}/openapi.json'
)

# Add all endpoints to the api
add_route_post_register_generic(api)
add_route_post_update_password(api)
add_route_post_update_username(api)
add_route_post_login(api)
add_route_post_new_game(api)
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
