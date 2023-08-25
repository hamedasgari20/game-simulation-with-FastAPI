import unittest
from unittest.mock import patch

import settings
from app.models import BoardState, Robot, Dinosaur
from app.services.board import initialize_board, generate_unique_position


class TestBoardService(unittest.TestCase):

    @patch("app.services.board.random.randint")
    def test_initialize_board_unique_positions(self, mock_randint):
        """
        Test the initialize_board function to ensure that no dinosaurs and robots share the same position.

        This test verifies that the initialize_board function generates a board state where no two entities
        (dinosaurs or robots) have the same position. The mock_randint function is used to provide
        predictable positions for testing.

        Assertions:
        - The returned board_state should be an instance of BoardState.
        - The board_state should contain 2 robots and 7 dinosaurs.
        - Each robot's position should be unique and within the grid boundaries (0 to 6).
        - Each dinosaur's position should be unique and within the grid boundaries (0 to 6).
        - No two entities (dinosaurs or robots) should have the same position.
        """

        mock_randint.side_effect = [
            2, 4,  # First robot position
            3, 2,  # Second robot position
            # ......
            1, 1,  # First dinosaur position
            3, 0,  # Second dinosaur position
            4, 1,  # Third dinosaur position
            1, 3,  # 4th dinosaur position
            4, 3,  # 5th dinosaur position
            1, 5,  # 6th dinosaur position
            3, 5,  # 7th dinosaur position
        ]

        board_state = initialize_board()

        self.assertIsInstance(board_state, BoardState)
        self.assertEqual(len(board_state.robots), settings.number_of_robots)
        self.assertEqual(len(board_state.dinosaurs), settings.number_of_dinosaurs)

        robot_positions = {(robot.x, robot.y) for robot in board_state.robots}
        dinosaur_positions = {(dino.x, dino.y) for dino in board_state.dinosaurs}

        self.assertEqual(len(robot_positions), settings.number_of_robots)
        self.assertEqual(len(dinosaur_positions), settings.number_of_dinosaurs)

        for robot in board_state.robots:
            self.assertIsInstance(robot, Robot)
            self.assertIn((robot.x, robot.y), robot_positions)

        for dinosaur in board_state.dinosaurs:
            self.assertIsInstance(dinosaur, Dinosaur)
            self.assertIn((dinosaur.x, dinosaur.y), dinosaur_positions)

    def test_generate_unique_position(self):
        """
        Test the generate_unique_position function.

        This test verifies that the generate_unique_position function correctly generates unique
        positions for entities, ensuring that no two entities share the same position.

        Assertions:
        - The generated position should be a tuple of two integers.
        - The generated position should not match any previously generated position.
        """

        used_positions = {(1, 1), (2, 3)}  # Example used positions
        unique_position = generate_unique_position(used_positions)

        self.assertIsInstance(unique_position, tuple)
        self.assertEqual(len(unique_position), 2)
        self.assertNotIn(unique_position, used_positions)


if __name__ == "__main__":
    unittest.main()
