import random

from app.models import Robot, Dinosaur, BoardState, Player
from settings import number_of_players, number_of_robots, number_of_dinosaurs, board_size


def initialize_board() -> BoardState:
    used_positions = set()
    robots = []
    dinosaurs = []
    players = [Player(id=i) for i in range(number_of_players)]

    for _ in range(number_of_robots):
        x, y = generate_unique_position(used_positions)
        robots.append(Robot(id=len(robots) + 1, x=x, y=y))
        used_positions.add((x, y))

    for _ in range(number_of_dinosaurs):
        x, y = generate_unique_position(used_positions)
        dinosaurs.append(Dinosaur(id=len(dinosaurs) + 1, x=x, y=y))
        used_positions.add((x, y))

    board_state = BoardState(players=players, robots=robots, dinosaurs=dinosaurs)
    return board_state


def generate_unique_position(used_positions):
    while True:
        x = random.randint(1, board_size)
        y = random.randint(1, board_size)
        position = (x, y)
        if position not in used_positions:
            return x, y

# ... rest of the code
