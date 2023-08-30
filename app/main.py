import asyncio
from http.client import HTTPException

from fastapi import FastAPI

from app.database import SessionLocal
from app.models import BoardState, RobotMove, BoardStateModel
from app.services import player
from app.services.board import initialize_board

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
        # Create a BoardStateModel instance and save it to the database
        db = SessionLocal()
        db_board_state = BoardStateModel(board_state=board_state.dict())
        db.add(db_board_state)
        db.commit()
        db.refresh(db_board_state)
        return board_state


@app.post("/move-robot", response_model=BoardState, summary="Move Robot")
async def move_robot(move: RobotMove):
    """
    Move a robot or perform an attack.

    This endpoint allows players to give instructions to a robot using its robot_id.
    A robot can move up, move down, move left, move right, or perform an attack.
    If an attack is performed, dinosaurs in adjacent cells are destroyed, and the player gains points.

    Args:
    move (RobotMove): The action to be performed by the robot.

    Returns:
    BoardState: The updated game state after the action is performed.
    """
    try:
        global board_state  # Access the global board state
        async with board_state_lock:
            updated_state = player.perform_action(move, board_state)
            board_state = updated_state  # Update the global board state
            return updated_state  # Make sure updated_state is an instance of BoardState
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/game-state", response_model=BoardState, summary="Get Game State")
async def get_game_state():
    """
    Get the current state of the game simulation.

    Returns:
    BoardState: The current state of the game simulation including player points.
    """
    global board_state
    async with board_state_lock:
        return board_state
