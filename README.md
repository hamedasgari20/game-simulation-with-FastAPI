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
  - `services/`: Contains service modules (e.g., `board.py`) with core logic.
- `tests/`: Contains unit tests for the application.
  - `test_board.py`: Example unit tests for the board service.

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

```angular2html
POST /initialize-board
```
Initialize the game board with robots and dinosaurs.

```angular2html
POST /docs
```
List of API endpoints


## Configurations

Modify **settings.py** to adjust game settings such as grid size and number of robots.

## Dependencies
- FastAPI
- Uvicorn
- Pydantic

## Run docker compose
file to run containers using folloewing command

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