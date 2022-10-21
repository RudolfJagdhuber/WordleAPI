#!/usr/bin/env python

"""API route to return a single game by id."""

__author__ = 'Dr. Rudolf Jagdhuber'
__status__ = 'Development'

import os
import json

import pandas as pd
import fastapi
from sqlalchemy import text

from src.helpers import DbEngine
from src.response_models import (
    GameResponse, LetterCorrectnessResponse, SimpleResponse
)


def get_game(id: str,
             include_solution: bool = False,
             only_active: bool = False) -> GameResponse:
    """Return a game by its id."""
    game = pd.read_sql(
        text('''
             SELECT
                 HEX(id) as id,
                 HEX(player) as player,
                 word_id,
                 word,
                 tries,
                 guesses,
                 DATE_FORMAT(created, "%Y-%m-%d %T") as created,
                 solved
             FROM games
             WHERE id = UNHEX(:id)
             '''),
        con=DbEngine.instance(),
        params={'id': id}
    ).to_dict('records')

    if not game or (only_active and game[0]['solved'] != 0):
        return fastapi.responses.JSONResponse(
            content={'message': 'Game not found.'}, status_code=404)

    # Format the response to pydantic model
    game = game[0]
    game['length'] = len(game['word'])
    if not include_solution:
        game['word'] = None
    if game['guesses']:
        guesses = json.loads(game['guesses'])
        game['guesses'] = [[LetterCorrectnessResponse.parse_obj(letter)
                            for letter in guess] for guess in guesses]

    return GameResponse.parse_obj(game)


def add_route_get_game(app: fastapi.FastAPI):
    """Define the /game/ route for a given api object."""
    @app.get(f'{os.environ["API_ROOT_PATH"]}/game/',
             tags=['Main Game Functionalities'],
             response_model=GameResponse,
             responses={404: {'model': SimpleResponse}})
    async def find_a_game_by_its_id(id: str,
                                    include_solution: bool = False
                                    ) -> GameResponse:
        """Return a game by its id."""
        return get_game(id=id, include_solution=include_solution)
