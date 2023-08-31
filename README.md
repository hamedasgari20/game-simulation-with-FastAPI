# Game Simulation using FastAPI

This project aims to create a robust and highly performant REST API service that supports a game simulation. 

## Objective

The objective of this project is to develop a REST API service that allows players to control robots in a game simulation. The API should support features such as initializing the game board, moving robots, attacking and destroying dinosaurs, tracking player points, and returning the current game state.

## Features

- **Board Initialization:** An API endpoint to initialize the game board with robots and dinosaurs.
- **Player Actions:** An API endpoint that allows players to move robots, attack, and gain points by destroying dinosaurs.
- **State:** An API endpoint that returns the current simulation state including the points of each player.

## Project Highlights

- The game board is initialized with a 50x50 grid simulation space.
- Players can control robots with actions like move up, move down, move left, move right, and attack.
- A robot attack destroys dinosaurs around it (if a dinosaur is in the top, left, right, or bottom cell).
- The game is not turn-based; players can control robots at their preferred frequency.
- The game ends when there are no dinosaurs left.

## Project Structure

The project follows a modular design and is structured as follows:

- `app/`: Contains the main application code.
  - `main.py`: Defines FastAPI application and API endpoints.
  - `models.py`: Defines Pydantic models for request and response data.
  - `services/`: Contains service modules (e.g., `board.py` and `player.py`) with core logic.
- `tests/`: Contains unit tests for the application.
  - `test_board.py`: Example unit tests for the board service.
  - `test_player.py`: Example unit tests for the player service.

## Getting Started

To run the project locally:

1. Clone the repository:

```angular2html
git clone https://github.com/yourusername/game-simulation-api.git cd game-simulation-api

```

2. Install Docker on your machine.
3. Navigate to the project directory.
4. Build the Docker image using following command:
```angular2html
docker build -t game-simulation-api .

```
5. Run the Docker container using the following commant: 
```angular2html
docker run -p 8000:8000 game-simulation-api
```

6. Run without docker from source directory
- Create VENV and activate it
- install requirements
Then run the following command
```angular2html
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints
List of API endpoints
```angular2html
POST /docs
```

Initialize the game board with robots and dinosaurs with following API.
```angular2html
POST /initialize-board
```

Get the state of the game simulation for a specific board ID.
here is its information:
```angular2html
    Get the state of the game simulation for a specific board ID.

    Args:
    board_id (int): The ID of the board for which to retrieve the state.

    Returns:
    BoardState: The state of the game simulation for the specified board ID.
```
```angular2html
GET /board-state/{board_id}
```

Move a robot or perform an attack.
here is its information:

```angular2html
    Move a robot or perform an attack.

    Args:
    board_id (int): The ID of the board on which the move is being made.
    player_id (int): The ID of the player making the move.
    move (RobotMove): The action to be performed by the robot.
    possible arguments: move_up, move_down, move_left, move_right, attack (if robot be adjacent to a dinosaur)

    Returns:
    BoardState: The updated game state after the action is performed.
    When robot attacks to a dinosaur it replace dinosaur location, one point has been granted to the player and game board updates
```
```angular2html
POST /move-robot
```



## Configurations

Modify **settings.py** to adjust game settings such as grid size and number of robots.

## Dependencies
- FastAPI
- Uvicorn
- Pydantic

## Run docker compose
file to run containers using following command

```angular2html
docker-compose up --build
```

This command creates containers and runs them 

## Generate Migrations
Generate an initial migration using Alembic:

```angular2html
alembic revision --autogenerate -m "create_board_states_table"

```

## Apply Migrations
Apply the migration to your database:

```angular2html
alembic upgrade head

```

## Challenges in this project
In the following, some of the main challenges in this project have been discussed.

#### The first challenge: 
The main challenge for me in this project was that I had never worked with FastAPI before and it was the first time I wanted to run a project with FastAPI. I was able to implement this project by researching studying and using artificial intelligence tools.

#### The second challenge: 
because I am currently working, I had very limited time to devote to this task, so I was able to handle the project by working late and using my days off.

#### The third challenge: 
In the project, many parts have to be created from scratch such as migration creation and database connection, such as how to do migrations, which I found out through research.

#### The fourth challenge: 
So far, most of the needs that have been solved were related to needs like updating the login page or filtering more pages in the field of web development, and this type of simulation was new to me, but by thinking and researching, I was able to do it for I was also attractive


## final word

Finally, thank you for the time you spend on the interview and review of the task. I hope I have the honor to work in your research team


with the best wishes

Hamed Asgari