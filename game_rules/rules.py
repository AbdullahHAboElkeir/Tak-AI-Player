from board_representation.board import Piece, PieceType, PlayerColor


DIRECTIONS = { #allowed directions for moving stones
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1),
}


class GameRules:
    def opening_move(self, game, row, col): #opening move when the game starts, the first player places a flat stone of the opposite color to the first player
        player = game.players[game.current_player]

        if game.move_number >= 2:
            raise ValueError("Opening moves are already finished")
        if not player.has_opening_stone:
            raise ValueError("Opening stone already used")
        if not game.board.is_valid_position(row, col):
            raise ValueError("Position is outside the board")
        if not game.board.is_empty(row, col):
            raise ValueError("Position is not empty")

        opening_color = (
            PlayerColor.BLACK
            if player.color == PlayerColor.WHITE
            else PlayerColor.WHITE
        )
        game.board.place_piece(row, col, Piece(opening_color, PieceType.FLAT))
        player.use_opening_stone()
        game.switch_turn()

    def place_piece(self, game, row, col, piece_type): #place a piece on the board, either a flat stone, standing stone, or capstone
        player = game.players[game.current_player]

        if game.move_number < 2:
            raise ValueError("Opening move required")
        if not game.board.is_valid_position(row, col):
            raise ValueError("Position is outside the board")
        if not game.board.is_empty(row, col):
            raise ValueError("Position is not empty")

        if not self.is_valid_move(
            game, "PLACE", row, col, piece_type=piece_type
        ):
            if piece_type not in (
                PieceType.FLAT,
                PieceType.STANDING,
                PieceType.CAPSTONE,
            ):
                raise ValueError("Invalid piece type")
            if piece_type == PieceType.CAPSTONE:
                raise ValueError("No capstone remaining")
            raise ValueError("No stones remaining")

        game.board.place_piece(row, col, Piece(player.color, piece_type))
        if piece_type in (PieceType.FLAT, PieceType.STANDING):
            player.use_stone()
        else:
            player.use_capstone()
        game.switch_turn()

    def is_valid_move( #a move is valid if the position is on the board, the position is empty, and the player has the appropriate piece to place
        self,
        game,
        move_type,
        row,
        col,
        piece_type=None,
        direction=None,
        count=None,
        distribution=None,
    ):
        player = game.players[game.current_player]

        if not game.board.is_valid_position(row, col):
            return False

        if move_type == "PLACE":
            if not game.board.is_empty(row, col):
                return False
            if piece_type in (PieceType.FLAT, PieceType.STANDING):
                return player.has_stones
            return piece_type == PieceType.CAPSTONE and player.has_capstone

        if move_type != "MOVE":
            return False

        stack = game.board.get_stack(row, col)
        if (
            not stack
            or stack[-1].color != player.color
            or count is None
            or count < 1
            or count > len(stack)
            or direction not in DIRECTIONS
            or not distribution
            or any(number <= 0 for number in distribution)
            or sum(distribution) != count
        ):
            return False

        row_change, col_change = DIRECTIONS[direction]
        carried = list(reversed(stack[-count:]))
        piece_index = 0

        for i, pieces_to_drop in enumerate(distribution, start=1):
            new_row = row + row_change * i
            new_col = col + col_change * i
            if not game.board.is_valid_position(new_row, new_col):
                return False

            destination = game.board.get_stack(new_row, new_col).copy()
            for _ in range(pieces_to_drop):
                piece = carried[piece_index]
                if not self.can_stack(destination, piece):
                    return False

                if (
                    destination
                    and destination[-1].piece_type == PieceType.STANDING
                    and piece.piece_type == PieceType.CAPSTONE
                ):
                    standing = destination[-1]
                    destination[-1] = Piece(standing.color, PieceType.FLAT)

                destination.append(piece)
                piece_index += 1

        return True

    def can_stack(self, destination_stack, piece): #a piece can be stacked on a stack if the stack is empty, or if the top piece is a flat stone, or if the top piece is a standing stone and the piece being placed is a capstone
        if not destination_stack:
            return True

        top = destination_stack[-1]
        return top.piece_type == PieceType.FLAT or (
            top.piece_type == PieceType.STANDING
            and piece.piece_type == PieceType.CAPSTONE
        )

    def move_stack(self, game, row, col, direction, count, distribution): #move a stack of pieces in a given direction, dropping pieces according to the distribution list
        if not self.is_valid_move(
            game,
            "MOVE",
            row,
            col,
            direction=direction,
            count=count,
            distribution=distribution,
        ):
            raise ValueError("Invalid move")

        row_change, col_change = DIRECTIONS[direction]
        stack = game.board.get_stack(row, col)
        carried = list(reversed(stack[-count:]))
        game.board.remove_top_pieces(row, col, count)

        piece_index = 0
        for i, pieces_to_drop in enumerate(distribution, start=1):
            destination_row = row + row_change * i
            destination_col = col + col_change * i
            destination = game.board.get_stack(destination_row, destination_col)

            for _ in range(pieces_to_drop):
                piece = carried[piece_index]
                if not self.can_stack(destination, piece):
                    raise ValueError("Piece cannot be placed on this stack")

                if (
                    destination
                    and destination[-1].piece_type == PieceType.STANDING
                    and piece.piece_type == PieceType.CAPSTONE
                ):
                    standing = destination[-1]
                    destination[-1] = Piece(
                        standing.color,
                        PieceType.FLAT,
                    )

                destination.append(piece)
                piece_index += 1
        game.switch_turn()
