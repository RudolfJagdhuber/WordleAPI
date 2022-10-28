#!/usr/bin/env python

"""API route to return an array of all games of a user."""

__author__ = 'Dr. Rudolf Jagdhuber'
__status__ = 'Development'

import os
import json

import pandas as pd
import fastapi
from sqlalchemy import text

from src.helpers import DbEngine
from src.response_models import (
    GameListResponse, GameResponse, LetterCorrectnessResponse, SimpleResponse
)


def add_route_get_game_list(app: fastapi.FastAPI):
    """Define the /game_list/ route for a given api object."""
    @app.get(f'{os.environ["API_ROOT_PATH"]}/game_list/',
             tags=['Main Game Functionalities'],
             response_model=GameListResponse,
             responses={404: {'model': SimpleResponse}})
    async def find_all_games_of_a_user(user_id: str) -> GameListResponse:
        """Return a list of finished games of by its id."""
        game_list = pd.read_sql(
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
                 WHERE player = UNHEX(:user_id)
                 AND SOLVED != 0
                 ORDER BY word_id
                 '''),
            con=DbEngine.instance(),
            params={'user_id': user_id}
        ).to_dict('records')

        # Format the response to the pydantic response model
        game_list = [GameResponse(
            id=game['id'],
            player=game['player'],
            word_id=game['word_id'],
            word=game['word'],
            length=len(game['word']),
            tries=game['tries'],
            guesses=([[LetterCorrectnessResponse.parse_obj(letter)
                       for letter in guess]
                      for guess in json.loads(game['guesses'])]
                     if game['guesses'] else None),
            created=game['created'],
            solved=game['solved']
        ) for game in game_list]

        return GameListResponse(__root__=game_list)
