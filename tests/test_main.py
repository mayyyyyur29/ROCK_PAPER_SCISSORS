import unittest
from unittest.mock import patch
import io
import sys
from main import main

class TestMain(unittest.TestCase):
    @patch('builtins.input', side_effect=['Alice', 'rock', 'paper', 'scissors'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_full_game_completion(self, mock_stdout, mock_input):
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Game over!", output)
        self.assertIn("Thanks for playing!", output)

    @patch('builtins.input', side_effect=['Bob', 'invalid', 'rock', 'paper', 'scissors'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_invalid_move_wastes_round(self, mock_stdout, mock_input):
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Invalid move", output)
        self.assertIn("invalid", output.lower())
        self.assertIn("round", output.lower())
        self.assertIn("Game over!", output)

if __name__ == '__main__':
    unittest.main()