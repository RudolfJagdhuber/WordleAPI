#!/usr/bin/env python

"""Provides global helper functions, like the db connection logic."""

__author__ = 'Dr. Rudolf Jagdhuber'
__status__ = 'Development'

import os

import sqlalchemy


class DbEngine:
    """A singleton holding an sqlalchemy engine. Initialized at API startup."""
    _engine: sqlalchemy.engine.base.Engine = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls) -> sqlalchemy.engine.base.Engine:
        """Return the engine if initialized, or initialize it first."""
        return cls._engine or cls._init_engine()

    @classmethod
    def _init_engine(cls) -> sqlalchemy.engine.base.Engine:
        """Initialize the class engine field from environment credentials."""
        cls._engine = sqlalchemy.create_engine(
            f'mysql+pymysql://'
            f'{os.environ["DB_USER"]}:{os.environ["DB_PASSWORD"]}@'
            f'{os.environ["DB_HOST"]}/{os.environ["DB_DATABASE"]}'
        )
        return cls._engine
