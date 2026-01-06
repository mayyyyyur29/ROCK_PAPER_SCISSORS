# Rock-Paper-Scissors-Plus AI Referee

A Python chatbot that referees Rock-Paper-Scissors-Plus games using Google's Gemini AI. It's got personality, makes jokes, and occasionally outsmarts you.

## Quick Start

```bash
pip install -r requirements.txt
export GOOGLE_AI_API_KEY="your-key-here"  # optional but recommended
python main.py
```

**Game Rules**: Rock > Scissors > Paper > Rock. Bomb beats everything but you only get one. 3 rounds, most points wins.

---

## State Model

The `GameState` class tracks everything in one place:
- Round number (1-3)
- Scores for user and bot
- Bomb usage flags (one per player)
- Game over status

This centralized state makes the game logic predictable and easy to test. Every tool function takes state as input and returns updated state, keeping things functional and avoiding hidden mutations.

## Agent & Tool Design

### Tools (`adk_tools.py`)
Three pure functions handle game mechanics:
- `validate_move()` - Checks if a move is legal (mainly bomb usage)
- `resolve_round()` - Determines round winner based on rules
- `update_game_state()` - Returns new state after a round

Clean separation means I can test game logic without touching the AI.

### Agent (`agent.py`)
The agent wraps Google's Gemini AI for three things:

1. **Intent Parsing** - Understands "throw a rock" or "I choose paper" instead of requiring exact keywords. Falls back to simple string matching if AI is down.

2. **Strategic Bot Moves** - AI analyzes game state (scores, bomb usage, round number) to pick smart moves instead of random ones. Falls back to random selection when needed.

3. **Conversational Responses** - Generates witty, context-aware commentary. Falls back to basic templates without AI.

The fallback architecture means the game works even without an API key - you just lose the personality and strategy.

## Tradeoffs

**Added Google AI dependency** - Better gameplay and conversation, but requires API key and internet. I kept fallback logic so it still works offline, just less interesting.

**Random response variation** - Using random selection from AI-generated responses for replayability instead of deterministic output. Could be more sophisticated with conversation history.

**Simple state model** - No conversation memory or history tracking. Each interaction is stateless except for game state. Keeps it simple but limits contextual awareness.

**More conversational **-added small jokes or banter in between the replies to make conversation more intresting.


## What I'd Improve

**Conversation memory** - Track full conversation history to make AI responses more contextually aware instead of treating each turn independently.

**Better strategy** - Right now the bot just asks AI for a move. Could implement actual game theory (Nash equilibrium mixed strategies, pattern detection in user behavior).

**Web interface** - Terminal is fine but a simple Flask app would be more accessible and could show game history visually.

**Persistent stats** - Track win rates, favorite moves, longest streaks across sessions. Would make it feel more like a real game.

**Tests for AI components** - Current tests only cover deterministic game logic. Could mock AI responses to test parsing and response generation.
