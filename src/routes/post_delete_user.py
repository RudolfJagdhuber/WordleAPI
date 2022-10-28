#!/usr/bin/env python

"""API route to delete all personal data of a user.

Deleting a user means to delete all game data from this user and changing the
db entry in users to uninformative data. The users row is not completely
deleted to avoid errors when registering new generic user names from the number
of rows in the table. Instead the name is changed to 'deleted' + userid, dates
are set to 2000-01-01 and password is set to null.
"""

__author__ = 'Dr. Rudolf Jagdhuber'
__status__ = 'Development'

import os

import fastapi
from sqlalchemy import text

from src.helpers import DbEngine
from src.input_models import DeleteUserInput
from src.response_models import SimpleResponse


def add_route_post_delete_user(app: fastapi.FastAPI):
    """Define the /delete_user/ route for a given api object."""
    @app.post(f'{os.environ["API_ROOT_PATH"]}/delete_user/',
              tags=['User Management'],
              status_code=200,
              response_model=SimpleResponse,
              responses={409: {'model': SimpleResponse},
                         403: {'model': SimpleResponse},
                         404: {'model': SimpleResponse}})
    async def delete_user(input: DeleteUserInput) -> SimpleResponse:
        """Delete all data of a user."""
        if input.token != os.environ['API_TOKEN']:
            return fastapi.responses.JSONResponse(
                content={'message': 'Wrong API token.'}, status_code=403)

        # Reset row of users table first to verify credentials
        with DbEngine.instance().connect() as db_connection:
            result = db_connection.execute(
                text('''
                     UPDATE users
                     SET
                       name = CONCAT("deleted", HEX(id)),
                       password_hash = NULL,
                       creation_date = NULL,
                       password_changed = 0
                     WHERE id = UNHEX(:user_id)
                     AND password_hash = UNHEX(:pw_hexdigest)
                     '''),
                user_id=input.user_id,
                pw_hexdigest=input.password
            )

        # Check if no row was updated (i.e. user_id or password is not correct)
        if result.rowcount == 0:
            return fastapi.responses.JSONResponse(
                content={'message': 'Wrong ID or Password.'}, status_code=404)

        with DbEngine.instance().connect() as db_connection:
            db_connection.execute(
                text('''
                     DELETE FROM games
                     WHERE player = UNHEX(:user_id)
                     '''),
                user_id=input.user_id
            )

        return fastapi.responses.JSONResponse({'message': 'User deleted.'},
                                              200)
