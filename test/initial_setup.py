#!/usr/bin/env python

"""Basic setup of the DB for testing.

Before executing this script, set up a new empty database named 'wordle' and
execute the init.sql script.

This script is not used in Production. Credentials are dummies for testing.
"""

import requests


API_HOST = 'http://localhost:8080'
API_TOKEN = 'test'
USER = '2db259b4517aa513f6e97e078f7ca688'
GUESSES = ['Musik', 'sUmMe', 'DUMMYfoo']


# Create a new game
game = requests.put(f'{API_HOST}/new_game', params={
    'user_id': USER, 'length': 5, 'tries': 5, 'token': API_TOKEN}).json()

# Make 3 guesses
for i in range(3):
    game = requests.post(f'{API_HOST}/guess', params={
        'game_id': game['id'], 'guess': GUESSES[i], 'token': API_TOKEN}).json()

print(game)
