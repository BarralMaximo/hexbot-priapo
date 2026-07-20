from hex_mcts import UnionFind

def test_initially_disjoint():
    uf = UnionFind(10)
    assert not uf.connected(0, 1)
    assert all(uf.find(i) == i for i in range(10))

def test_union_and_transitivity():
    uf = UnionFind(10)
    uf.union(0, 1)
    uf.union(1, 2)
    assert uf.connected(0, 2)
    assert not uf.connected(0, 3)

def test_small_universe_uses_one_byte_arrays():
    assert UnionFind(255).parent.typecode == "B"
    assert UnionFind(256).parent.typecode == "H"

def test_copy_is_independent():
    uf = UnionFind(10)
    uf.union(0, 1)
    clone = uf.copy()
    clone.union(2, 3)
    assert clone.connected(0, 1)
    assert clone.connected(2, 3)
    assert not uf.connected(2, 3)