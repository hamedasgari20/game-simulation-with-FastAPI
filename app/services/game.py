from typing import List

import settings
from app.models import RobotMove, Robot, Dinosaur, GameState


def perform_action(move: RobotMove, robots: List[Robot], dinosaurs: List[Dinosaur]) -> GameState:
    robot = next((r for r in robots if r.id == move.robot_id), None)

    if robot:
        if move.action == "move_up":
            robot.y = max(0, robot.y - 1)
        elif move.action == "move_down":
            robot.y = min(settings.grid_size - 1, robot.y + 1)
        elif move.action == "move_left":
            robot.x = max(0, robot.x - 1)
        elif move.action == "move_right":
            robot.x = min(settings.grid_size - 1, robot.x + 1)
        elif move.action == "attack":
            destroyed_dinosaurs = []
            for dino in dinosaurs:
                if (abs(robot.x - dino.x) == 1 and robot.y == dino.y) or \
                        (robot.x == dino.x and abs(robot.y - dino.y) == 1):
                    destroyed_dinosaurs.append(dino)

            for dino in destroyed_dinosaurs:
                dinosaurs.remove(dino)
                robot.points += 1

        updated_state = GameState(robots=robots, dinosaurs=dinosaurs, player_points=robot.points)
        return updated_state
    else:
        raise ValueError("Robot not found")
