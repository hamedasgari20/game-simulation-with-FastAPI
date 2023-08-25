import asyncio

from fastapi import FastAPI, HTTPException

from app.models import RobotMove, GameState, BoardState
from app.services.board import initialize_board
from app.services.game import perform_action

app = FastAPI()

# Define board_state as a global variable and initialize it
board_state = None
board_state_lock = asyncio.Lock()  # Create a lock to protect board_state access


# endpoint definitions...

@app.post("/initialize-board", response_model=BoardState, summary="Initialize Game Board")
async def initialize_game_board():
    global board_state
    async with board_state_lock:
        board_state = initialize_board()
        return board_state


@app.post("/perform-action", response_model=GameState, summary="Perform Robot Action")
async def perform_robot_action(move: RobotMove):
    try:
        global board_state
        async with board_state_lock:
            updated_state = perform_action(move, board_state.robots, board_state.dinosaurs)
            board_state = updated_state
            return updated_state
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/state", response_model=GameState, summary="Get Current Game State")
async def get_game_state():
    """
    Get the current state of the game.

    This endpoint retrieves the current state of the game board, including the positions of robots,
    dinosaurs, and the points of each player.

    Returns:
    GameState: The current state of the game board.
    """
    global board_state
    if board_state is None:
        raise HTTPException(status_code=404, detail="Game board has not been initialized")

    return board_state
