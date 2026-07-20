import random
import numpy as np

from .board import HexBoard

class RandomAgent:
    def action(self, board) -> int:
        empties = np.flatnonzero(board.ravel() == 0)
        return int(random.choice(empties))

    def reset(self) -> None: pass

    def __str__(self) -> str: return "random"

def render(board) -> str:
    """ASCII rendering of a board. ``X`` is +1 (left-right), ``O`` is -1
    (top-bottom); rows are offset to suggest the hex geometry."""
    n = board.shape[0]
    symbols = {0: ".", 1: "X", -1: "O"}
    header = "   " + " ".join(f"{c:2d}" for c in range(n))
    lines = [header]

    for r in range(n):
        offset = " " * r
        cells = "  ".join(symbols[int(v)] for v in board[r])
        lines.append(f"{offset}{r:2d}  {cells}")

    return "\n".join(lines)

def play_match(agent1, agent2, size: int = 13, verbose: bool = False):
    """Play one game between two agents; returns the winner (1 or 2).

    ``agent1`` plays first as +1 (left-right in real coordinates). ``agent2``
    receives the transposed, sign-flipped board so it also sees itself as +1.
    An illegal move forfeits the game.
    """
    referee = HexBoard(size)
    board = np.zeros((size, size), dtype=int)
    current = 1

    while True:
        mover = agent1 if current == 1 else agent2
        obs = board.copy() if current == 1 else (board.T * -1).copy()

        action = mover.action(obs)
        r, c = divmod(int(action), size)
        if current == -1: r, c = c, r  # back to real coordinates

        if not (0 <= r < size and 0 <= c < size) or board[r, c] != 0:
            if verbose: print(f"Illegal move {(r, c)} by {mover} — forfeits.")
            return 2 if current == 1 else 1

        board[r, c] = current
        referee.place(r, c, current, simulation=False)

        if verbose:
            print(f"\n{mover} plays {(r, c)}")
            print(render(board))

        if referee.check_win(current):
            return 1 if current == 1 else 2

        current = -current