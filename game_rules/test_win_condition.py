from board_representation.board import (
    Board,
    GameState,
    Piece,
    PieceType,
    PlayerColor,
)
from game_rules.win_condition import WinCondition


def place_road(board, cells, color=PlayerColor.WHITE, piece_type=PieceType.FLAT):
    for row, col in cells:
        board.place_piece(row, col, Piece(color, piece_type))


def test_finds_straight_vertical_road_on_small_board():
    board = Board(5)
    place_road(board, [(row, 2) for row in range(5)])

    assert WinCondition().has_road(board, PlayerColor.WHITE)


def test_five_cell_winding_road_is_not_valid():
    board = Board(5)
    place_road(
        board,
        [(0, 1), (0, 2), (0, 3), (0, 4), (1, 4)]
    )

    assert not WinCondition().has_road(
        board, PlayerColor.WHITE
    )


def test_standing_stone_blocks_road():
    board = Board(5)
    place_road(board, [(row, 2) for row in (0, 2, 3, 4)])
    place_road(board, [(1, 2)], piece_type=PieceType.STANDING)

    assert not WinCondition().has_road(board, PlayerColor.WHITE)


def test_road_must_connect_opposite_edges():
    board = Board(5)
    place_road(board, [(0, col) for col in range(1, 5)] + [(1, 4)])

    assert not WinCondition().has_road(board, PlayerColor.WHITE)


def test_capstone_is_a_road_piece():
    board = Board(5)
    place_road(
        board,
        [(row, 2) for row in range(5)],
        piece_type=PieceType.CAPSTONE,
    )

    assert WinCondition().has_road(board, PlayerColor.WHITE)


def test_other_color_road_does_not_count():
    board = Board(5)
    place_road(
        board,
        [(row, 2) for row in range(5)],
        color=PlayerColor.BLACK,
    )

    assert not WinCondition().has_road(board, PlayerColor.WHITE)


def test_flat_stone_win_ignores_all_pieces_in_stacks():
    board = Board(5)
    board.place_piece(0, 0, Piece(PlayerColor.WHITE, PieceType.FLAT))
    board.place_piece(0, 1, Piece(PlayerColor.WHITE, PieceType.FLAT))
    board.place_piece(1, 0, Piece(PlayerColor.BLACK, PieceType.FLAT))
    board.set_stack(
        1,
        1,
        [
            Piece(PlayerColor.WHITE, PieceType.FLAT),
            Piece(PlayerColor.WHITE, PieceType.FLAT),
        ],
    )
    board.set_stack(
        1,
        2,
        [
            Piece(PlayerColor.WHITE, PieceType.FLAT),
            Piece(PlayerColor.BLACK, PieceType.FLAT),
        ],
    )

    rules = WinCondition()
    assert rules.count_flat_stones(board, PlayerColor.WHITE) == 2
    assert rules.count_flat_stones(board, PlayerColor.BLACK) == 1
    assert rules.flat_stone_win(board) == PlayerColor.WHITE


def test_flat_stone_win_returns_none_on_a_tie():
    board = Board(5)
    place_road(
        board,
        [(0, 0), (0, 1)],
        color=PlayerColor.WHITE,
    )
    place_road(
        board,
        [(1, 0), (1, 1)],
        color=PlayerColor.BLACK,
    )

    assert WinCondition().flat_stone_win(board) is None


def test_road_takes_precedence_over_flat_score_on_full_board():
    game = GameState(board=Board(5))
    board = game.board

    for row in range(board.size):
        for col in range(board.size):
            board.set_stack(
                row,
                col,
                [Piece(PlayerColor.WHITE, PieceType.STANDING)],
            )

    board.set_stack(2, 1, [Piece(PlayerColor.WHITE, PieceType.FLAT)])
    board.set_stack(2, 3, [Piece(PlayerColor.WHITE, PieceType.FLAT)])
    for row in range(board.size):
        board.set_stack(row, 4, [Piece(PlayerColor.BLACK, PieceType.FLAT)])

    assert WinCondition().check_win_condition(game) == PlayerColor.BLACK


def test_all_stones_win_requires_stones_and_capstone_exhausted():
    game = GameState()
    player = game.players[PlayerColor.WHITE]
    player.stones_remaining = 0
    player.capstones_remaining = 0

    assert WinCondition().all_stones_win(game, PlayerColor.WHITE)


def test_all_stones_win_is_false_while_inventory_remains():
    game = GameState()
    player = game.players[PlayerColor.WHITE]
    player.stones_remaining = 0

    assert not WinCondition().all_stones_win(game, PlayerColor.WHITE)
