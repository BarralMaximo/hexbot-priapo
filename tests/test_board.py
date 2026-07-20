import numpy as np

from hex_mcts import HexBoard

def test_place_updates_board_and_turn():
    b = HexBoard(5)
    assert b.current_player == 1
    b.place(2, 2, 1, simulation=False)
    assert b.board[2, 2] == 1
    assert b.current_player == -1
    assert b.move_count == 1
    assert (2, 2) not in b.moves_list

def test_horizontal_chain_wins_for_player_1():
    b = HexBoard(5)
    for c in range(5):
        b.place(2, c, 1, simulation=False)
    assert b.check_win(1)
    assert not b.check_win(-1)

def test_vertical_chain_wins_for_player_minus_1():
    b = HexBoard(5)
    for r in range(5):
        b.place(r, 3, -1, simulation=False)
    assert b.check_win(-1)
    assert not b.check_win(1)

def test_diagonal_neighbors_connect():
    # (r, c) and (r-1, c+1) are adjacent in Hex.
    b = HexBoard(3)
    b.place(2, 0, 1, simulation=False)
    b.place(1, 1, 1, simulation=False)
    b.place(0, 2, 1, simulation=False)
    assert b.check_win(1)

def test_incomplete_chain_does_not_win():
    b = HexBoard(5)
    for c in range(4):
        b.place(2, c, 1, simulation=False)
    assert not b.check_win(1)

def test_copy_is_independent_and_shares_topology():
    b = HexBoard(5)
    b.place(0, 0, 1, simulation=False)
    clone = b.copy()
    clone.place(1, 1, -1, simulation=False)

    assert b.board[1, 1] == 0
    assert clone.board[0, 0] == 1
    # Precomputed topology is shared on purpose (immutable).
    assert clone.neighbors_idx is b.neighbors_idx
    assert clone.bridges_from is b.bridges_from

def test_flat_view_is_synchronized():
    b = HexBoard(4)
    b.place(1, 2, -1)
    assert b.flat[1 * 4 + 2] == -1
    assert np.shares_memory(b.flat, b.board)