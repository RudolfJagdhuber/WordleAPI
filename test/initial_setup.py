#!/usr/bin/env python

"""Basic setup of the DB for testing.

Before executing this script, set up a new empty database named 'wordle' and
execute the init.sql script.

This script is not used in Production. Credentials are dummies for testing.
"""

import hashlib
import json
from textwrap import indent
import requests


API_HOST = 'http://localhost:8080'
API_TOKEN = 'test'
USERNAME1 = 'Rudi1556'
PASSWORD1 = 'dummy'
GUESSES = ['Musik', 'sUmMe', 'DUMMYfoo']


# Register 3 generic users
users = []
users.append(requests.post(f'{API_HOST}/register_generic',
                           json={'token': API_TOKEN}).json())
users.append(requests.post(f'{API_HOST}/register_generic',
                           json={'token': API_TOKEN}).json())
users.append(requests.post(f'{API_HOST}/register_generic',
                           json={'token': API_TOKEN}).json())

# Update password of user 1
requests.post(f'{API_HOST}/update_password', json={
    'user_id': users[0]['id'],
    'old_password': hashlib.sha256(users[0]['password'].encode()).hexdigest(),
    'new_password': hashlib.sha256(PASSWORD1.encode()).hexdigest(),
    'token': API_TOKEN})
users[0]['password'] = PASSWORD1

# Update username of user 1
requests.post(f'{API_HOST}/update_username', json={
    'user_id': users[0]['id'],
    'password': hashlib.sha256(PASSWORD1.encode()).hexdigest(),
    'new_name': USERNAME1,
    'token': API_TOKEN})
users[0]['name'] = USERNAME1

# Create a new game
game = requests.post(f'{API_HOST}/new_game', json={
    'user_id': users[0]['id'], 'length': 5, 'tries': 5,
    'token': API_TOKEN}).json()

# Make 3 guesses
for i in range(3):
    game = requests.post(f'{API_HOST}/guess', json={
        'game_id': game['id'], 'guess': GUESSES[i], 'token': API_TOKEN}).json()

# Store the generated data in text file
with open('test_info.json', 'w') as f:
    json.dump({'users': users, 'game': game}, f, indent=4)

# Load the generated data from text file
with open('test_info.json', 'r') as f:
    data = json.load(f)

print(json.dumps(data, indent=2))
