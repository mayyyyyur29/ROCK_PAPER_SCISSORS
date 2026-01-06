import unittest
from game_state import GameState
from adk_tools import validate_move, resolve_round, update_game_state

class TestGame(unittest.TestCase):
    def test_resolve_round(self):
        self.assertEqual(resolve_round('rock', 'scissors'), 'user')
        self.assertEqual(resolve_round('bomb', 'rock'), 'user')
        self.assertEqual(resolve_round('rock', 'bomb'), 'bot')
        self.assertEqual(resolve_round('rock', 'rock'), 'tie')

    def test_validate_move(self):
        state = GameState()
        self.assertTrue(validate_move(state, 'rock', 'user'))
        self.assertTrue(validate_move(state, 'bomb', 'user'))
        state.user_bomb_used = True
        self.assertFalse(validate_move(state, 'bomb', 'user'))

    def test_update_game_state(self):
        state = GameState()
        update_game_state(state, 'user', 'rock', 'scissors')
        self.assertEqual(state.user_score, 1)
        self.assertEqual(state.round_number, 2)
        update_game_state(state, 'bot', 'rock', 'bomb')
        self.assertEqual(state.bot_score, 1)
        self.assertTrue(state.bot_bomb_used)
        self.assertEqual(state.round_number, 3)
        update_game_state(state, 'tie', 'rock', 'rock')
        self.assertEqual(state.round_number, 4)
        self.assertTrue(state.game_over)

if __name__ == '__main__':
    unittest.main()