"""Play against the agent, or watch it play, from the terminal.

Examples:
    python examples/play.py --opponent random --size 9 --time 2
    python examples/play.py --opponent human --size 7 --time 3
    python examples/play.py --opponent self --size 9 --time 1
"""

import argparse
from hex_mcts import MCTSAgent, RandomAgent, play_match, render

class HumanAgent:
    """Reads moves from stdin as ``row col``. You are X (left to right)."""

    def action(self, board) -> int:
        n = board.shape[0]
        print(render(board))
        while True:
            raw = input("Your move (row col): ").split()
            try:
                r, c = int(raw[0]), int(raw[1])
                if 0 <= r < n and 0 <= c < n and board[r, c] == 0: return r * n + c
            except (ValueError, IndexError):
                pass
            print("Invalid move, try again.")

    def reset(self) -> None:
        pass

    def __str__(self) -> str:
        return "human"

def main():
    parser = argparse.ArgumentParser(description="Play Hex against the MCTS agent.")
    parser.add_argument("--size", type=int, default=9, help="board side (default 9)")
    parser.add_argument("--time", type=float, default=2.0, help="agent seconds per move")
    parser.add_argument("--opponent", choices=["random", "human", "self"], default="random", help="who plays against the agent")
    parser.add_argument("--agent-second", action="store_true", help="let the opponent move first")
    args = parser.parse_args()

    agent = MCTSAgent(board_size=args.size, time_limit=args.time)
    if args.opponent == "random": opponent = RandomAgent()
    elif args.opponent == "human": opponent = HumanAgent()
    else: opponent = MCTSAgent(board_size=args.size, time_limit=args.time)

    if args.agent_second:
        first, second = opponent, agent
    else:
        first, second = agent, opponent

    winner = play_match(first, second, size=args.size, verbose=True)
    print(f"\n{first if winner == 1 else second} wins!")

if __name__ == "__main__":
    main()