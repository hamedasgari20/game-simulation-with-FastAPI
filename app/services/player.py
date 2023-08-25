from typing import List

import settings
from app.models import Robot, Dinosaur, BoardState, RobotMove, GameState, Player


def perform_action(move: RobotMove, board_state: BoardState) -> GameState:
    robot_id = move.robot_id
    action = move.action

    # Find the robot with the specified ID
    robot = next((r for r in board_state.robots if r.id == robot_id), None)
    if robot:
        if action.startswith("move"):
            updated_state = move_robot(robot, action, board_state)
        elif action == "attack":
            updated_state = attack_with_robot(robot, board_state)
        else:
            raise ValueError("Invalid action")

        return updated_state
    else:
        raise ValueError("Robot not found")


def move_robot(robot: Robot, action: str, board_state: BoardState) -> GameState:
    # Implement the logic to move the robot based on the action
    # Update the robot's position and return the updated game state
    # You should handle bounds checking and any other game-specific logic here
    updated_robots = [r if r.id != robot.id else move_robot_position(r, action) for r in board_state.robots]
    updated_state = BoardState(players=board_state.players, robots=updated_robots, dinosaurs=board_state.dinosaurs)
    return updated_state


def move_robot_position(robot: Robot, action: str) -> Robot:
    # Update the robot's position based on the action
    if action == "move_up":
        return robot.model_copy(update={"y": max(0, robot.y - 1)})
    elif action == "move_down":
        return robot.model_copy(update={"y": min(settings.grid_size - 1, robot.y + 1)})
    elif action == "move_left":
        return robot.model_copy(update={"x": max(0, robot.x - 1)})
    elif action == "move_right":
        return robot.model_copy(update={"x": min(settings.grid_size - 1, robot.x + 1)})
    return robot


def attack_with_robot(robot: Robot, board_state: BoardState) -> GameState:
    # Implement the logic to perform an attack with the robot
    # Update the game state, destroy dinosaurs, and update points
    # Return the updated game state
    updated_dinosaurs = destroy_dinosaurs_around(robot, board_state.dinosaurs)
    destroyed_dinosaur_count = count_destroyed_dinosaurs(robot, board_state.dinosaurs)

    updated_players = []
    for player in board_state.players:
        if any(dino.id in destroyed_dinosaur_count for dino in updated_dinosaurs):
            updated_points = player.points + 1
        else:
            updated_points = player.points
        updated_players.append(Player(id=player.id, points=updated_points))

    updated_state = BoardState(players=updated_players, robots=board_state.robots, dinosaurs=updated_dinosaurs)
    return updated_state


def destroy_dinosaurs_around(robot: Robot, dinosaurs: List[Dinosaur]) -> List[Dinosaur]:
    # Implement the logic to destroy dinosaurs around the robot
    # Return the updated list of dinosaurs after destruction
    # You should check the positions of dinosaurs around the robot and remove them
    return [dino for dino in dinosaurs if not is_near_robot(dino, robot)]


def is_near_robot(dinosaur: Dinosaur, robot: Robot) -> bool:
    # Implement a check to determine if the given dinosaur is near the robot
    # You should check if the positions are adjacent (top, bottom, left, right)
    return abs(dinosaur.x - robot.x) <= 1 and abs(dinosaur.y - robot.y) <= 1


def count_destroyed_dinosaurs(robot: Robot, dinosaurs: List[Dinosaur]) -> int:
    # Implement the logic to count the number of destroyed dinosaurs due to the robot's attack
    # You should count the dinosaurs that are near the robot and return the count
    return sum(1 for dino in dinosaurs if is_near_robot(dino, robot))
