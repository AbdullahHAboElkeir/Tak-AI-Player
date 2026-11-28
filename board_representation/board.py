
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional


class PlayerColor(Enum):
    WHITE = "white"
    BLACK = "black"


class PieceType(Enum):
    FLAT = "flat"
    STANDING = "standing"
    CAPSTONE = "capstone"


@dataclass(frozen=True)
class Piece:
    color: PlayerColor
    piece_type: PieceType


@dataclass
class Player:
    color: PlayerColor
    stones_remaining: int = 20
    capstones_remaining: int = 1
    opening_stone_remaining: int = 1

    def has_stones(self) -> bool:
        return self.stones_remaining > 0

    def has_capstone(self) -> bool:
        return self.capstones_remaining > 0

    def has_opening_stone(self):
        return self.opening_stone_remaining > 0

    def use_stone(self) -> bool:
        if self.stones_remaining <= 0:
            return False
        self.stones_remaining -= 1
        return True

    def use_opening_stone(self) -> bool:
        if self.opening_stone_remaining <= 0:
            return False
        self.opening_stone_remaining -= 1
        return True

    def use_capstone(self) -> bool:
        if self.capstones_remaining <= 0:
            return False
        self.capstones_remaining -= 1
        return True


class Board:
    def __init__(self, size: int = 5):
        if type(size) is not int or size < 3:
            raise ValueError(
                "Board size must be an integer of at least 3."
            )

        self.size = size

        # Each cell contains a stack of pieces.
        # The last piece is the top piece.
        self.grid: list[list[list[Piece]]] = [
            [[] for _ in range(size)]
            for _ in range(size)
        ]

    def is_valid_position(self, row: int, col: int) -> bool:
        return 0 <= row < self.size and 0 <= col < self.size

    def get_stack(self, row: int, col: int) -> list[Piece]:
        if not self.is_valid_position(row, col):
            raise IndexError("Invalid board position.")

        return self.grid[row][col]

    def get_top_piece(
        self, row: int, col: int
    ) -> Optional[Piece]:
        stack = self.get_stack(row, col)
        return stack[-1] if stack else None

    def get_stack_height(self, row: int, col: int) -> int:
        return len(self.get_stack(row, col))

    def is_empty(self, row: int, col: int) -> bool:
        return self.get_stack_height(row, col) == 0

    def place_piece(
        self, row: int, col: int, piece: Piece
    ) -> bool:
        """Place a piece on an empty cell."""

        if not self.is_valid_position(row, col):
            return False

        if not isinstance(piece, Piece):
            return False

        if not self.is_empty(row, col):
            return False

        self.grid[row][col].append(piece)
        return True

    def remove_top_piece(
        self, row: int, col: int
    ) -> Optional[Piece]:
        stack = self.get_stack(row, col)

        if not stack:
            return None

        return stack.pop()

    def remove_top_pieces(
        self, row: int, col: int, count: int
    ) -> Optional[list[Piece]]:
        """
        Remove the top N pieces from a stack.
        The returned list preserves the original bottom-to-top order.
        """
        if not self.is_valid_position(row, col):
            return None

        stack = self.grid[row][col]
        if count <= 0 or count > len(stack):
            return None

        removed = stack[-count:]
        del stack[-count:]
        return removed

    def add_to_stack(
        self, row: int, col: int, pieces: list[Piece]
    ) -> bool:
        """Add pieces to an existing stack."""
        if not self.is_valid_position(row, col):
            return False

        if not pieces:
            return False

        if not all(isinstance(piece, Piece) for piece in pieces):
            return False

        self.grid[row][col].extend(pieces)
        return True

    def set_stack(
        self, row: int, col: int, pieces: list[Piece]
    ) -> None:
        if not self.is_valid_position(row, col):
            raise IndexError("Invalid board position.")

        self.grid[row][col] = list(pieces)

    def get_all_pieces(self) -> list[Piece]:
        pieces = []

        for row in self.grid:
            for stack in row:
                pieces.extend(stack)

        return pieces

    def clone(self) -> "Board":
        new_board = Board(self.size)

        for row in range(self.size):
            for col in range(self.size):
                new_board.grid[row][col] = (
                    self.grid[row][col].copy()
                )

        return new_board

    def display(self) -> None:
        print("\n" + "=" * (self.size * 12))

        for row in range(self.size):
            for col in range(self.size):
                stack = self.grid[row][col]

                if not stack:
                    cell = "Empty"
                else:
                    top = stack[-1]
                    cell = (
                        f"{top.color.value[0].upper()}-"
                        f"{top.piece_type.value[0].upper()}"
                        f"({len(stack)})"
                    )

                print(f"{cell:^10}", end=" ")

            print()

        print("=" * (self.size * 12))


@dataclass
class GameState:
    board: Board = field(default_factory=Board)

    players: dict = field(default_factory=lambda: {
        PlayerColor.WHITE: Player(PlayerColor.WHITE),
        PlayerColor.BLACK: Player(PlayerColor.BLACK)
    })

    current_player: PlayerColor = PlayerColor.WHITE
    move_number: int = 0

    def switch_turn(self) -> None:
        if self.current_player == PlayerColor.WHITE:
            self.current_player = PlayerColor.BLACK
        else:
            self.current_player = PlayerColor.WHITE

        self.move_number += 1

    def clone(self) -> "GameState":
        return GameState(
            board=self.board.clone(),
            players={
                color: Player(
                    color=player.color,
                    stones_remaining=player.stones_remaining,
                    capstones_remaining=player.capstones_remaining
                    opening_stone_remaining=player.opening_stone_remaining
                )
                for color, player in self.players.items()
            },
            current_player=self.current_player,
            move_number=self.move_number
        )
