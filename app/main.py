from http.client import HTTPException

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import BoardState, BoardStateModel
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
