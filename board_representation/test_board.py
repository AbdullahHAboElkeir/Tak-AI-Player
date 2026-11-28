
from board import (
    Board,
    Piece,
    PieceType,
    PlayerColor,
    Player,
    GameState
)


def test_board_initialization():
    board = Board(5)

    assert board.size == 5
    assert board.is_empty(0, 0)


def test_place_piece():
    board = Board()

    piece = Piece(PlayerColor.WHITE, PieceType.FLAT)

    assert board.place_piece(0, 0, piece)
    assert not board.is_empty(0, 0)


def test_stack_height():
    board = Board()

    pieces = [
        Piece(PlayerColor.WHITE, PieceType.FLAT),
        Piece(PlayerColor.BLACK, PieceType.FLAT)
    ]

    board.set_stack(0, 0, pieces)

    assert board.get_stack_height(0, 0) == 2


def test_get_top_piece():
    board = Board()

    piece = Piece(PlayerColor.BLACK, PieceType.FLAT)
    board.set_stack(0, 0, [piece])

    assert board.get_top_piece(0, 0) == piece


def test_remove_top_piece():
    board = Board()

    piece = Piece(PlayerColor.WHITE, PieceType.FLAT)
    board.place_piece(0, 0, piece)

    removed = board.remove_top_piece(0, 0)

    assert removed == piece
    assert board.is_empty(0, 0)


def test_board_clone():
    board = Board()

    board.place_piece(
        0, 0,
        Piece(PlayerColor.WHITE, PieceType.FLAT)
    )

    copied = board.clone()
    copied.remove_top_piece(0, 0)

    assert not board.is_empty(0, 0)
    assert copied.is_empty(0, 0)


def test_game_state_switch_turn():
    game = GameState()

    game.switch_turn()

    assert game.current_player == PlayerColor.BLACK
    assert game.move_number == 1


def test_invalid_position():
    board = Board()

    piece = Piece(PlayerColor.WHITE, PieceType.FLAT)

    assert not board.place_piece(10, 10, piece)


def test_invalid_board_size():
    try:
        Board(2)
        assert False
    except ValueError:
        assert True


def test_invalid_board_size_type():
    for size in (2.5, "5", True):
        try:
            Board(size)
            assert False
        except ValueError:
            assert True


def test_player_inventory():
    player = Player(PlayerColor.WHITE)

    assert player.stones_remaining == 20
    assert player.opening_stone_remaining == 1
    assert player.capstones_remaining == 1
    assert player.use_stone()
    assert player.stones_remaining == 19
    assert player.opening_stone_remaining == 1
    assert player.use_capstone()
    assert player.capstones_remaining == 0
    assert not player.use_capstone()


def test_clone_independent_inventory():
    game = GameState()
    copied = game.clone()

    copied.players[PlayerColor.WHITE].use_stone()

    assert game.players[PlayerColor.WHITE].stones_remaining == 20
    assert copied.players[PlayerColor.WHITE].stones_remaining == 19

def test_clone_preserves_opening_stone_inventory():
    game = GameState()
    game.players[PlayerColor.WHITE].use_opening_stone()
    copied = game.clone()
    assert copied.players[PlayerColor.WHITE].opening_stone_remaining == 0

def test_remove_multiple_pieces():
    board = Board()
    pieces = [
        Piece(PlayerColor.WHITE, PieceType.FLAT),
        Piece(PlayerColor.BLACK, PieceType.FLAT),
        Piece(PlayerColor.WHITE, PieceType.STANDING)
    ]
    board.set_stack(0, 0, pieces)

    removed = board.remove_top_pieces(0, 0, 2)

    assert removed == pieces[1:]
    assert board.get_stack_height(0, 0) == 1
    assert board.get_top_piece(0, 0) == pieces[0]


def test_add_pieces_to_stack():
    board = Board()
    first = Piece(PlayerColor.WHITE, PieceType.FLAT)
    second = Piece(PlayerColor.BLACK, PieceType.FLAT)
    board.place_piece(0, 0, first)

    assert board.add_to_stack(0, 0, [second])
    assert board.get_stack_height(0, 0) == 2
    assert board.get_top_piece(0, 0) == second


def test_remove_invalid_number_of_pieces():
    board = Board()
    piece = Piece(PlayerColor.WHITE, PieceType.FLAT)
    board.place_piece(0, 0, piece)

    assert board.remove_top_pieces(0, 0, 0) is None
    assert board.remove_top_pieces(0, 0, 2) is None
    assert board.remove_top_pieces(0, 0, -1) is None
    assert board.remove_top_pieces(-1, 0, 1) is None
    assert board.get_stack_height(0, 0) == 1


def test_add_to_stack_rejects_invalid_input():
    board = Board()

    assert not board.add_to_stack(0, 0, [])
    assert not board.add_to_stack(-1, 0, [
        Piece(PlayerColor.WHITE, PieceType.FLAT)
    ])
    assert not board.add_to_stack(0, 0, [
        Piece(PlayerColor.WHITE, PieceType.FLAT),
        "not a piece"
    ])
    assert board.is_empty(0, 0)


def test_place_piece_rejects_invalid_type():
    board = Board()

    assert not board.place_piece(0, 0, "not a piece")
    assert board.is_empty(0, 0)

def test_add_to_stack_rejects_non_piece():
    board = Board()

    assert not board.add_to_stack(0, 0, ["invalid"])


def test_add_to_stack_rejects_mixed_types():
    board = Board()

    piece = Piece(PlayerColor.WHITE, PieceType.FLAT)

    assert not board.add_to_stack(0, 0, [piece, "invalid"])


def test_remove_top_piece_invalid_position():
    board = Board()

    try:
        board.remove_top_piece(10, 10)
        assert False, "Expected IndexError"
    except IndexError:
        pass
