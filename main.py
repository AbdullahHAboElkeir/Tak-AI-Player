
from board_representation.board import (
    Board,
    Piece,
    PieceType,
    PlayerColor,
    GameState
)


game = GameState()

# Place pieces on the board
game.board.place_piece(
    0, 0,
    Piece(PlayerColor.WHITE, PieceType.FLAT)
)

game.board.place_piece(
    0, 1,
    Piece(PlayerColor.BLACK, PieceType.STANDING)
)

# Add another piece to the first stack
game.board.set_stack(
    0, 0,
    [
        Piece(PlayerColor.WHITE, PieceType.FLAT),
        Piece(PlayerColor.BLACK, PieceType.FLAT)
    ]
)

# Display board
print("TAK AI PLAYER")
game.board.display()

# Display stack information
print("\nStack Information:")
print("Stack height:", game.board.get_stack_height(0, 0))
print("Top piece:", game.board.get_top_piece(0, 0))

# Display current player
print("\nCurrent player:", game.current_player.value)

# Switch turn
game.switch_turn()
print("Next player:", game.current_player.value)

# Test cloning
new_state = game.clone()

print("\nCloned Board:")
new_state.board.display()
