import asyncio

from fastapi import FastAPI

from app.models import BoardState
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
        return board_state
