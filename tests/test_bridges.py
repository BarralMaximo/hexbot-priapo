from hex_mcts import HexBoard

def make_bridge(b):
    """Form a player-1 bridge between (2, 2) and (1, 1).

    Those stones sit at relative offset (-1, -1), whose critical (empty)
    cells are (2, 1) and (1, 2).
    """
    b.place(2, 2, 1, simulation=False)
    b.place(1, 1, 1, simulation=False)
    return (2, 2), (1, 1), (2, 1), (1, 2)

def test_bridge_is_detected_and_virtually_connected():
    b = HexBoard(5, track_bridges=True)
    s1, s2, crit1, crit2 = make_bridge(b)
    assert frozenset({s1, s2}) in b.bridges
    assert b.bridge_map[crit1] == crit2
    assert b.bridge_map[crit2] == crit1
    assert b.uf1_virtual.connected(b.idx(*s1), b.idx(*s2))
    assert not b.uf1.connected(b.idx(*s1), b.idx(*s2)) # The stones are not adjacent: no real connection yet.

def test_bridge_response_returns_sister_cell():
    b = HexBoard(5, track_bridges=True)
    _, _, crit1, crit2 = make_bridge(b)
    assert b.bridge_response(*crit1) == crit2
    assert b.bridge_response(*crit2) == crit1
    assert b.bridge_response(0, 0) is None

def test_intrusion_clears_bridge_bookkeeping():
    b = HexBoard(5, track_bridges=True)
    s1, s2, crit1, _ = make_bridge(b)
    b.place(crit1[0], crit1[1], -1, simulation=False) # opponent intrudes
    assert frozenset({s1, s2}) not in b.bridges
    assert crit1 not in b.bridge_map

def test_bridges_only_tracked_when_enabled():
    b = HexBoard(5) # simulation boards do not track bridge metadata
    s1, s2, _, _ = make_bridge(b)
    assert b.bridges == {}
    assert b.uf1_virtual.connected(b.idx(*s1), b.idx(*s2)) # The virtual union still happens: rollouts rely on it.

def test_virtual_win_via_bridge():
    b = HexBoard(3)
    b.place(1, 0, 1) # touches the left edge
    b.place(0, 2, 1) # touches the right edge; bridges (1, 0) via (0, 1)/(1, 1)
    assert not b.check_win(1)
    assert b.check_virtual_win(1)