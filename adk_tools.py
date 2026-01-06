from game_state import GameState

def validate_move(state: GameState, move: str, player: str) -> bool:
    valid_moves = ['rock', 'paper', 'scissors', 'bomb']
    if move not in valid_moves:
        return False
    if move == 'bomb':
        if player == 'user' and state.user_bomb_used:
            return False
        if player == 'bot' and state.bot_bomb_used:
            return False
    return True

def resolve_round(user_move: str, bot_move: str) -> str:
    if user_move == bot_move:
        return 'tie'
    if user_move == 'bomb':
        return 'user'
    if bot_move == 'bomb':
        return 'bot'
    # standard rps
    rules = {'rock': 'scissors', 'scissors': 'paper', 'paper': 'rock'}
    if rules[user_move] == bot_move:
        return 'user'
    else:
        return 'bot'

def update_game_state(state: GameState, winner: str, user_move: str, bot_move: str):
    if winner == 'user':
        state.user_score += 1
    elif winner == 'bot':
        state.bot_score += 1
    if user_move == 'bomb':
        state.user_bomb_used = True
    if bot_move and bot_move == 'bomb':
        state.bot_bomb_used = True
    state.round_number += 1
    if state.round_number > 3:
        state.game_over = True