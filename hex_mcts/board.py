import numpy as np

from .union_find import UnionFind

class HexBoard:
    """State and rules of an n x n Hex board.

    Player ``+1`` connects the left and right edges; player ``-1`` connects
    the top and bottom edges. There are no draws in Hex.

    Performance-critical design:

    - **Win detection via Union-Find**: every placed stone is unioned with its
      same-colored neighbors and, on the edge columns/rows, with a virtual
      edge node. ``check_win`` is then two ``find`` calls.
    - **Virtual connections (bridges)**: a second pair of Union-Find
      structures additionally unions stones connected by a *bridge* — the
      two-cell template that cannot be cut if the owner always answers the
      intrusion. ``check_virtual_win`` lets Monte Carlo rollouts terminate
      early, which speeds up convergence considerably.
    - **O(1) move list**: available moves live in a list with a reverse index
      (``pos_idx``) so removal is a swap-and-pop.
    - **Precomputed topology**: neighbor lists and every possible bridge
      pattern per cell are computed once in ``__init__``.

    Bridge bookkeeping (``track_bridges=True``, used only on the agent's real
    board) stores the bridges owned by player +1 so that an opponent intrusion
    into one of the two critical cells can be answered deterministically with
    the sister cell (see ``bridge_response``).

    Note on overlapping bridges: when a new bridge would share a critical cell
    with an already-registered one, the new bridge is discarded. Handling the
    overlap exactly would require rebuilding the virtual Union-Find on every
    collision; the performance cost outweighs the rare positions where the
    simplification gives a sub-optimal forced defense.

    Note on virtual connections in rollouts: virtual unions are additive and
    never undone, so a rollout may end on a "virtual win" whose critical cells
    were later occupied during that same rollout. This keeps rollouts fast and
    is a standard approximation — the affected player could have answered each
    intrusion as it happened.
    """

    __slots__ = ("n", "board", "flat", "current_player", "move_count", "uf1", "uf2", "uf1_virtual", "uf2_virtual", "top", "bottom",
                 "left", "right", "track_bridges", "pos_idx", "moves_list", "neighbors_idx", "bridges_from", "bridges", "bridge_map")

    # Bridge templates as (stone offset) -> [critical cell offsets].
    # Each pattern is also applied with sign -1, covering all 6 orientations.
    BRIDGE_PATTERNS = {(-1, -1): [(0, -1), (-1, 0)],
                       (-2, 1): [(-1, 0), (-1, 1)],
                       (1, -2): [(0, -1), (1, -1)]}

    NEIGHBORS = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, -1)]

    def __init__(self, n: int, track_bridges: bool = False):
        self.n = n
        self.board = np.zeros((n, n), dtype=np.int8)
        self.flat = self.board.reshape(-1)  # 1D view, shares memory with `board`
        self.current_player = 1
        self.move_count = 0

        # Union-Find structures: `size` cells plus two virtual edge nodes.
        # The same two extra indices act as left/right for player +1 and
        # top/bottom for player -1 (each player has its own UF instances).
        size = n * n + 2
        self.left, self.right = n * n, n * n + 1
        self.top, self.bottom = n * n, n * n + 1

        self.uf1 = UnionFind(size)          # player +1, real connections
        self.uf2 = UnionFind(size)          # player -1, real connections
        self.uf1_virtual = UnionFind(size)  # player +1, real + bridge unions
        self.uf2_virtual = UnionFind(size)  # player -1, real + bridge unions

        # Bridge bookkeeping (player +1 only, real board only).
        self.track_bridges = track_bridges
        self.bridges = {}     # frozenset({stone1, stone2}) -> [crit1, crit2]
        self.bridge_map = {}  # critical cell -> sister critical cell

        self.bridges_from, self.neighbors_idx = self._precompute_topology()

        # Available-move list with O(1) removal.
        self.pos_idx = np.full((n, n), -1, dtype=np.int16)
        self.moves_list = []
        for i in range(n):
            for j in range(n):
                self.pos_idx[i, j] = len(self.moves_list)
                self.moves_list.append((i, j))

    def get_moves(self):
        return self.moves_list.copy()

    def rm_move(self, f: int, c: int) -> None:
        idx = int(self.pos_idx[f, c])
        if idx == -1: return

        last_idx = len(self.moves_list) - 1
        
        if idx != last_idx:
            last_mv = self.moves_list[last_idx]
            self.moves_list[idx] = last_mv
            self.pos_idx[last_mv] = idx
        
        self.moves_list.pop()
        self.pos_idx[f, c] = -1

    def _precompute_topology(self):
        """Build, once per board, the neighbor list and every possible bridge
        ``(far stone, critical cell 1, critical cell 2)`` for each cell."""
        n = self.n
        bridges = [[] for _ in range(n * n)]
        neighbors = [[] for _ in range(n * n)]

        for r in range(n):
            for c in range(n):
                p = r * n + c
                for (df, dc), crits in self.BRIDGE_PATTERNS.items():
                    for sign in (1, -1):
                        nr, nc = r + df * sign, c + dc * sign
                        if not (0 <= nr < n and 0 <= nc < n): continue

                        b1r, b1c = r + crits[0][0] * sign, c + crits[0][1] * sign
                        b2r, b2c = r + crits[1][0] * sign, c + crits[1][1] * sign
                        if 0 <= b1r < n and 0 <= b1c < n and 0 <= b2r < n and 0 <= b2c < n:
                            bridges[p].append((nr * n + nc, b1r * n + b1c, b2r * n + b2c))

                for dr, dc in self.NEIGHBORS:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < n:
                        neighbors[p].append(nr * n + nc)

        return bridges, neighbors

    def detect_bridges(self, f: int, c: int, player: int) -> None:
        """Register any new bridges formed by the stone just placed at (f, c).

        A bridge is valid when the far stone belongs to the same player and
        both critical cells are empty. Valid bridges are unioned in the
        player's *virtual* Union-Find; overlapping bridges are discarded (see
        class docstring). With ``track_bridges`` on, player +1's bridges are
        also stored for deterministic defense.
        """
        n = self.n
        p = f * n + c
        uf_virtual = self.uf1_virtual if player == 1 else self.uf2_virtual
        B = self.flat

        for q, b1, b2 in self.bridges_from[p]:
            if B[q] == player and B[b1] == 0 and B[b2] == 0:
                b1rc = (b1 // n, b1 % n)
                b2rc = (b2 // n, b2 % n)
                if b1rc in self.bridge_map or b2rc in self.bridge_map: continue

                uf_virtual.union(p, q)

                if player == 1 and self.track_bridges:
                    qrc = (q // n, q % n)
                    self.bridges[frozenset({(f, c), qrc})] = [b1rc, b2rc]
                    self.bridge_map[b1rc] = b2rc
                    self.bridge_map[b2rc] = b1rc

    def bridge_response(self, f: int, c: int):
        """Return the forced defense against a move at (f, c), if any.

        If (f, c) is a critical cell of a stored bridge and its sister cell is
        still empty, the sister cell is the deterministic response that keeps
        the bridge connected. Returns ``(row, col)`` or ``None``.
        """
        resp = self.bridge_map.get((f, c))
        if resp and self.board[resp] == 0: return resp
        return None

    def idx(self, f: int, c: int) -> int:
        return f * self.n + c

    def place(self, f: int, c: int, player: int, simulation: bool = True) -> None:
        """Place a stone, updating Union-Find state (and metadata if real).

        With ``simulation=True`` (rollouts) only the essentials for win
        detection are updated. With ``simulation=False`` (real moves) the
        available-move list and the bridge bookkeeping are maintained too.
        """
        self.board[f, c] = player
        self.move_count += 1

        if not simulation:
            self.rm_move(f, c)

            # A stone on a critical cell invalidates its bridge's bookkeeping
            # (the bridge is either being defended or was just broken).
            if (f, c) in self.bridge_map:
                crit = (f, c)
                sister = self.bridge_map.pop(crit, None)
                if sister is not None:
                    self.bridge_map.pop(sister, None)
                for key, crits in list(self.bridges.items()):
                    if crit in crits or (sister is not None and sister in crits):
                        self.bridges.pop(key)

        idx = f * self.n + c
        uf_real = self.uf1 if player == 1 else self.uf2
        uf_virtual = self.uf1_virtual if player == 1 else self.uf2_virtual

        # Union with the edge nodes.
        if player == 1:
            if c == 0:
                uf_real.union(idx, self.left)
                uf_virtual.union(idx, self.left)
            if c == self.n - 1:
                uf_real.union(idx, self.right)
                uf_virtual.union(idx, self.right)
        else:
            if f == 0:
                uf_real.union(idx, self.top)
                uf_virtual.union(idx, self.top)
            if f == self.n - 1:
                uf_real.union(idx, self.bottom)
                uf_virtual.union(idx, self.bottom)

        # Union with same-colored neighbors.
        for q in self.neighbors_idx[idx]:
            if self.flat[q] == player:
                uf_real.union(idx, q)
                uf_virtual.union(idx, q)

        self.detect_bridges(f, c, player)
        self.current_player = -player

    def check_win(self, player: int) -> bool:
        if player == 1: return self.uf1.connected(self.left, self.right)
        return self.uf2.connected(self.top, self.bottom)

    def check_virtual_win(self, player: int) -> bool:
        if player == 1: return self.uf1_virtual.connected(self.left, self.right)
        return self.uf2_virtual.connected(self.top, self.bottom)

    def copy(self) -> "HexBoard":
        """Fast deep-enough copy for MCTS simulations.

        Mutable game state (board, Union-Finds, move list) is copied;
        immutable precomputed topology is shared. Bridge bookkeeping is not
        copied — only the agent's real board tracks bridges.
        """
        new = object.__new__(type(self))
        new.n = self.n
        new.board = self.board.copy()
        new.flat = new.board.reshape(-1)
        new.current_player = self.current_player
        new.move_count = self.move_count
        new.track_bridges = False

        new.uf1 = self.uf1.copy()
        new.uf2 = self.uf2.copy()
        new.uf1_virtual = self.uf1_virtual.copy()
        new.uf2_virtual = self.uf2_virtual.copy()

        new.top, new.bottom = self.top, self.bottom
        new.left, new.right = self.left, self.right

        new.neighbors_idx = self.neighbors_idx  # shared, immutable
        new.bridges_from = self.bridges_from    # shared, immutable

        new.moves_list = self.moves_list.copy()
        new.pos_idx = self.pos_idx.copy()

        new.bridges = {}
        new.bridge_map = {}

        return new