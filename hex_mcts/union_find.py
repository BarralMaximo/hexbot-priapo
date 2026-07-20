from array import array

class UnionFind:
    """Union-Find with union by rank and path compression (by halving).

    The implementation is optimized for memory: a naive list-based DSU stores
    8-byte pointers to boxed Python integers, which made early versions of the
    agent exceed 500 MB of RAM once thousands of board copies were alive inside
    the search tree. Storing the data in compact ``array`` buffers instead
    removes the per-object overhead entirely:

    - ``parent``: ``array('H')`` (2-byte unsigned) — or ``array('B')``
      (1 byte) when the universe fits in 255 elements.
    - ``rank``: ``array('B')`` (1-byte unsigned).

    Limitation: the 2-byte representation supports universes up to 65535
    elements, i.e. Hex boards up to 255x255 — far beyond any practical size.
    """

    __slots__ = ("parent", "rank")

    def __init__(self, size: int):
        if size <= 255:
            self.parent = array("B", range(size))
        else:
            self.parent = array("H", range(size))
        self.rank = array("B", [0]) * size

    def find(self, x: int) -> int:
        parent = self.parent
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # Path compression by halving
            x = parent[x]
        return x

    def union(self, x: int, y: int) -> None:
        parent, rank = self.parent, self.rank
        xr, yr = self.find(x), self.find(y)

        if xr == yr:
            return
        if rank[xr] < rank[yr]:
            parent[xr] = yr
        elif rank[xr] > rank[yr]:
            parent[yr] = xr
        else:
            parent[yr] = xr
            rank[xr] += 1

    def connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)

    def copy(self) -> "UnionFind":
        new = object.__new__(type(self))
        new.parent = array(self.parent.typecode, self.parent)
        new.rank = array("B", self.rank)
        return new