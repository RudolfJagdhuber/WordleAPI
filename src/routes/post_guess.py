#!/usr/bin/env python

"""API route to make a word-guess for an active game.

The data of the given game id is loaded. Then, for each letter of the guess, a
LetterCorrectnessResponse is created by comparing it with the solution. Each
letter can be
- not found in the solution
- in the correct position
- in a different position
- in the correct AND a different position (if the letter occurs multiple times)

Finally a list of LetterCorrectnessResponses is returned
"""

__author__ = 'Dr. Rudolf Jagdhuber'
__status__ = 'Development'

import os

import fastapi
from sqlalchemy import text

from src.helpers import DbEngine
from src.constants import GAME_ACTIVE, GAME_LOST
from src.response_models import (
    WordCorrectnessResponse, GuessListResponse, GameResponse, SimpleResponse
)
from src.input_models import GuessInput
from src.routes.get_game import get_game


def check_guess(guess: str, solution: str) -> WordCorrectnessResponse:
    """Check a word against the solution and returns the pydantic models."""
    result = []
    for i, letter in enumerate(guess[:len(solution)].upper()):
        result.append({
            'letter': letter,
            'correct_position': solution[i] == letter,
            'different_position': letter in (solution[:i] + solution[(i+1):])
        })
    return WordCorrectnessResponse(__root__=result)


def add_route_post_guess(app: fastapi.FastAPI):
    """Define the /guess/ route for a given api object."""
    @app.post(f'{os.environ["API_ROOT_PATH"]}/guess/',
              tags=['Main Game Functionalities'],
              status_code=200,
              response_model=GameResponse,
              responses={403: {'model': SimpleResponse},
                         404: {'model': SimpleResponse}})
    async def make_a_guess(input: GuessInput) -> GameResponse:
        """Make a guess for a game and get the correctness of this guess."""
        if input.token != os.environ['API_TOKEN']:
            return fastapi.responses.JSONResponse(
                content={'message': 'Wrong API token.'}, status_code=403)

        # Get the game data for the given ID, and check if its active
        game = get_game(id=input.game_id, include_solution=True,
                        only_active=True)
        if not game.__dict__.get('id'):  # Error Response has no id field
            return fastapi.responses.JSONResponse(
                content={'message': 'Active game not found.'}, status_code=404)

        # Check against the solution
        response = check_guess(input.guess, game.word)
        guesses = game.guesses or GuessListResponse(__root__=[])
        guesses.__root__.append(response)
        is_solved = all([x.correct_position for x in response.__root__])
        is_lost = not is_solved and (len(guesses.__root__) >= game.tries)

        # Insert guess and update solved status in the games DB entry
        with DbEngine.instance().connect() as db_connection:
            db_connection.execute(
                text('UPDATE games SET guesses = :guesses, solved = :solved '
                     'WHERE id = UNHEX(:game_id)'),
                guesses=guesses.json(),
                solved=(len(guesses.__root__) if is_solved else
                        GAME_LOST if is_lost else
                        GAME_ACTIVE),
                game_id=input.game_id
            )

        # Reload the game from the DB to ensure that the data has been stored
        return get_game(id=input.game_id,
                        include_solution=(is_solved or is_lost))
