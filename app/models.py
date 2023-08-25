from typing import List

from pydantic import BaseModel


class Robot(BaseModel):
    id: int
    x: int
    y: int
    points: int = 0  # Default points to 0


class Dinosaur(BaseModel):
    id: int
    x: int
    y: int


class BoardState(BaseModel):
    robots: List[Robot]
    dinosaurs: List[Dinosaur]


class RobotMove(BaseModel):
    robot_id: int
    action: str


class GameState(BaseModel):
    robots: List[Robot]
    dinosaurs: List[Dinosaur]
    player_points: int = 0  # Default player points to 0


class PlayerActionResponse(BaseModel):
    success: bool
    message: str
    game_state: GameState
