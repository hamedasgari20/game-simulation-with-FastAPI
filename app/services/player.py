from typing import List, Tuple, Optional
from app.models import RobotMove, Robot, GameState


def perform_action(move: RobotMove, robots: List[Robot], dinosaurs: List[Tuple[int, int]]) -> GameState:
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
            for dino_x, dino_y in dinosaurs:
                if (abs(robot.x - dino_x) == 1 and robot.y == dino_y) or \
                        (robot.x == dino_x and abs(robot.y - dino_y) == 1):
                    destroyed_dinosaurs.append((dino_x, dino_y))

            for dino in destroyed_dinosaurs:
                dinosaurs.remove(dino)
                # Increment robot's points
                robot.points += 1

        game_state = GameState(robots=robots, dinosaurs=dinosaurs)
        return game_state
    else:
        raise ValueError("Robot not found")
