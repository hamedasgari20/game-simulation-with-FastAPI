# models.py

from typing import List

from pydantic import BaseModel
from sqlalchemy import Column, Integer, JSON

from app.database import Base


class Robot(BaseModel):
    id: int
    x: int
    y: int


class Dinosaur(BaseModel):
    id: int
    x: int
    y: int


class RobotMove(BaseModel):
    robot_id: int
    action: str


class Player(BaseModel):
    id: int
    points: int = 0  # Initialize player points to zero


class BoardState(BaseModel):
    players: List[Player]  # List of players with their points
    robots: List[Robot]
    dinosaurs: List[Dinosaur]


class BoardStateModel(Base):
    __tablename__ = "board_states"

    id = Column(Integer, primary_key=True, index=True)
    board_state = Column(JSON)
