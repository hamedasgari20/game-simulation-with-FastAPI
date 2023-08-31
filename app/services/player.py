from typing import List

import settings
from app.models import RobotMove, BoardState, Robot, Player, Dinosaur


def perform_action(move: RobotMove, board_state: BoardState) -> BoardState:
    robot_id = move.robot_id
    action = move.action

    # Find the robot with the specified ID
    try:
        robot = next((r for r in board_state.robots if r.id == robot_id), None)
        if robot:
            if action.startswith("move"):
                updated_state = move_robot_position(robot, action, board_state)
            elif action == "attack":
                updated_state = attack_with_robot(robot, board_state)
            else:
                raise ValueError("Invalid action")

            return updated_state
        else:
            raise ValueError("Robot not found")
    except Exception as e:
        raise ValueError("Robot not found")


def move_robot_position(robot: Robot, action: str, board_state: BoardState) -> BoardState:
    if action == "move_up":
        new_robot = robot.model_copy(update={"y": max(0, robot.y + 1)})
    elif action == "move_down":
        new_robot = robot.model_copy(update={"y": min(settings.grid_size - 1, robot.y - 1)})
    elif action == "move_left":
        new_robot = robot.model_copy(update={"x": max(0, robot.x - 1)})
    elif action == "move_right":
        new_robot = robot.model_copy(update={"x": min(settings.grid_size - 1, robot.x + 1)})
    else:
        return board_state

    return update_board_state(new_robot, board_state)


def attack_with_robot(robot: Robot, board_state: BoardState) -> BoardState:
    updated_dinosaurs = destroy_dinosaurs_around(robot, board_state.dinosaurs)
    destroyed_dinosaur_ids = {dino.id for dino in updated_dinosaurs}

    updated_players = []
    for player in board_state.players:
        if player.id in destroyed_dinosaur_ids:
            updated_points = player.points + 1
        else:
            updated_points = player.points
        updated_players.append(Player(id=player.id, points=updated_points))

    updated_state = BoardState(players=updated_players, robots=board_state.robots, dinosaurs=updated_dinosaurs)
    return updated_state


def destroy_dinosaurs_around(robot: Robot, dinosaurs: List[Dinosaur]) -> List[Dinosaur]:
    # Calculate the coordinates of adjacent cells around the robot
    adjacent_coordinates = [
        (robot.x - 1, robot.y),
        (robot.x + 1, robot.y),
        (robot.x, robot.y - 1),
        (robot.x, robot.y + 1),
    ]

    # Create a set of coordinates of adjacent cells
    adjacent_cells = {(x, y) for x, y in adjacent_coordinates}

    # Filter out dinosaurs that are in adjacent cells
    updated_dinosaurs = [dino for dino in dinosaurs if (dino.x, dino.y) in adjacent_cells]

    return updated_dinosaurs


def is_near_robot(dinosaur: Dinosaur, robot: Robot) -> bool:
    # Check if the given dinosaur is adjacent to the robot (top, bottom, left, right)
    x_diff = abs(dinosaur.x - robot.x)
    y_diff = abs(dinosaur.y - robot.y)
    return (x_diff == 1 and y_diff == 0) or (x_diff == 0 and y_diff == 1)


def count_destroyed_dinosaurs(robot: Robot, dinosaurs: List[Dinosaur]) -> int:
    # Implement the logic to count the number of destroyed dinosaurs due to the robot's attack
    # You should count the dinosaurs that are near the robot and return the count
    return sum(1 for dino in dinosaurs if is_near_robot(dino, robot))


def update_board_state(updated_state: BoardState, original_state: BoardState) -> BoardState:
    # Implement the logic to update the board state based on the action
    # You should handle any game-specific updates and return the new state
    # Example: return updated_state with modifications
    return updated_state
