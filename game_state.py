class GameState:
    def __init__(self):
        self.round_number = 1
        self.user_score = 0
        self.bot_score = 0
        self.user_bomb_used = False
        self.bot_bomb_used = False
        self.game_over = False