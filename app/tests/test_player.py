import unittest
from unittest.mock import Mock

from app.services.player import perform_action, move_robot, attack_with_robot
from app.models import Robot, Dinosaur, RobotMove, BoardState


class TestPlayerService(unittest.TestCase):

    def test_perform_action_move_robot(self):
        """
        Test the perform_action function for moving a robot.

        This test verifies that when a robot is instructed to move, it updates its position correctly.

        """
        # Mocking board_state
        board_state = Mock()
        board_state.robots = [Robot(id=1, x=0, y=0)]

        move = RobotMove(robot_id=1, action="move_up")
        updated_state = perform_action(move, board_state)

        self.assertIsNotNone(updated_state)
        self.assertEqual(len(updated_state.robots), 1)
        self.assertEqual(updated_state.robots[0].y, 0)  # Robot should have moved up

    def test_perform_action_attack_robot(self):
        """
        Test the perform_action function for attacking with a robot.

        This test verifies that when a robot performs an attack, nearby dinosaurs are destroyed.

        """
        # Mocking board_state
        board_state = Mock()
        board_state.robots = [Robot(id=1, x=0, y=0)]
        board_state.dinosaurs = [Dinosaur(id=1, x=1, y=0)]

        move = RobotMove(robot_id=1, action="attack")
        updated_state = perform_action(move, board_state)

        self.assertIsNotNone(updated_state)
        self.assertEqual(len(updated_state.robots), 1)
        self.assertEqual(len(updated_state.dinosaurs), 0)  # Dinosaur should be destroyed

    def test_move_robot(self):
        """
        Test the move_robot function for moving a robot.

        This test verifies that the move_robot function updates the robot's position correctly.

        """
        robot = Robot(id=1, x=0, y=0)
        board_state = BoardState(players=[], robots=[robot], dinosaurs=[])

        updated_state = move_robot(robot, "move_right", board_state)

        self.assertIsNotNone(updated_state)
        self.assertEqual(len(updated_state.robots), 1)
        self.assertEqual(updated_state.robots[0].x, 1)  # Robot should have moved right

    def test_attack_with_robot(self):
        """
        Test the attack_with_robot function for attacking with a robot.

        This test verifies that the attack_with_robot function destroys nearby dinosaurs.

        """
        robot = Robot(id=1, x=0, y=0)
        dinosaur = Dinosaur(id=1, x=1, y=0)
        board_state = BoardState(players=[], robots=[robot], dinosaurs=[dinosaur])

        updated_state = attack_with_robot(robot, board_state)

        self.assertIsNotNone(updated_state)
        self.assertEqual(len(updated_state.robots), 1)
        self.assertEqual(len(updated_state.dinosaurs), 0)  # Dinosaur should be destroyed


if __name__ == '__main__':
    unittest.main()
