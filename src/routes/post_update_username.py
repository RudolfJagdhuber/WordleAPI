#!/usr/bin/env python

"""API route to update a username.

For a given userID, the username is updated with a new value. A typical
application would be to change the name of a generic users to an actual
username.
The username can not start with 'user' or 'deleted' to not interfere with
auto-generated names.
"""

__author__ = 'Dr. Rudolf Jagdhuber'
__status__ = 'Development'

import os

import pandas as pd
import fastapi
from sqlalchemy import text

from src.helpers import DbEngine
from src.input_models import ChangeNameInput
from src.response_models import SimpleResponse


def add_route_post_update_username(app: fastapi.FastAPI):
    """Define the /update_username/ route for a given api object."""
    @app.post(f'{os.environ["API_ROOT_PATH"]}/update_username/',
              tags=['User Management'],
              status_code=200,
              response_model=SimpleResponse,
              responses={409: {'model': SimpleResponse},
                         403: {'model': SimpleResponse},
                         404: {'model': SimpleResponse}})
    async def update_username(input: ChangeNameInput) -> SimpleResponse:
        """Update the name of a user."""
        if input.token != os.environ['API_TOKEN']:
            return fastapi.responses.JSONResponse(
                content={'message': 'Wrong API token.'}, status_code=403)

        # Username may not start with 'user' or 'deleted'
        if input.new_name.startswith(('user', 'deleted')):
            return fastapi.responses.JSONResponse(
                content={'message': 'Name not allowed.'}, status_code=403)

        # Check for existing username
        if pd.read_sql(text('''
                            SELECT count(*) as n
                            FROM users
                            WHERE name = :name
                            '''),
                       con=DbEngine.instance(),
                       params={'name': input.new_name}).at[0, 'n'] > 0:
            return fastapi.responses.JSONResponse(
                content={'message': 'Username is taken.'}, status_code=409)

        # Update the name for the given user_id
        with DbEngine.instance().connect() as db_connection:
            result = db_connection.execute(
                text('''
                     UPDATE users
                     SET name = :new_name
                     WHERE id = UNHEX(:user_id)
                     AND password_hash = UNHEX(:pw_hexdigest)
                     '''),
                new_name=input.new_name,
                user_id=input.user_id,
                pw_hexdigest=input.password
            )

        # Check if no row was updated (i.e. user_id or password is not correct)
        if result.rowcount == 0:
            return fastapi.responses.JSONResponse(
                content={'message': 'Wrong ID or Password.'}, status_code=404)

        return fastapi.responses.JSONResponse({'message': 'Username changed.'},
                                              200)
