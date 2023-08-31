import unittest

from app.models import BoardState, Robot, Dinosaur, RobotMove, Player
from app.services.player import perform_action, move_robot_position, destroy_dinosaurs_around, \
    is_near_robot, count_destroyed_dinosaurs, update_board_state


class TestGameLogic(unittest.TestCase):

    def setUp(self):
        self.sample_board_state = BoardState(
            players=[Player(id=1, points=0), Player(id=2, points=0)],
            robots=[Robot(id=1, x=1, y=1), Robot(id=2, x=2, y=2)],
            dinosaurs=[Dinosaur(id=1, x=3, y=2), Dinosaur(id=2, x=3, y=3)]
        )

    def test_update_board_state(self):
        updated_state = update_board_state(self.sample_board_state, self.sample_board_state)
        self.assertEqual(updated_state, self.sample_board_state)

    def test_count_destroyed_dinosaurs(self):
        robot = self.sample_board_state.robots[0]
        dinosaurs = self.sample_board_state.dinosaurs
        count = count_destroyed_dinosaurs(robot, dinosaurs)
        self.assertEqual(count, 0)

    def test_is_near_robot(self):
        robot = self.sample_board_state.robots[1]
        dinosaur = self.sample_board_state.dinosaurs[0]
        self.assertTrue(is_near_robot(dinosaur, robot))

    def test_is_near_robot_not_near(self):
        robot = self.sample_board_state.robots[0]
        dinosaur = self.sample_board_state.dinosaurs[1]
        self.assertFalse(is_near_robot(dinosaur, robot))

    def test_destroy_dinosaurs_around(self):
        robot = self.sample_board_state.robots[1]
        dinosaurs = self.sample_board_state.dinosaurs
        updated_dinosaurs = destroy_dinosaurs_around(robot, dinosaurs)
        self.assertEqual(len(updated_dinosaurs), 1)

    def test_move_robot_position_up(self):
        robot = self.sample_board_state.robots[0]
        updated_robot = move_robot_position(robot, "move_up", self.sample_board_state)
        self.assertEqual(updated_robot.y, max(0, robot.y + 1))

    def test_move_robot_position_down(self):
        robot = self.sample_board_state.robots[0]
        updated_robot = move_robot_position(robot, "move_down", self.sample_board_state)
        self.assertEqual(updated_robot.y, min(4, robot.y - 1))

    def test_move_robot_position_left(self):
        robot = self.sample_board_state.robots[0]
        updated_robot = move_robot_position(robot, "move_left", self.sample_board_state)
        self.assertEqual(updated_robot.x, max(0, robot.x - 1))

    def test_move_robot_position_right(self):
        robot = self.sample_board_state.robots[0]
        updated_robot = move_robot_position(robot, "move_right", self.sample_board_state)
        self.assertEqual(updated_robot.x, min(4, robot.x + 1))

    def test_perform_action_move(self):
        move = RobotMove(robot_id=1, action="move_up")
        updated_state = perform_action(move, self.sample_board_state)
        self.assertEqual(updated_state, Robot(id=1, x=1, y=2))


class TestPerformAction(unittest.TestCase):
    def setUp(self):
        # Create sample board state for testing
        self.board_state = BoardState(
            players=[Player(id=1, points=0), Player(id=2, points=0)],
            robots=[Robot(id=1, x=1, y=1), Robot(id=2, x=2, y=2)],
            dinosaurs=[Dinosaur(id=1, x=3, y=2)]
        )

    def test_move_robot_position(self):
        move = RobotMove(robot_id=1, action="move-up")
        updated_state = perform_action(move, self.board_state)
        self.assertEqual(updated_state.robots[0].y, 1)

    def test_attack_with_robot(self):
        move = RobotMove(robot_id=2, action="attack")
        updated_state = perform_action(move, self.board_state)
        self.assertEqual(len(updated_state.dinosaurs), 1)
        self.assertEqual(updated_state.players[0].points, 1)

    def test_invalid_action(self):
        move = RobotMove(robot_id=1, action="invalid_action")
        with self.assertRaises(ValueError):
            perform_action(move, self.board_state)

    def test_robot_not_found(self):
        move = RobotMove(robot_id=3, action="move_up")
        with self.assertRaises(ValueError):
            perform_action(move, self.board_state)
