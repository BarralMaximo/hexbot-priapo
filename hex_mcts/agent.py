import numpy as np

from .board import HexBoard
from .mcts import MCTS, Node
from .union_find import UnionFind

class MCTSAgent:
    """Hex agent combining MCTS/RAVE search with deterministic bridge defense.

    Board convention (inherited from the tournament harness this agent was
    built for): the agent always sees itself as player ``+1`` connecting the
    **left and right** edges. When the agent plays second, the runner must
    present it a transposed and sign-flipped board (see ``hex_mcts.match``).

    Per move, the agent:

    1. Diffs the incoming board against its internal one to find the
       opponent's move (``apply_delta``) and advances the search-tree root so
       previous search effort is reused.
    2. If the opponent's move intrudes into one of the agent's bridges,
       answers with the sister cell immediately — and spends the move's time
       budget enriching the search tree for future turns.
    3. Otherwise runs time-bounded MCTS from the (possibly reused) root.

    Args:
        board_size: expected board side; the agent re-adapts automatically if
            the first observed board has a different size.
        time_limit: seconds of search per move.
    """

    def __init__(self, board_size: int = 13, time_limit: float = 5.0):
        self.n = board_size
        self.t = time_limit
        self.first_call = True

        self.board = HexBoard(board_size, track_bridges=True)
        self.engine = MCTS()
        self.root = None

    def advance_root(self, move) -> None:
        """Move the tree root to the child reached by ``move``, if explored.

        This is what makes search effort reusable across turns: statistics
        gathered for the subtree of the move actually played (by either side)
        carry over. If the move was never expanded, the tree is dropped.
        """
        if self.root and move in self.root.children:
            self.root = self.root.children[move]
            self.root.parent = None
        else:
            self.root = None

    def apply_delta(self, env_board):
        """Sync the internal board with the environment's board.

        Finds the opponent's last move as the single differing cell (a fast
        NumPy diff), applies it internally and advances the root.

        Returns:
            ``(row, col, response)`` where ``response`` is the forced bridge
            defense if the move intrudes into one of our bridges (else
            ``None``); or ``None`` when no single new move is found (first
            move of the game).
        """
        n = env_board.shape[0]
        internal = self.board.board
        diff = np.flatnonzero(env_board.ravel() != internal.ravel())

        if diff.size == 1:
            i = int(diff[0])
            f, c = divmod(i, n)
            if internal[f, c] == 0 and env_board[f, c] != 0:
                resp = self.board.bridge_response(f, c)
                self.board.place(f, c, int(env_board[f, c]), simulation=False)
                self.advance_root((f, c))
                return (f, c, resp)
        return None

    def action(self, board) -> int:
        """Return the move to play as a flat index (``row * n + col``).

        ``board`` is the current position as an ``(n, n)`` ndarray with the
        agent's stones as ``+1``.
        """
        if self.first_call:
            if board.shape[0] != self.n:
                self.n = board.shape[0]
                self.board = HexBoard(self.n, track_bridges=True)
                self.engine = MCTS()
            self.first_call = False

        last_move = self.apply_delta(board)

        if last_move:
            f, c, resp = last_move
            if resp:
                # The opponent intruded into one of our bridges: the sister
                # cell restores the connection and is answered without search.
                ff, cf = resp
                self.board.place(ff, cf, self.board.current_player, simulation=False)
                self.advance_root((ff, cf))

                # Spend this turn's budget growing the tree for later reuse.
                if self.root is None: self.root = Node(self.board.copy())
                self.engine.search(self.board, root=self.root, t_limit=self.t)

                return ff * self.n + cf

        # Once we are *virtually* connected, every rollout ends instantly in a
        # "win", which would stop the search from telling moves apart. Reset
        # the virtual structure (and the tree built on top of it) so MCTS is
        # forced to find the concrete winning connection.
        if self.board.uf1_virtual.connected(self.board.left, self.board.right):
            self.board.uf1_virtual = UnionFind(self.n * self.n + 2)
            self.root = None

        f, c = self.engine.search(self.board, root=self.root, t_limit=self.t)

        self.advance_root((f, c))
        self.board.place(f, c, self.board.current_player, simulation=False)
        return f * self.n + c

    def reset(self) -> None:
        """Forget the current game (board and search tree)."""
        self.first_call = True
        self.board = HexBoard(self.n, track_bridges=True)
        self.engine = MCTS()
        self.root = None

    def __str__(self) -> str:
        return "hexbot_priapo"