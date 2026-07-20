# hexbot_priapo

A [Hex](https://en.wikipedia.org/wiki/Hex_(board_game))-playing agent built around **Monte Carlo Tree Search with RAVE**, **virtual connections (bridges)** and **search-tree reuse**, written in pure Python.

It was originally developed for the Fundamentos de la Inteligencia Artificial course at Universidad de San Andrés, where student agents competed on 13×13 boards under a TrueSkill rating system, with a fixed time budget per move and a 500 MB memory cap (constraints that shaped most of the design decisions below). Competing as **Príapo**, it finished **🥉 3rd out of 83 agents** in the [final standings](#tournament-results). It was later refined for publication as a standalone project.

## Tournament results

The agent competed as **Príapo** and finished **3rd out of 83 agents** in the final TrueSkill standings, with **0% errors and 0% timeouts**, and using roughly **half the iteration time** of the two agents that finished above it.

| # | Agent | Rating (μ ± σ) | Iteration time | Errors | Timeouts |
|--:|:--|:--|--:|--:|--:|
| 🥇 1 | PerretAgent | 41.27 ± 1.32 | 27.8 s | 0.00% | 0.00% |
| 🥈 2 | AgenteCassanello | 40.96 ± 1.31 | 27.4 s | 0.00% | 4.76% |
| **🥉 3** | **Príapo** | **39.15 ± 1.27** | **15.0 s** | **0.00%** | **0.00%** |
| 4 | Hexconvicto | 38.95 ± 1.29 | 26.3 s | 0.00% | 0.00% |
| 5 | Rami Colapinto🏎️ v2.0 | 38.03 ± 1.28 | 27.5 s | 0.00% | 0.00% |
| 6 | etnL | 37.16 ± 1.29 | 21.6 s | 0.00% | 2.38% |
| 7 | 🤖SmartAgent | 37.13 ± 1.30 | 22.8 s | 0.00% | 0.00% |
| 8 | hombre aguja | 36.44 ± 1.30 | 28.8 s | 0.00% | 0.00% |
| 9 | Sheconquista | 35.64 ± 1.30 | 27.7 s | 0.00% | 0.00% |
| 10 | KirAgent | 35.52 ± 1.31 | 22.5 s | 0.00% | 0.00% |

<details>
<summary><b>Full standings (83 agents)</b></summary>

| # | Agent | Rating (μ ± σ) | Iteration time | Errors | Timeouts |
|--:|:--|:--|--:|--:|--:|
| 🥇 1 | PerretAgent | 41.27 ± 1.32 | 27.8 s | 0.00% | 0.00% |
| 🥈 2 | AgenteCassanello | 40.96 ± 1.31 | 27.4 s | 0.00% | 4.76% |
| **🥉 3** | **Príapo** | **39.15 ± 1.27** | **15.0 s** | **0.00%** | **0.00%** |
| 4 | Hexconvicto | 38.95 ± 1.29 | 26.3 s | 0.00% | 0.00% |
| 5 | Rami Colapinto🏎️ v2.0 | 38.03 ± 1.28 | 27.5 s | 0.00% | 0.00% |
| 6 | etnL | 37.16 ± 1.29 | 21.6 s | 0.00% | 2.38% |
| 7 | 🤖SmartAgent | 37.13 ± 1.30 | 22.8 s | 0.00% | 0.00% |
| 8 | hombre aguja | 36.44 ± 1.30 | 28.8 s | 0.00% | 0.00% |
| 9 | Sheconquista | 35.64 ± 1.30 | 27.7 s | 0.00% | 0.00% |
| 10 | KirAgent | 35.52 ± 1.31 | 22.5 s | 0.00% | 0.00% |
| 11 | LeAgent 🐐 | 35.10 ± 1.27 | 2.2 s | 2.38% | 0.00% |
| 12 | Yabot | 34.83 ± 1.29 | 20.0 s | 0.00% | 0.00% |
| 13 | Hextech Agent 2.0 | 34.38 ± 1.29 | 27.2 s | 0.00% | 0.00% |
| 14 | Wall-E🤖 | 33.33 ± 1.27 | 24.8 s | 0.00% | 0.00% |
| 15 | Turko 👽 | 32.84 ± 1.29 | 27.7 s | 0.00% | 0.00% |
| 16 | 🪸Maestro Alga🪸 | 32.62 ± 1.28 | 27.5 s | 0.00% | 0.00% |
| 17 | Jaz | 32.54 ± 1.27 | 29.0 s | 0.00% | 0.00% |
| 18 | 🐜 lacayo de Fede Pizarro 🐜 | 32.22 ± 1.29 | 18.2 s | 0.00% | 0.00% |
| 19 | 🕹️ DoorAgent | 31.98 ± 1.28 | 28.0 s | 0.00% | 0.00% |
| 20 | 🤖 Paranoid Android | 31.51 ± 1.29 | 19.1 s | 0.00% | 0.00% |
| 21 | 007Agent | 31.21 ± 1.29 | 29.0 s | 0.00% | 0.00% |
| 22 | 🪲Hex Jude (Remaster) | 31.10 ± 1.28 | 14.1 s | 0.00% | 0.00% |
| 23 | Caminito | 30.90 ± 1.28 | 13.7 s | 0.00% | 0.00% |
| 24 | El DiDi pistero de Gian | 30.68 ± 1.28 | 28.0 s | 0.00% | 0.00% |
| 25 | Clanker | 30.13 ± 1.28 | 26.0 s | 0.00% | 0.00% |
| 26 | 🐙Jugador 456 | 29.92 ± 1.28 | 4.5 s | 0.00% | 0.00% |
| 27 | Kowalski | 29.58 ± 1.27 | 12.5 s | 0.00% | 0.00% |
| 28 | R2-D2 🚀 | 29.46 ± 1.30 | 26.9 s | 0.00% | 0.00% |
| 29 | Teenager | 29.27 ± 1.29 | 29.1 s | 0.00% | 0.00% |
| 30 | 🦦 Agente P v3 | 29.05 ± 1.26 | 27.2 s | 0.00% | 9.52% |
| 31 | CardelliAgent | 28.84 ± 1.29 | 28.0 s | 0.00% | 0.00% |
| 32 | ClickAgent 2.0 | 28.53 ± 1.27 | 28.1 s | 0.00% | 0.00% |
| 33 | Piñatomico | 27.97 ± 1.28 | 25.0 s | 0.00% | 0.00% |
| 34 | Terminator | 27.98 ± 1.29 | 29.0 s | 0.00% | 0.00% |
| 35 | MyAgent | 27.86 ± 1.28 | 29.0 s | 0.00% | 0.00% |
| 36 | CasasAgent | 27.73 ± 1.28 | 14.6 s | 0.00% | 0.00% |
| 37 | agentBeta | 27.28 ± 1.27 | 187.45 ms | 0.00% | 0.00% |
| 38 | Ginés | 27.18 ± 1.28 | 29.0 s | 0.00% | 0.00% |
| – | ZuberbuhlerAgent | 26.71 ± 2.43 | 19.5 s | 0.00% | 0.00% |
| 39 | Botti 👹👹👹 | 26.66 ± 1.29 | 27.0 s | 0.00% | 0.00% |
| 40 | O⬡ hexGoat ⬡O | 26.56 ± 1.29 | 24.6 s | 0.00% | 0.00% |
| 41 | Pardoval | 26.37 ± 1.29 | 25.3 s | 0.00% | 2.38% |
| 42 | AlphaMathiK | 26.21 ± 1.29 | 26.7 s | 0.00% | 0.00% |
| 43 | Alejandrito | 26.09 ± 1.29 | 1.2 s | 0.00% | 0.00% |
| 44 | Andex__agent | 25.09 ± 1.29 | 25.0 s | 0.00% | 0.00% |
| 45 | AlphaHex | 24.59 ± 1.31 | 27.0 s | 0.00% | 0.00% |
| 46 | Inés | 24.33 ± 1.28 | 25.5 s | 0.00% | 14.29% |
| 47 | persi | 24.30 ± 1.30 | 28.1 s | 0.00% | 0.00% |
| 48 | 😊Hexterminator | 23.70 ± 1.28 | 17.0 s | 0.00% | 0.00% |
| 49 | anALPHABETO | 23.61 ± 1.29 | 2.2 s | 0.00% | 0.00% |
| 50 | Curacautin3.3.3 36346 | 23.58 ± 1.29 | 29.3 s | 0.00% | 0.00% |
| 51 | 🐸FC43 | 22.83 ± 1.29 | 22.6 s | 0.00% | 0.00% |
| 52 | Pepito | 22.78 ± 1.30 | 427.14 ms | 0.00% | 0.00% |
| 53 | HexaShus | 22.71 ± 1.28 | 4.2 s | 0.00% | 0.00% |
| 54 | 🎭CastañosZemborain | 21.84 ± 1.30 | 14.3 s | 0.00% | 0.00% |
| 55 | 🐻AgenteOsoRAVE | 21.72 ± 1.29 | 10.3 s | 0.00% | 0.00% |
| 56 | ❤️ Agente Martu | 21.65 ± 1.30 | 18.7 s | 0.00% | 0.00% |
| 57 | 🏎️BoxBox | 21.62 ± 1.29 | 11.8 s | 0.00% | 0.00% |
| 58 | Patruno_Agent | 21.35 ± 1.28 | 22.4 s | 0.00% | 0.00% |
| 59 | 🎀Dai | 21.04 ± 1.30 | 4.7 s | 0.00% | 0.00% |
| – | The Goat🐐 | 21.04 ± 4.17 | 11.8 s | 0.00% | 0.00% |
| 60 | Everdeen | 20.48 ± 1.30 | 22.6 s | 0.00% | 0.00% |
| 61 | 💐juaa76cool 36803 | 19.94 ± 1.30 | 1.9 s | 0.00% | 0.00% |
| 62 | ✨Hexpecto Patronum | 19.74 ± 1.29 | 21.8 s | 0.00% | 0.00% |
| 63 | Lucía Agent | 19.52 ± 1.30 | 7.0 s | 0.00% | 0.00% |
| 64 | SaloGrande 34610 | 19.11 ± 1.28 | 28.0 s | 0.00% | 0.00% |
| 65 | 🧠 AlphaGoat | 18.78 ± 1.30 | 7.8 s | 0.00% | 0.00% |
| 66 | Larigod | 18.56 ± 1.30 | 27.7 s | 0.00% | 0.00% |
| 67 | 🍕 Piza | 17.89 ± 1.27 | 12.9 s | 0.00% | 0.00% |
| 68 | bIAnca | 17.77 ± 1.29 | 23.5 s | 0.00% | 0.00% |
| 69 | 🥥Half | 17.54 ± 1.28 | 0.03 ms | 0.00% | 0.00% |
| 70 | 🤖SmartAgent1 | 17.06 ± 1.30 | 15.11 ms | 0.00% | 0.00% |
| 71 | 🦋El Viaje de CHIHIRO ガイア | 17.00 ± 1.34 | 1.9 s | 0.00% | 0.00% |
| 72 | Faker | 16.91 ± 1.31 | 25.1 s | 0.00% | 0.00% |
| – | Greek Agent | 16.37 ± 2.46 | 28.2 s | 0.00% | 0.00% |
| 73 | Montecarleano | 15.83 ± 1.30 | 29.0 s | 0.00% | 0.00% |
| 74 | 🥇First | 15.69 ± 1.32 | 0.08 ms | 0.00% | 0.00% |
| 75 | AgenteCheckpoint | 14.41 ± 1.12 | 340.30 ms | 0.00% | 0.00% |
| 76 | 🧙💍🧒⛰️u shall not pass🧝🏰🌋 | 12.98 ± 1.31 | 1.46 ms | 0.00% | 0.00% |
| 77 | 🥽Antifaz | 12.91 ± 1.29 | 0.50 ms | 0.00% | 0.00% |
| 78 | 🎲LuckyAgent 35720 | 12.09 ± 1.10 | 5.8 s | 0.00% | 0.00% |
| 79 | 🎭Adjacent | 11.90 ± 1.29 | 0.29 ms | 0.00% | 0.00% |
| 80 | Foiler | 10.55 ± 1.36 | 804.84 ms | 0.00% | 0.00% |
| 81 | 🎯Center | 7.43 ± 1.35 | 0.17 ms | 0.00% | 0.00% |
| 82 | ❌ | 6.92 ± 1.46 | 0.03 ms | 0.00% | 0.00% |
| 83 | 🎲Randall_M 2982 | 3.99 ± 1.58 | 0.08 ms | 0.00% | 0.00% |

</details>

## How it works

The agent always sees itself as player `+1`, connecting the **left and right** edges (the runner transposes the board for the second player, a convention inherited from the tournament harness).

### MCTS + RAVE

The core is a time-bounded MCTS loop (selection / expansion / simulation / backpropagation). Plain UCT is slow to converge on Hex's large branching factor, so node selection blends the classic UCT score with **RAVE/AMAF** (all-moves-as-first) statistics, using the MoHex-style formula:

```
score = (1 - w) · (Q + c·√(ln N / n))  +  w · Q_RAVE,      w = n_rave / (n_rave + n)
```

RAVE credits every cell played by the side to move anywhere inside a winning simulation, giving early, low-variance (if biased) estimates; the weight `w` fades RAVE out as real visit counts accumulate. RAVE counters are seeded with small pseudo-counts (8 visits / 4 wins, values from the MoHex paper) to smooth out early noise.

### O(~1) win detection with Union-Find

Every stone is unioned with its same-colored neighbors and with virtual edge nodes, so checking "did this player win?" costs two `find` operations instead of a graph traversal. Since MCTS runs thousands of rollouts per move and each rollout checks for a win after every stone, this is the single most performance-critical structure in the project.

The Union-Find is also memory-optimized: parent/rank tables live in compact `array('H')` / `array('B')` buffers rather than Python lists, which cut the agent's memory footprint by roughly an order of magnitude (early list-based versions blew through the tournament's 500 MB cap).

### Virtual connections (bridges)

A *bridge* is the classic two-cell Hex template: two stones that are not adjacent but cannot be disconnected, because for each of the two empty "critical" cells the owner can always answer an intrusion by taking the other. The agent exploits bridges in two ways:

- **Early rollout termination**: a second, *virtual* Union-Find additionally unions bridged stones. Rollouts stop as soon as a player is virtually connected, making simulations shorter and the search noticeably stronger for the same time budget.
- **Deterministic defense**: bridges formed by the agent on the real board are stored, and if the opponent plays into a critical cell, the agent instantly answers with the sister cell without spending any search time. The saved time budget is still used: the agent runs the search anyway to grow the tree for future turns.

### Tree reuse

Between turns the root of the search tree is advanced along the moves actually played (by either side), so statistics gathered on previous turns keep working. Combined with the "enrich the tree during forced replies" trick above, the agent often starts a turn with a substantial tree already built.

### Design trade-offs

- **Overlapping bridges are discarded** (first detected wins). Handling overlaps exactly would require rebuilding the virtual Union-Find on each collision; the rare sub-optimal forced defense is a price worth paying.
- **Virtual unions are never undone**, so a rollout can end on a "virtual win" whose critical cells were occupied later in that same rollout. This is a standard approximation: the affected player could have answered each intrusion when it happened.
- **Once the agent is virtually connected**, every rollout ends instantly in a win and the search can no longer differentiate moves — so the virtual structure (and the tree built on it) is reset, forcing MCTS to find the concrete winning sequence.
- **2-byte RAVE counters** (`array('H')`) keep per-node memory small; within realistic time budgets they never saturate, and backpropagation clamps them just in case.

## Installation

```bash
git clone https://github.com/BarralMaximo/hexbot_priapo.git
cd hexbot_priapo
pip install -e .          # or: pip install -e ".[dev]" to run the tests
```

## Usage

Watch the agent beat a random player, play against it, or make it play itself:

```bash
python examples/play.py --opponent random --size 9 --time 2
python examples/play.py --opponent human --size 7 --time 3
python examples/play.py --opponent self --size 9 --time 1
```

Or use it as a library:

```python
import numpy as np
from hex_mcts import MCTSAgent, RandomAgent, play_match

agent = MCTSAgent(board_size=9, time_limit=2.0)
winner = play_match(agent, RandomAgent(), size=9, verbose=True)

# Lower-level: ask for a move on any position (agent is +1, left-right)
board = np.zeros((9, 9), dtype=int)
move = agent.action(board)          # flat index: row * 9 + col
```

## Tests

```bash
pytest
```

The suite covers the Union-Find, board rules and win detection, bridge detection/defense, and end-to-end agent behavior (legal play, forced bridge answers, beating a random baseline).

## Project structure

```
hex_mcts/
├── agent.py        # MCTSAgent: turn orchestration, bridge defense, tree reuse
├── mcts.py         # MCTS engine + tree nodes with RAVE statistics
├── board.py        # Board rules, Union-Find win detection, bridge templates
├── union_find.py   # Memory-compact DSU (union by rank + path compression)
└── match.py        # Standalone match runner + ASCII rendering
examples/play.py    # CLI: agent vs random / human / itself
tests/              # pytest suite
```

## References

- Arneson, Hayward & Henderson — *Monte Carlo Tree Search in Hex* (IEEE T-CIAIG, 2010): MoHex, RAVE weighting and prior values.
- Gelly & Silver — *Monte-Carlo tree search and rapid action value estimation in computer Go* (Artificial Intelligence, 2011): RAVE/AMAF.
