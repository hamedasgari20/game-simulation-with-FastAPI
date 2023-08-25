# Board initialization logic
import random

import settings
from app.models import Robot, Dinosaur, BoardState


def initialize_board():
    """
    Initialize the game board with robots and dinosaurs.

    This function generates the initial state of the game board by placing robots and dinosaurs
    on the board. It ensures that no two entities share the same position. The number of robots
    and dinosaurs are determined by the settings module.

    Returns:
    BoardState: The initial state of the game board containing robots and dinosaurs.
    """
    used_positions = set()
    robots = []
    dinosaurs = []

    for i in range(settings.number_of_robots):
        x, y = generate_unique_position(used_positions)
        robots.append(Robot(id=i, x=x, y=y))
        used_positions.add((x, y))

    for j in range(settings.number_of_dinosaurs):
        x, y = generate_unique_position(used_positions)
        dinosaurs.append(Dinosaur(id=j, x=x, y=y))
        used_positions.add((x, y))

    board_state = BoardState(robots=robots, dinosaurs=dinosaurs)
    return board_state


def generate_unique_position(used_positions):
    """
    Generate a unique position for an entity on the game board.

    This function generates a random position (x, y) within the board boundaries that has not been
    used before. It ensures that entities like robots and dinosaurs are placed at unique positions.

    Args:
    used_positions (set): A set containing positions that have already been used.

    Returns:
    Tuple[int, int]: The generated unique position (x, y).
    """
    while True:
        x = random.randint(0, settings.board_size)
        y = random.randint(0, settings.board_size)
        position = (x, y)
        if position not in used_positions:
            return x, y
