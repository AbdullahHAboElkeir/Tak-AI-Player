from board_representation.board import GameState, Piece, PieceType, PlayerColor
from game_rules.rules_simple import GameRules


def test_opening_move_gives_opponent_the_opening_piece():
    game = GameState()
    rules = GameRules()

    rules.opening_move(game, 0, 0)

    piece = game.board.get_top_piece(0, 0)
    assert piece == Piece(PlayerColor.BLACK, PieceType.FLAT)
    assert game.current_player == PlayerColor.BLACK


def test_place_piece_requires_opening_moves_and_consumes_inventory():
    game = GameState()
    rules = GameRules()
    game.move_number = 2

    rules.place_piece(game, 0, 0, PieceType.STANDING)

    assert game.board.get_top_piece(0, 0) == Piece(
        PlayerColor.WHITE,
        PieceType.STANDING,
    )
    assert game.players[PlayerColor.WHITE].stones_remaining == 19
    assert game.current_player == PlayerColor.BLACK
    assert game.move_number == 3


def test_move_stack_drops_pieces_in_distribution():
    game = GameState()
    rules = GameRules()
    game.move_number = 2
    game.board.set_stack(
        1,
        1,
        [
            Piece(PlayerColor.WHITE, PieceType.FLAT),
            Piece(PlayerColor.WHITE, PieceType.STANDING),
        ],
    )

    rules.move_stack(game, 1, 1, "RIGHT", 2, [1, 1])

    assert game.board.get_stack_height(1, 1) == 0
    assert game.board.get_stack(1, 2) == [
        Piece(PlayerColor.WHITE, PieceType.STANDING)
    ]
    assert game.board.get_stack(1, 3) == [
        Piece(PlayerColor.WHITE, PieceType.FLAT)
    ]
    assert game.current_player == PlayerColor.BLACK
    assert game.move_number == 3
