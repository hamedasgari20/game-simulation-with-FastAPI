import unittest

from app.models import RobotMove, Robot, GameState, Dinosaur
from app.services.game import perform_action


class TestGameService(unittest.TestCase):

    def test_move_robot(self):
        """
        Test moving a robot to a new position.

        This test verifies that the perform_action function correctly updates the position
        of a robot when a move action is performed.

        The robot is initially at position (0, 0). After performing a move_right action,
        the robot's new position should be (1, 0).

        Expected Outcome:
        - The robot's position is updated as expected.
        - The game state reflects the updated robot position.
        """
        robots = [Robot(id=1, x=0, y=0)]
        dinosaurs = []
        move = RobotMove(robot_id=1, action="move_right")
        expected_robots = [Robot(id=1, x=1, y=0)]
        expected_state = GameState(robots=expected_robots, dinosaurs=dinosaurs)

        updated_state = perform_action(move, robots, dinosaurs)
        self.assertEqual(updated_state, expected_state)

    def test_attack_dinosaur(self):
        """
        Test attacking and destroying dinosaurs.

        This test verifies that the perform_action function correctly handles an attack action.
        The robot is positioned at (1, 1), and there are two dinosaurs adjacent to it.
        After performing an attack action, both dinosaurs should be destroyed, and the robot's
        points should be updated to 2.

        Expected Outcome:
        - The dinosaurs are destroyed.
        - The robot's points are updated.
        - The game state reflects the updated robot points and the absence of dinosaurs.
        """
        robots = [Robot(id=1, x=1, y=1)]
        dinosaurs = [Dinosaur(id=1, x=1, y=0), Dinosaur(id=2, x=0, y=1)]
        move = RobotMove(robot_id=1, action="attack")
        expected_robots = [Robot(id=1, x=1, y=1, points=2)]
        expected_state = GameState(robots=expected_robots, dinosaurs=[])

        updated_state = perform_action(move, robots, dinosaurs)
        self.assertEqual(updated_state, expected_state)


if __name__ == "__main__":
    unittest.main()
