from typing import List
from pydantic import BaseModel


class Player(BaseModel):
    id: int
    points: int = 0


class Robot(BaseModel):
    id: int
    x: int
    y: int


class Dinosaur(BaseModel):
    id: int
    x: int
    y: int


class BoardState(BaseModel):
    players: List[Player]
    robots: List[Robot]
    dinosaurs: List[Dinosaur]
