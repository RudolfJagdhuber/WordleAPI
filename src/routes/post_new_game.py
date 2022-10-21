#!/usr/bin/env python

"""API route to create a new game with provided settings."""

__author__ = 'Dr. Rudolf Jagdhuber'
__status__ = 'Development'

import os
import secrets

import pandas as pd
import fastapi
from sqlalchemy import text

from src.helpers import DbEngine
from src.input_models import NewGameInput
from src.response_models import GameResponse, SimpleResponse
from src.routes.get_game import get_game


def add_route_post_new_game(app: fastapi.FastAPI):
    """Define the /new_game/ route for a given api object."""
    @app.post(f'{os.environ["API_ROOT_PATH"]}/new_game/',
              tags=['Main Game Functionalities'],
              status_code=201,
              response_model=GameResponse,
              responses={403: {'model': SimpleResponse}})
    async def create_a_new_game(input: NewGameInput) -> GameResponse:
        """Create a new game with a given word-length and number of tries."""
        if input.token != os.environ['API_TOKEN']:
            return fastapi.responses.JSONResponse(
                content={'message': 'Wrong API token.'}, status_code=403)

        # Either select the specified word_id, or a random unplayed word
        if input.word_id > 0:
            word = pd.read_sql(
                text('''
                     SELECT word
                     FROM words
                     WHERE id = :word_id
                     '''),
                con=DbEngine.instance(),
                params={'word_id': input.word_id}
            ).at[0, 'word']
            word_id = input.word_id
        else:
            word_draw = pd.read_sql(
                text('''
                     SELECT id, word
                     FROM words
                     WHERE id NOT IN (
                         SELECT word_id
                         FROM games
                         WHERE player = :user_id
                     )
                     ORDER BY RAND()
                     LIMIT 1
                     '''),
                con=DbEngine.instance(),
                params={'user_id': input.user_id}
            )
            word_id = word_draw.at[0, 'id']
            word = word_draw.at[0, 'word']

        # Create a new game
        id = secrets.token_hex(16)
        with DbEngine.instance().connect() as db_connection:
            db_connection.execute(
                text('''
                     INSERT INTO games (
                         id,
                         player,
                         word_id,
                         word,
                         tries
                     )
                     VALUES (
                         UNHEX(:id),
                         UNHEX(:player),
                         :word_id,
                         :word,
                         :tries
                     )
                     '''),
                id=id,
                player=input.user_id,
                word_id=word_id,
                word=word,
                tries=input.tries
            )

        return get_game(id=id)
