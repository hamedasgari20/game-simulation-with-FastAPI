# models.py

from typing import List

from pydantic import BaseModel


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


class GameState(BaseModel):
    robots: List[Robot]
    dinosaurs: List[Dinosaur]
    player_points: int


class PlayerActionResponse(BaseModel):
    success: bool
    message: str
    game_state: GameState


class Player(BaseModel):
    id: int
    points: int = 0  # Initialize player points to zero


class BoardState(BaseModel):
    players: List[Player]  # List of players with their points
    robots: List[Robot]
    dinosaurs: List[Dinosaur]
