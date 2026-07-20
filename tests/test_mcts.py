import numpy as np

from hex_mcts import HexBoard, MCTS, MCTSAgent, Node, RandomAgent, play_match

def test_expanded_child_board_is_consistent():
    """Regression test: expanding a node must remove the played move from the
    child board's move list, otherwise deeper rollouts replay occupied cells."""
    root = Node(HexBoard(4))
    child = root.expand()
    assert child.move not in child.board.moves_list
    assert child.move not in child.untried_moves
    assert child.board.board[child.move] != 0
    grandchild = child.expand()
    assert child.move not in grandchild.board.moves_list

def test_search_returns_legal_move():
    board = HexBoard(4)
    board.place(0, 0, 1, simulation=False)
    board.place(3, 3, -1, simulation=False)
    move = MCTS().search(board, t_limit=0.2)
    assert move in board.moves_list

def test_search_finds_immediate_win():
    # Player 1 holds (1, 0)-(1, 1) on a 3x3 board: both (1, 2) and the
    # adjacent edge cell (0, 2) win on the spot.
    board = HexBoard(3)
    board.place(1, 0, 1, simulation=False)
    board.place(0, 0, -1, simulation=False)
    board.place(1, 1, 1, simulation=False)
    board.place(0, 1, -1, simulation=False)
    move = MCTS().search(board, t_limit=0.5)
    assert move in {(1, 2), (0, 2)}

def test_agent_plays_legal_moves_and_adapts_size():
    agent = MCTSAgent(board_size=13, time_limit=0.1)
    board = np.zeros((5, 5), dtype=int)
    action = agent.action(board.copy())
    r, c = divmod(action, 5)
    assert agent.n == 5
    assert board[r, c] == 0

    # Opponent answers; the agent must play another empty cell.
    board[r, c] = 1
    empties = np.argwhere(board == 0)
    orow, ocol = map(int, empties[0])
    board[orow, ocol] = -1
    action2 = agent.action(board.copy())
    r2, c2 = divmod(action2, 5)
    assert board[r2, c2] == 0

def test_agent_defends_bridge_intrusion():
    agent = MCTSAgent(board_size=5, time_limit=0.1)
    board = np.zeros((5, 5), dtype=int)

    # Agent stones forming a bridge: (2, 2) and (1, 1), crits (2, 1)/(1, 2).
    agent.board.place(2, 2, 1, simulation=False)
    agent.board.place(1, 1, 1, simulation=False)
    agent.first_call = False
    board[2, 2] = 1
    board[1, 1] = 1

    # Opponent intrudes into (2, 1): the forced answer is (1, 2).
    board[2, 1] = -1
    action = agent.action(board.copy())
    assert divmod(action, 5) == (1, 2)

def test_mcts_agent_beats_random():
    agent = MCTSAgent(board_size=5, time_limit=0.15)
    winner = play_match(agent, RandomAgent(), size=5)
    assert winner == 1