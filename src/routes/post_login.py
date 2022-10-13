#!/usr/bin/env python

"""API route that returns the user ID from a given name and password.

The UserID is the main handle to identify a user and query its data. It is
a random MD5 hash assigned at registration. The login process returns that ID,
for a given username (str) and sha256-hashdigest password (str).
"""

__author__ = 'Dr. Rudolf Jagdhuber'
__status__ = 'Development'

import os

import pandas as pd
import fastapi
from sqlalchemy import text

from src.helpers import DbEngine
from src.input_models import LoginInput
from src.response_models import LoginResponse, SimpleResponse


def add_route_post_login(app: fastapi.FastAPI):
    """Define the /login/ route for a given api object."""
    @app.post(f'{os.environ["API_ROOT_PATH"]}/login/',
              tags=['User Management'],
              response_model=LoginResponse,
              responses={404: {'model': SimpleResponse},
                         403: {'model': SimpleResponse}})
    async def login(input: LoginInput) -> LoginResponse | SimpleResponse:
        """Get the user id from a given name and password sha256-hexdigest."""
        if input.token != os.environ['API_TOKEN']:
            return fastapi.responses.JSONResponse(
                content={'message': 'Wrong API token.'}, status_code=403)

        result = pd.read_sql(
            text('SELECT HEX(id) as id FROM users WHERE '
                 'name = :name AND password_hash = UNHEX(:password)'),
            con=DbEngine.instance(),
            params={'name': input.name, 'password': input.password}
        ).to_dict('records')

        if not result:
            return fastapi.responses.JSONResponse(
                content={'message': 'Wrong credentials.'}, status_code=404)

        return LoginResponse(**result[0])
