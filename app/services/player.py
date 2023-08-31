from typing import List

import settings
from app.models import RobotMove, BoardState, Robot, Player, Dinosaur


def perform_action(player_id: int, move: RobotMove, board_state: BoardState) -> BoardState:
    robot_id = move.robot_id
    action = move.action

    # Find the robot with the specified ID
    robot_found = False
    updated_robots = []
    for robot in board_state.robots:
        if robot.id == robot_id:
            robot_found = True
            if action.startswith("move"):
                updated_robot = move_robot_position(robot, action, board_state)
            elif action == "attack":
                updated_robot = attack_with_robot(player_id, robot, board_state)
            else:
                raise ValueError("Invalid action")
            updated_robots.append(updated_robot)
        else:
            updated_robots.append(robot)

    if not robot_found:
        raise ValueError(f"Robot with ID {robot_id} not found")

    # Create an updated BoardState with the new robots
    updated_board_state = BoardState(players=board_state.players, robots=updated_robots,
                                     dinosaurs=board_state.dinosaurs)
    return updated_board_state

    # Create an updated BoardState with the new robots
    updated_board_state = BoardState(players=board_state.players, robots=updated_robots,
                                     dinosaurs=board_state.dinosaurs)
    return updated_board_state


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


def attack_with_robot(player_id: int, robot: Robot, board_state: BoardState) -> BoardState:
    # Destroy dinosaurs around the robot
    updated_dinosaurs = destroy_dinosaurs_around(robot, board_state.dinosaurs)
    destroyed_dinosaur_ids = {dino.id for dino in updated_dinosaurs}

    # Update player points
    updated_players = []
    for player in board_state.players:
        if player.id == player_id:
            updated_points = player.points + len(destroyed_dinosaur_ids)
            updated_players.append(Player(id=player.id, points=updated_points))
        else:
            updated_players.append(player)

    # Update the robot's position (optional: remove the following if you don't want to update the robot's position)
    updated_robot = robot.model_copy()  # Create a copy of the robot
    updated_robot.x = robot.x - 1  # Update the robot's position (change this to the desired new position)

    # Create a new BoardState with updated data
    updated_state = BoardState(
        players=updated_players,
        robots=[updated_robot if r.id == robot.id else r for r in board_state.robots],
        dinosaurs=[dino for dino in board_state.dinosaurs if dino.id not in destroyed_dinosaur_ids]
    )

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
