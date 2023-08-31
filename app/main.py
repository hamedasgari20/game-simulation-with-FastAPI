import asyncio
import json
from http.client import HTTPException

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import BoardState, BoardStateModel, RobotMove
from app.services.board import initialize_board
from app.services.player import perform_action

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# endpoint definitions...

@app.post("/initialize-board", response_model=BoardState, summary="Initialize Game Board")
async def initialize_game_board():
    board_state = initialize_board()
    # Create a BoardStateModel instance and save it to the database
    db = SessionLocal()
    db_board_state = BoardStateModel(board_state=board_state.dict())
    db.add(db_board_state)
    db.commit()
    db.refresh(db_board_state)
    return board_state


@app.get("/board-state/{board_id}", response_model=BoardState, summary="Get Board State by ID")
async def get_board_state_by_id(board_id: int, db: Session = Depends(get_db)):
    """
    Get the state of the game simulation for a specific board ID.

    Args:
    board_id (int): The ID of the board for which to retrieve the state.

    Returns:
    BoardState: The state of the game simulation for the specified board ID.
    """
    db_board_state = db.query(BoardStateModel).filter(BoardStateModel.id == board_id).first()
    if db_board_state:
        return db_board_state.board_state
    else:
        raise HTTPException(status_code=404, detail="Board state not found")


# Define board_state_lock to handle concurrency and race conditions
board_state_lock = asyncio.Lock()


@app.post("/move-robot", response_model=BoardState, summary="Move Robot")
async def move_robot(board_id: int, player_id: int, move: RobotMove, db: Session = Depends(get_db)):
    """
    Move a robot or perform an attack.

    This endpoint allows players to give instructions to a robot using its robot_id.
    A robot can move up, move down, move left, move right, or perform an attack.
    If an attack is performed, dinosaurs in adjacent cells are destroyed, and the player gains points.

    Args:
    board_id (int): The ID of the board on which the move is being made.
    player_id (int): The ID of the player making the move.
    move (RobotMove): The action to be performed by the robot.

    Returns:
    BoardState: The updated game state after the action is performed.
    """
    async with board_state_lock:
        # Retrieve the latest board state from the database
        db_board_state = db.query(BoardStateModel).filter_by(id=board_id).order_by(BoardStateModel.id.desc()).first()
        if db_board_state:
            current_board_state_data = db_board_state.board_state
            current_board_state = BoardState(**current_board_state_data)
        else:
            raise HTTPException(status_code=404, detail="Board state not found")

        # Perform the action with the robot using the player's move
        updated_board_state = perform_action(player_id, move, current_board_state)

        # Update the board state in the database
        new_db_board_state = BoardStateModel(board_state=updated_board_state.dict())
        db.add(new_db_board_state)
        db.commit()
        db.refresh(new_db_board_state)

        return updated_board_state
