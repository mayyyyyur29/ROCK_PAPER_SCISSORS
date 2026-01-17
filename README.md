# Rock-Paper-Scissors-Plus (ADK Version)

An interactive conversational agent built using Google's **Agent Development Kit (ADK)**. It referees a 3-round Rock-Paper-Scissors-Plus match with witty commentary and strategic moves. Powered by Gemini and written entirely in Python.

## 🌟 Features

* Natural-language move parsing ("I'll throw a rock!")
* Strategic bot moves (smart use of Bomb!)
* Fun, dynamic responses for each round
* Game state stored between turns (via ADK session state)
* Fully compatible with `adk web` and ADK Dev UI

---

## 🚀 Quick Start

```bash
pip install -r requirements.txt
adk web
```

Then open `http://127.0.0.1:8000` and launch the `rps_plus_referee` agent.

**Optional**: To use Gemini AI for smarter intent parsing or response generation:

```bash
export GOOGLE_API_KEY="your-key-here"
```

## ⚖️ Game Rules

* Rock beats Scissors
* Scissors beats Paper
* Paper beats Rock
* Bomb beats everything, but each player can only use it once
* Invalid moves waste the round
* Game lasts exactly 3 rounds

---

## 📊 State Model

The agent tracks game progress using ADK's session state:

```json
{
  "round": 1,
  "user_score": 0,
  "bot_score": 0,
  "user_bomb_used": false,
  "bot_bomb_used": false,
  "game_over": false
}
```

This keeps gameplay consistent and makes testing easy.

---

## 🧹 Agent Design

### Tools (inline in `agent.py`)

* `tool_parse_intent()` — Extracts move from user input
* `tool_validate_move()` — Validates move legality (e.g., bomb reuse)
* `tool_resolve_round()` — Applies RPS+ rules to determine round outcome
* `tool_update_game_state()` — Updates scores and flags based on the result
* `tool_generate_response()` — Builds human-friendly responses with variation

### Agent Callback Logic

Defined in `before_agent_callback()`:

* Initializes state if first message
* Parses user move
* Computes and validates bot move
* Resolves outcome
* Updates state
* Responds with rich commentary

Fallbacks are built-in:

* If input parsing fails, round is wasted but game continues
* If user types "restart" after game ends, state resets

---

## ⚖️ Tradeoffs & Design Decisions

* **No LLM calls by default** — Designed to be fully functional without API key
* **Simple game state only** — No conversation memory/history, just round-wise
* **Random response variety** — Adds fun and replayability
* **No external UI** — Uses ADK Dev UI for testing, easily extendable to web

---

## ✏️ What I'd Improve

* Add memory of full move history for smarter AI
* Improve bot strategy beyond random (e.g. Nash logic or pattern matching)
* Extend to a visual or web UI (Flask/Tailwind)
* Add stats tracking (wins, longest streak, bomb usage rate)
* Include unit tests for tool functions and mocked callbacks

---

## 🔗 Related

* Built with: [Google ADK](https://developers.generativeai.google/guide/adk)
* AI model (optional): Gemini Flash / Pro
* Format: One-agent file (`agent.py`) + `adk.yaml`

Enjoy the game, and may your bombs be well-timed!
