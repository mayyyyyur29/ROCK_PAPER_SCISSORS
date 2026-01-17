from google.adk.agents.llm_agent import Agent
from google.adk.agents.callback_context import CallbackContext
from google.genai import types
import random

def tool_parse_intent(user_input: str) -> str:
    """Extracts the move keyword from user input."""
    text = user_input.strip().lower()
    if "restart" in text:
        return "restart"
    if "rock" in text:
        return "rock"
    if "paper" in text:
        return "paper"
    if "scissor" in text:
        return "scissors"
    if "bomb" in text:
        return "bomb"
    return ""

def tool_validate_move(move: str, state: dict) -> bool:
    """Checks move validity and bomb usage rules for the user."""
    valid_moves = {"rock", "paper", "scissors", "bomb"}
    if move not in valid_moves:
        return False
    if move == "bomb" and state.get("user_bomb_used", False):
        return False
    return True

def tool_generate_bot_move(state: dict) -> str:
    """Chooses the bot's move, considering its bomb usage."""
    moves = ["rock", "paper", "scissors"]
    if not state.get("bot_bomb_used", False):
        moves.append("bomb")
    return random.choice(moves)

def tool_resolve_round(user_move: str, bot_move: str) -> str:
    """Determines the round result: 'user', 'bot', or 'tie'."""
    if user_move == bot_move:
        return "tie"
    if user_move == "bomb" and bot_move != "bomb":
        return "user"
    if bot_move == "bomb" and user_move != "bomb":
        return "bot"
    wins = {("rock", "scissors"), ("scissors", "paper"), ("paper", "rock")}
    if (user_move, bot_move) in wins:
        return "user"
    if (bot_move, user_move) in wins:
        return "bot"
    return "tie"

def tool_update_game_state(state: dict, user_move: str, bot_move: str, winner: str):
    """Updates scores, bomb flags, and round count in state."""
    if user_move == "bomb":
        state["user_bomb_used"] = True
    if bot_move == "bomb":
        state["bot_bomb_used"] = True
    if winner == "user":
        state["user_score"] = state.get("user_score", 0) + 1
    elif winner == "bot":
        state["bot_score"] = state.get("bot_score", 0) + 1
    # Advance to next round
    state["round"] = state.get("round", 0) + 1
    if state["round"] > 3:
        state["game_over"] = True

def tool_generate_response(state: dict, user_move: str, bot_move: str, winner: str) -> str:
    """Generates the response message for the round or end of game."""
    round_num = state.get("round", 0) - 1
    if round_num < 1:
        round_num = 1
    user_score = state.get("user_score", 0)
    bot_score = state.get("bot_score", 0)
    if not tool_validate_move(user_move, state):
        return f"Round {round_num}: Invalid move! You wasted this round.\nScore: You {user_score}, Bot {bot_score}."
    if winner == "tie":
        if user_move == bot_move:
            if user_move == "bomb":
                result_msg = "Both used Bomb! It's a tie."
            else:
                result_msg = f"Both chose {user_move.capitalize()}. It's a tie."
        else:
            result_msg = "It's a tie."
        return f"Round {round_num}: {result_msg}\nScore: You {user_score}, Bot {bot_score}."
    def cap(m): return m.capitalize() if m else m
    round_msg = f"Round {round_num}: You chose {cap(user_move)}, I chose {cap(bot_move)}. "
    if winner == "user":
        round_msg += "You win this round!"
    elif winner == "bot":
        round_msg += "I win this round!"
    return f"{round_msg}\nScore: You {user_score}, Bot {bot_score}."

def before_agent_callback(callback_context: CallbackContext):
    state = callback_context.state
    user_content = callback_context.user_content
    user_text = ""
    if user_content and user_content.parts:
        user_text = user_content.parts[0].text.strip()
    # First interaction: show game rules
    if not state.get("round"):
        state["round"] = 1
        state["user_score"] = 0
        state["bot_score"] = 0
        state["user_bomb_used"] = False
        state["bot_bomb_used"] = False
        state["game_over"] = False
        rules = (
            "Welcome to Rock-Paper-Scissors-Plus!\n"
            "Rules:\n"
            "- Valid moves: rock, paper, scissors, bomb.\n"
            "- Rock beats Scissors, Scissors beats Paper, Paper beats Rock.\n"
            "- Bomb beats everything but can be used only once per player.\n"
            "- Invalid moves waste the round (and still count).\n"
            "Let's play 3 rounds. What's your move?"
        )
        return types.Content(role="assistant", parts=[types.Part(text=rules)])
    # If game has ended
    if state.get("game_over"):
        if user_text.lower() == "restart":
            state["round"] = 1
            state["user_score"] = 0
            state["bot_score"] = 0
            state["user_bomb_used"] = False
            state["bot_bomb_used"] = False
            state["game_over"] = False
            rules = (
                "Game restarted. Rock-Paper-Scissors-Plus!\n"
                "Rules:\n"
                "- Valid moves: rock, paper, scissors, bomb.\n"
                "- Rock beats Scissors, Scissors beats Paper, Paper beats Rock.\n"
                "- Bomb beats everything but can be used only once per player.\n"
                "- Invalid moves waste the round (and still count).\n"
                "Let's play 3 rounds. What's your move?"
            )
            return types.Content(role="assistant", parts=[types.Part(text=rules)])
        else:
            message = "Game over. To play again, type 'restart'."
            return types.Content(role="assistant", parts=[types.Part(text=message)])
    # Otherwise, process the user's move
    move = tool_parse_intent(user_text)
    valid = tool_validate_move(move, state)
    if not valid:
        bot_move = tool_generate_bot_move(state)
        state["round"] += 1
        if state["round"] > 3:
            state["game_over"] = True
        resp = f"Round {state['round']-1}: Invalid move! You wasted this round.\n"
        resp += f"Score: You {state['user_score']}, Bot {state['bot_score']}."
        if state["game_over"]:
            resp += f"\nGame over! Final Score: You {state['user_score']}, Bot {state['bot_score']}. "
            if state['user_score'] > state['bot_score']:
                resp += "You win the game!"
            elif state['user_score'] < state['bot_score']:
                resp += "I win the game!"
            else:
                resp += "It's a tie!"
            resp += " To play again, type 'restart'."
        return types.Content(role="assistant", parts=[types.Part(text=resp)])
    bot_move = tool_generate_bot_move(state)
    winner = tool_resolve_round(move, bot_move)
    tool_update_game_state(state, move, bot_move, winner)
    resp = tool_generate_response(state, move, bot_move, winner)
    if state.get("game_over"):
        final = f"\nGame over! Final Score: You {state['user_score']}, Bot {state['bot_score']}. "
        if state['user_score'] > state['bot_score']:
            final += "You win the game!"
        elif state['user_score'] < state['bot_score']:
            final += "I win the game!"
        else:
            final += "It's a tie!"
        final += " To play again, type 'restart'."
        resp += final
    return types.Content(role="assistant", parts=[types.Part(text=resp)])

root_agent = Agent(
    model="gemini-3.5-base",
    name="rps_plus_referee",
    description="A referee for a Rock-Paper-Scissors-Plus game.",
    instruction=(
        "You are a Rock-Paper-Scissors-Plus game referee. "
        "Respond to the user's moves according to the game rules."
    ),
    before_agent_callback=before_agent_callback,
)
