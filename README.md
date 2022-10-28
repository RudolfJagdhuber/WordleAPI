# Wordle API <img src="https://user-images.githubusercontent.com/42039093/183470830-59b57576-90aa-4c91-a471-e582f92dde43.png" align="right" height = 120/>

This repository contains the source code of a FastAPI handling requests to play
a word-guessing game in the style of "Wordle". The Production Version of this
API is deployed in a Kubernetes Cluster and connects to a separate MySQL
Database.

It is hosted on http://82.165.111.42/wordle/api/


## Installation

The image of the most recent main branch version is openly available at
DockerHub
```sh
docker pull jagdhuber/wordle-api:latest
```

To run the docker image and connect to a mysql database, you need to supply at
least the following environment variables
* `DB_HOST`
* `DB_DATABASE`
* `DB_USER`
* `DB_PASSWORD`

Optionally, you can also specify the following environment variables
* `API_HOST`
* `API_PORT`
* `API_TOKEN`
* `API_ROOT_PATH`

The default values for these are `0.0.0.0`, `8080`, `""`. If not executed in a
docker context, you might want to change the host to `localhost` instead. The
`API_TOKEN` can be seen as a password, which protects certain endpoints from
misuse or outside attacks. Non public endpoints, like for example `/new_game`,
can only be accessed, if the correct token is provided. The `API_ROOT_PATH` is
used if the root of the API is not the webservers root.

An example using the mysql:8.0.30 image from dockerhub (with default user
*root* and password *my-secret*):
```sh
docker run -d --name wordle-api -p 8080:8080 \
    -e DB_HOST='localhost' \
    -e DB_DATABASE='wordle' \
    -e DB_USER='root' \
    -e DB_PASSWORD='my-secret' \
    jagdhuber/wordle-api:latest
```

## Usage

The API includes several endpoints, which allow to interact with the game.

An overview of all endpoints is given from the swagger-ui that comes with
FastAPI. It is available at the root of the API deployment. In the above
example (with port 8080 mapped to 8080 of localhost), this would be at
*localhost:8080*. 

The basic gameplay would be to create a new game with the `POST new_game`
route. In the following, the player can make guesses via the `POST guess`
route. 

An output for a finished game is given below. The correct word was `DUMMY`.
Three guesses were made: `MUSIK`, `SUMME`, `DUMMY`. The last one solved the
game and set the `solved` field to `1`. 


```json
{
  "id": "3AE74D532A6454A558E6EFFDFA6B4948",
  "player": "2DB259B4517AA513F6E97E078F7CA688",
  "word_id": 1234,
  "word": "DUMMY",
  "length": 5,
  "tries": 6,
  "guesses": [
    [
      { "letter": "M", "correct_position": false, "different_position": true },
      { "letter": "U", "correct_position": true, "different_position": false },
      { "letter": "S", "correct_position": false, "different_position": false },
      { "letter": "I", "correct_position": false, "different_position": false },
      { "letter": "K", "correct_position": false, "different_position": false }
    ],
    [
      { "letter": "S", "correct_position": false, "different_position": false },
      { "letter": "U", "correct_position": true, "different_position": false },
      { "letter": "M", "correct_position": true, "different_position": true },
      { "letter": "M", "correct_position": true, "different_position": true },
      { "letter": "E", "correct_position": false, "different_position": false }
    ],
    [
      { "letter": "D", "correct_position": true, "different_position": false },
      { "letter": "U", "correct_position": true, "different_position": false },
      { "letter": "M", "correct_position": true, "different_position": true },
      { "letter": "M", "correct_position": true, "different_position": true },
      { "letter": "Y", "correct_position": true, "different_position": false }
    ]
  ],
  "created": "2022-10-09 23:54:08",
  "solved": 3
}
```