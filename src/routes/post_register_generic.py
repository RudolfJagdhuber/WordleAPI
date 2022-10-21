#!/usr/bin/env python

"""API route to generate a new generic user.

When starting the App for the first time, a new generic user is generated, and
the username and random password are sent back to the App. The app stores this
information, which allows basic gameplay without registering first.
The user can later change the generic username and password to be able to
fully take control of the account and also login at different devices.
"""

__author__ = 'Dr. Rudolf Jagdhuber'
__status__ = 'Development'

import os
import secrets

import pandas as pd
import hashlib
import fastapi
from sqlalchemy import text

from src.helpers import DbEngine
from src.response_models import GenericUserResponse, SimpleResponse
from src.input_models import TokenInput


def add_route_post_register_generic(app: fastapi.FastAPI):
    """Define the /register_generic/ route for a given api object."""
    @app.post(f'{os.environ["API_ROOT_PATH"]}/register_generic/',
              tags=['User Management'],
              status_code=201,
              response_model=GenericUserResponse,
              responses={403: {'model': SimpleResponse}})
    async def register_generic(input: TokenInput) -> GenericUserResponse:
        """Create a new generic user with unique name and random password."""
        if input.token != os.environ['API_TOKEN']:
            return fastapi.responses.JSONResponse(
                content={'message': 'Wrong API token.'}, status_code=403)

        # Generate random values for id and password
        id = secrets.token_hex(16)
        password = secrets.token_hex(32)

        # Create a new DB entry. A unique name is generated automatically as
        # 'user' + str(1556 + <number of users>)
        with DbEngine.instance().connect() as db_connection:
            db_connection.execute(
                text('''
                     INSERT INTO users (
                         id,
                         name,
                         password_hash
                     )
                     VALUES (
                         UNHEX(:id),
                         (SELECT CONCAT("user", (
                             SELECT count(*)  + 1556
                             FROM (SELECT * FROM users) as x
                         ))),
                         UNHEX(:pw_hex)
                     )
                     '''),
                id=id, pw_hex=hashlib.sha256(password.encode()).hexdigest()
            )

        # Fetch the implicitly generated name and return the new user
        name = pd.read_sql(text('SELECT name FROM users WHERE id=UNHEX(:id)'),
                           con=DbEngine.instance(),
                           params={'id': id}).at[0, 'name']

        return GenericUserResponse(id=id, name=name, password=password)
