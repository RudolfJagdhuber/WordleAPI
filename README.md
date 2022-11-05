# Wortel Unlimited API <img src="https://user-images.githubusercontent.com/42039093/200065456-0ee2c416-a195-4d7d-a821-744f8b7257bb.png" align="right" height = 120/>

A FastAPI handling requests for the Android App Wortel Unlimited.
* Android App GitHub Page: https://github.com/RudolfJagdhuber/WortelUnlimitedAndroid
* Android App at Google Play: https://play.google.com/store/apps/details?id=de.datavisions.wortel

The Production Version of this API is deployed in a Kubernetes Cluster
with a non-exposed MySQL Database.

The official API is hosted on https://data-visions.de/wortel/api/

![image](https://user-images.githubusercontent.com/42039093/200065936-2638fe9b-64e2-47c7-a73e-d935abfc1fce.png)

## Local Installation

The image of the most recent main branch version is openly available at
DockerHub
```sh
docker pull jagdhuber/wortel-api:latest
```

To run the docker image you need to have a mysql database running and supply at
least the following environment variables to connect to it.
* `DB_HOST`
* `DB_DATABASE`
* `DB_USER`
* `DB_PASSWORD`

Optionally, you can also specify the following environment variables to
customize the API.
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
docker run -d --name wortel-api -p 8080:8080 \
    -e DB_HOST='localhost' \
    -e DB_DATABASE='wortel' \
    -e DB_USER='root' \
    -e DB_PASSWORD='my-secret' \
    jagdhuber/wortel-api:latest
```

## Usage

The API includes several endpoints, which allow to interact with the game.

An overview of all endpoints is given from the swagger-ui that comes with
FastAPI. It is available at the root of the API deployment. In the above
example (with port 8080 mapped to 8080 of localhost), this would be at
*localhost:8080*. 

The basic gameplay would be:
1) A new user is generated with `POST register_generic`.
2) The user creates a new game with `POST new_game`. 
3) The player can now make guesses via `POST guess`. 

A game output returned for example by `POST guess` or `POST new_game` contains
all revelant metadata, as well as the list of guesses .

Below you can find an example output. The correct word here is `DUMMY`.
Three guesses were made: `MUSIK`, `SUMME`, `DUMMY`. The last one solved the
game and set the `solved` field to `3` (i.e. the number of guesses needed). 


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
