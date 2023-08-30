from http.client import HTTPException

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import BoardState, RobotMove, BoardStateModel
from app.services import player
from app.services.board import initialize_board

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
