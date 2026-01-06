from game_state import GameState
from agent import Agent

def explain_rules():
    print("ENTER GOOGLE API KEY FOR BETTER EXPERIENCE")
    print("Welcome to Rock-Paper-Scissors-Plus!")
    print("Rules:")
    print("- Rock beats Scissors, Scissors beats Paper, Paper beats Rock")
    print("- Bomb beats everything, but can only be used once per player")
    print("- Invalid moves waste the round")
    print("- Game lasts exactly 3 rounds")
    print("Let's play!")

def main():
    state = GameState()
    agent = Agent()
    explain_rules()
    username = input("Enter your name: ")
    while not state.game_over:
        user_input = input(f"Round {state.round_number}: {username}, your move (rock/paper/scissors/bomb): ")
        user_move = agent.parse_intent(user_input)
        winner, user_move, bot_move = agent.handle_game_logic(state, user_move)
        response = agent.generate_response(state, winner, user_move, bot_move)
        print(response)
    print("Thanks for playing!")

if __name__ == "__main__":
    main()