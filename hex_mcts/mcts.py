import math
import random
import time

from array import array

# RAVE statistics are stored in 2-byte unsigned arrays. Within the agent's
# time budgets a single cell never accumulates anywhere near 65535 visits
# (it was only reachable in stress tests on tiny boards with huge budgets),
# but the backpropagation still clamps to be safe.
_RAVE_MAX = 65535

class Node:
    """A node of the MCTS tree.

    ``player`` is the player who made ``move`` to reach this node, so
    ``wins / n_visits`` estimates the value of ``move`` for that player.

    RAVE/AMAF statistics are stored *in the parent's perspective* as flat
    arrays indexed by cell (``row * n + col``): ``rave_visits[p]`` counts how
    often cell ``p`` was played (by the player to move at this node) anywhere
    inside a simulation that passed through this node, and ``rave_wins[p]``
    how often those simulations were won. Flat ``array('H')`` buffers keep the
    per-node memory footprint small.
    """

    __slots__ = ("board", "parent", "children", "move", "player", "n_visits", "wins", "untried_moves", "rave_visits", "rave_wins")

    RAVE_PRIOR_VISITS = 8 # Pseudo-counts smoothing early RAVE noise,
    RAVE_PRIOR_WINS = 4 # values taken from the MoHex paper.

    def __init__(self, hexboard, parent=None, move=None, player=None):
        self.board = hexboard
        self.parent = parent
        self.children = {}
        self.move = move
        self.player = player
        self.n_visits = 0
        self.wins = 0

        self.untried_moves = hexboard.get_moves()
        random.shuffle(self.untried_moves)

        n = hexboard.n
        self.rave_visits = array("H", (0 for _ in range(n * n)))
        self.rave_wins = array("H", (0 for _ in range(n * n)))

        for (f, c) in self.untried_moves:
            p = f * n + c
            self.rave_visits[p] = self.RAVE_PRIOR_VISITS
            self.rave_wins[p] = self.RAVE_PRIOR_WINS

    def best_child(self, c: float):
        """Select a child maximizing the MoHex-style UCT-RAVE blend:

        ``score = (1 - w) * (Q + exploration) + w * Q_rave``

        where ``w = rave_visits / (rave_visits + visits)`` fades the RAVE
        estimate out as real visits accumulate.
        """
        if not self.children:
            return None

        # Local binds avoid repeated attribute lookups in the hot loop.
        rave_visits = self.rave_visits
        rave_wins = self.rave_wins
        n = self.board.n
        sqrt = math.sqrt

        expl_factor = c * sqrt(math.log(self.n_visits + 1.0))  # same for all children

        best = None
        best_score = float("-inf")

        for ch in self.children.values():
            nv = ch.n_visits
            if nv == 0: return ch  # force exploration of unvisited children

            Q = ch.wins / nv

            f, col = ch.move
            p = f * n + col
            rv = rave_visits[p]
            Q_rave = rave_wins[p] / rv  # rv > 0 thanks to the prior

            w = rv / (rv + nv)
            exploration = expl_factor / sqrt(nv)  # sqrt(log)/sqrt(nv) == sqrt(log/nv)

            score = (1.0 - w) * (Q + exploration) + w * Q_rave
            if score > best_score:
                best_score = score
                best = ch

        return best

    def expand(self):
        if not self.untried_moves:
            return None

        move = self.untried_moves.pop()
        new_board = self.board.copy()
        new_board.place(move[0], move[1], new_board.current_player)
        new_board.rm_move(move[0], move[1])  # keep the move list consistent for descendants
        child = Node(new_board, parent=self, move=move, player=-new_board.current_player)
        self.children[move] = child
        return child

    def rollout(self):
        """Play uniformly random moves until someone wins (Hex has no draws).

        The rollout also stops on a *virtual* win — a chain of stones and
        unbroken bridges spanning the player's edges — which shortens
        simulations without changing the winner in the vast majority of
        playouts.

        Returns ``(winner, played_moves)`` where ``played_moves`` is the list
        of ``(row, col, player)`` needed for RAVE updates.
        """
        # Selection can land on a node whose game is already decided — with a
        # full board there would be nothing left to pop from the pool.
        if self.board.check_win(1): return 1, []
        if self.board.check_win(-1): return -1, []

        simu_board = self.board.copy()
        pool = simu_board.moves_list[:]
        random.shuffle(pool)

        played_moves = []

        while True:
            pl = simu_board.current_player
            f, c = pool.pop()
            simu_board.place(f, c, pl)
            played_moves.append((f, c, pl))

            if simu_board.check_win(pl): return pl, played_moves
            if simu_board.check_virtual_win(pl): return pl, played_moves

    def fully_expanded(self) -> bool:
        return len(self.untried_moves) == 0

    def is_terminal(self) -> bool:
        if self.board.move_count < self.board.n: return False  # a win needs at least n stones from one player
        return self.board.check_win(1) or self.board.check_win(-1)


class MCTS:
    """Time-bounded MCTS engine.

    The tree is reusable across calls: pass the previous root (advanced to the
    move actually played) as ``root`` and the accumulated statistics are kept.
    """

    __slots__ = ("c")

    def __init__(self, c: float = 0.2):
        self.c = c

    def search(self, root_board, root=None, t_limit: float = 5.0):
        """Run simulations until ``t_limit`` seconds elapse and return the
        most visited root move as ``(row, col)``.

        ``root_board`` must reflect the position *as seen by the player to
        move*; if ``root`` is given, its board must match ``root_board``.
        """
        deadline = time.perf_counter() + t_limit

        if root is None:
            root = Node(root_board.copy())

        while time.perf_counter() < deadline:
            node = root

            # Selection
            while node.fully_expanded() and not node.is_terminal():
                nxt = node.best_child(c=self.c)
                if nxt is None: break
                node = nxt

            # Expansion
            if not node.is_terminal() and node.untried_moves:
                node = node.expand()

            # Simulation
            result, played_moves = node.rollout()

            # Backpropagation
            cur = node
            while cur is not None:
                cur.n_visits += 1
                if cur.player is not None and result == cur.player:
                    cur.wins += 1

                p_to_move = cur.board.current_player
                n = cur.board.n
                B = cur.board.flat
                rv = cur.rave_visits
                rw = cur.rave_wins

                for (f, c, pl) in played_moves:
                    if pl != p_to_move: continue
                    p = f * n + c

                    if B[p] != 0: continue  # occupied at this node: not a legal AMAF move here
                    if rv[p] < _RAVE_MAX: rv[p] += 1
                    if result == p_to_move and rw[p] < _RAVE_MAX: rw[p] += 1

                cur = cur.parent

        if not root.children: return random.choice(root.board.get_moves())

        # A child already won by its mover is a proven immediate win for the
        # side to move at the root — play it regardless of visit counts.
        for ch in root.children.values():
            if ch.board.check_win(ch.player): return ch.move

        best = max(root.children.values(), key=lambda ch: ch.n_visits)
        return best.move