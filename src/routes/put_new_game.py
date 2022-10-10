#!/usr/bin/env python

"""API route to create a new game with provided settings."""

__author__ = 'Dr. Rudolf Jagdhuber'
__status__ = 'Development'

import os
import secrets

import fastapi
from sqlalchemy import text

from src.helpers import DbEngine
from src.response_models import GameResponse, SimpleResponse
from src.routes.get_game import get_game


def add_route_put_new_game(app: fastapi.FastAPI):
    """Define the /new_game/ route for a given api object."""
    @app.put(f'{os.environ["API_ROOT_PATH"]}/new_game/',
             tags=['Main Game Functionalities'],
             status_code=201,
             response_model=GameResponse,
             responses={403: {'model': SimpleResponse}})
    async def create_a_new_game(user_id: str,
                                length: int,
                                tries: int,
                                token: str) -> GameResponse:
        """Create a new game with a given word-length and number of tries."""
        if token != os.environ['API_TOKEN']:
            return fastapi.responses.JSONResponse(
                content={'message': 'Wrong API token.'}, status_code=403)

        # TODO: Draw a random word with the intended length
        word = 'dummy'.upper()

        # Create a new game
        id = secrets.token_hex(16)
        with DbEngine.instance().connect() as db_connection:
            db_connection.execute(
                text('INSERT INTO games (id, player, word, tries) '
                     'VALUES (UNHEX(:id), UNHEX(:player), :word, :tries)'),
                id=id,
                player=user_id,
                word=word,
                tries=tries
            )

        return get_game(id=id)
