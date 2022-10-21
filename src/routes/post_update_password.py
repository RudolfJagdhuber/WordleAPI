#!/usr/bin/env python

"""API route to update a users password.

For a given userID, the password is updated with a new value. A typical
application would be to change the password of a generic users to an actual
value set by the user. The column 'password_changed' in the users table is set
to True in this process as well, indicating that the value is not generic
anymore.
"""

__author__ = 'Dr. Rudolf Jagdhuber'
__status__ = 'Development'

import os

import fastapi
from sqlalchemy import text

from src.helpers import DbEngine
from src.response_models import SimpleResponse
from src.input_models import ChangePasswordInput


def add_route_post_update_password(app: fastapi.FastAPI):
    """Define the /update_password/ route for a given api object."""
    @app.post(f'{os.environ["API_ROOT_PATH"]}/update_password/',
              tags=['User Management'],
              status_code=200,
              response_model=SimpleResponse,
              responses={403: {'model': SimpleResponse},
                         404: {'model': SimpleResponse}})
    async def update_password(input: ChangePasswordInput) -> SimpleResponse:
        """Update the stored password hexdigest of a user."""
        if input.token != os.environ['API_TOKEN']:
            return fastapi.responses.JSONResponse(
                content={'message': 'Wrong API token.'}, status_code=403)

        # Update the password for matching old password and user_id
        with DbEngine.instance().connect() as db_connection:
            result = db_connection.execute(
                text('''
                     UPDATE users
                     SET
                         password_hash = UNHEX(:new_password),
                         password_changed = 1
                     WHERE id = UNHEX(:user_id)
                     AND password_hash = UNHEX(:old_password)
                     '''),
                new_password=input.new_password,
                user_id=input.user_id,
                old_password=input.old_password
            )

        # Check if no row was updated (i.e. user_id or password is not correct)
        if result.rowcount == 0:
            return fastapi.responses.JSONResponse(
                content={'message': 'Wrong ID or password.'}, status_code=404)

        return fastapi.responses.JSONResponse({'message': 'Password changed.'},
                                              200)
