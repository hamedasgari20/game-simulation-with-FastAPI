import unittest

from app.services.board import initialize_board


class TestBoardService(unittest.TestCase):

    def test_initialize_board(self):
        """
        Test initializing the game board.

        This test verifies that the initialize_board function correctly initializes the game board
        with robots, dinosaurs, and players.

        Expected Outcome:
        - The board_state contains the correct number of robots, dinosaurs, and players.
        - The positions of robots and dinosaurs are unique and within the board limits.
        """
        number_of_robots = 3
        number_of_dinosaurs = 5
        number_of_players = 2

        board_state = initialize_board(number_of_robots, number_of_dinosaurs, number_of_players)

        self.assertEqual(len(board_state.robots), number_of_robots)
        self.assertEqual(len(board_state.dinosaurs), number_of_dinosaurs)
        self.assertEqual(len(board_state.players), number_of_players)

        # Check unique positions of robots and dinosaurs
        robot_positions = set((robot.x, robot.y) for robot in board_state.robots)
        self.assertEqual(len(robot_positions), number_of_robots)

        dinosaur_positions = set((dino.x, dino.y) for dino in board_state.dinosaurs)
        self.assertEqual(len(dinosaur_positions), number_of_dinosaurs)


if __name__ == "__main__":
    unittest.main()
