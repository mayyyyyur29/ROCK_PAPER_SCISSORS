import random
import os
import google.generativeai as genai
from game_state import GameState
from adk_tools import validate_move, resolve_round, update_game_state

# Configure Google AI (API key should be set in environment)
# Option 1: Set environment variable GOOGLE_AI_API_KEY
# Option 2: Replace the string below with your actual API key
api_key = os.getenv('GOOGLE_AI_API_KEY') or "YOUR_API_KEY_HERE"
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

class Agent:
    def __init__(self):
        pass

    def parse_intent(self, user_input: str) -> str:
        prompt = f"""
        Analyze the user's input for a Rock-Paper-Scissors game and extract their move.
        Valid moves: rock, paper, scissors, bomb
        If no clear move, return 'invalid'
        
        User input: "{user_input}"
        
        Respond with only the move or 'invalid'.
        """
        try:
            response = model.generate_content(prompt)
            move = response.text.strip().lower()
            if move in ['rock', 'paper', 'scissors', 'bomb']:
                return move
            else:
                return 'invalid'
        except:
            # Fallback to simple parsing
            input_lower = user_input.lower()
            if 'rock' in input_lower:
                return 'rock'
            elif 'paper' in input_lower:
                return 'paper'
            elif 'scissors' in input_lower:
                return 'scissors'
            elif 'bomb' in input_lower:
                return 'bomb'
            else:
                return 'invalid'

    def handle_game_logic(self, state: GameState, user_move: str) -> tuple:
        if not validate_move(state, user_move, 'user'):
            update_game_state(state, 'invalid', user_move, None)
            return 'invalid', user_move, None
        bot_move = self.generate_bot_move(state)
        winner = resolve_round(user_move, bot_move)
        update_game_state(state, winner, user_move, bot_move)
        return winner, user_move, bot_move

    def generate_bot_move(self, state: GameState) -> str:
        prompt = f"""
        You are playing Rock-Paper-Scissors-Plus against a human.
        Rules: Rock beats Scissors, Scissors beats Paper, Paper beats Rock, Bomb beats everything.
        Bomb can only be used once per player.
        
        Current game state:
        Round: {state.round_number}/3
        Your score: {state.bot_score}
        Human score: {state.user_score}
        You have used bomb: {state.bot_bomb_used}
        Human has used bomb: {state.user_bomb_used}
        
        Choose the best move for you: rock, paper, scissors, or bomb (if available).
        Respond with only the move.
        """
        try:
            response = model.generate_content(prompt)
            move = response.text.strip().lower()
            if move in ['rock', 'paper', 'scissors'] or (move == 'bomb' and not state.bot_bomb_used):
                return move
            else:
                # Fallback to random
                moves = ['rock', 'paper', 'scissors']
                if not state.bot_bomb_used:
                    moves.append('bomb')
                return random.choice(moves)
        except:
            # Fallback to random
            moves = ['rock', 'paper', 'scissors']
            if not state.bot_bomb_used:
                moves.append('bomb')
            return random.choice(moves)

    def generate_response(self, state: GameState, winner: str, user_move: str, bot_move: str) -> str:
        if winner == 'invalid':
            responses = [
                f"Whoops! '{user_move}' isn't a valid move. That round's wasted, but let's keep the game rolling!",
                f"Oops! '{user_move}' doesn't count. Round forfeited, but don't let it rock your world!",
                f"Invalid move alert! '{user_move}' is out. Round wasted, but the game's still on!"
            ]
            response = random.choice(responses)
        else:
            if winner == 'tie':
                tie_responses = [
                    f"It's a tie! Both of you picked {user_move} - great minds think alike, or maybe just copycats!",
                    f"Draw! {user_move} vs {user_move} - a standoff that would make even the best strategists pause.",
                    f"Tie game! Both chose {user_move}. Looks like you and the bot are on the same wavelength!"
                ]
                response = random.choice(tie_responses)
            elif winner == 'user':
                win_responses = [
                    f"You win this round! {user_move.capitalize()} beats {bot_move} - you're really bringing the heat!",
                    f"Victory! Your {user_move} outsmarted the bot's {bot_move}. Rock on!",
                    f"You take the point! {user_move.capitalize()} triumphs over {bot_move} - strategy pays off!"
                ]
                response = random.choice(win_responses)
            else:
                lose_responses = [
                    f"Bot wins this round! {bot_move.capitalize()} beats {user_move} - even machines have their day.",
                    f"Bot takes it! {bot_move.capitalize()} over {user_move} - the bot's playing mind games now.",
                    f"Bot scores! {bot_move.capitalize()} defeats {user_move}. Next time, think like a computer!"
                ]
                response = random.choice(lose_responses)
            
            response += f"\nCurrent scores: You {state.user_score}, Bot {state.bot_score}"
            
            if not state.game_over:
                continue_responses = [
                    "Let's keep the momentum going!",
                    "Onward to the next round!",
                    "The game's heating up - your move!"
                ]
                response += f"\n{random.choice(continue_responses)}"
            
            if state.game_over:
                if state.user_score > state.bot_score:
                    end_responses = [
                        "Game over! Congratulations, you won the match! You're the champion!",
                        "Final whistle! You take the victory - rockstar performance!",
                        "Game over! You emerge triumphant. The bot bows to your skill!"
                    ]
                    response += f"\n{random.choice(end_responses)}"
                elif state.bot_score > state.user_score:
                    end_responses = [
                        "Game over! The bot takes the victory this time. Machines are learning!",
                        "Game over! Bot wins the match! Looks like the AI outsmarted the human today.",
                        "Game over! Bot claims victory. Next time, bring your A-game!"
                    ]
                    response += f"\n{random.choice(end_responses)}"
                else:
                    end_responses = [
                        "Game over! It's a perfect tie! A draw worthy of the ages.",
                        "Game over! Match ends in a tie! Both of you played brilliantly.",
                        "Game over! Perfect stalemate - neither could claim superiority!"
                    ]
                    response += f"\n{random.choice(end_responses)}"
        
        return response