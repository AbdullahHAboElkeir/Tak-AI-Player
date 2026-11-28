from board_representation.board import PieceType, PlayerColor

DIRECTIONS = [
    (-1, 0),  # up
    (1, 0),   # down
    (0, -1),  # left
    (0, 1),   # right
]

class WinCondition:

    def check_win_condition(self, game):
        board = game.board

        for color in [PlayerColor.WHITE, PlayerColor.BLACK]:

            if self.has_road(board, color):
                return color

            if self.all_stones_win(game, color):
                return color

        if self.is_board_full(board):
            return self.flat_stone_win(board)

        return None

    def is_road_piece(self, board, row, col, color):
        stack = board.get_stack(row, col)

        if not stack:
            return False

        top = stack[-1]

        return (
        top.color == color
        and top.piece_type != PieceType.STANDING
        )

    def get_edges(self, board, row, col):
        edges = []

        if row == 0:
            edges.append("TOP")

        if row == board.size - 1:
            edges.append("BOTTOM")

        if col == 0:
            edges.append("LEFT")

        if col == board.size - 1:
            edges.append("RIGHT")

        return edges

    def has_road(self, board, color):
        for row in range(board.size):
            for col in range(board.size):

                if not self.is_road_piece(board, row, col, color):
                    continue

                edges = self.get_edges(board, row, col)

                for start_edge in edges:
                    path = {(row, col)}

                    if self.search_road(
                        board,
                        color,
                        row,
                        col,
                        start_edge,
                        path,
                        False,
                        None,
                    ):
                        return True

        return False

    def search_road(
    self,
    board,
    color,
    row,
    col,
    start_edge,
    path,
    turned,
    previous_direction,
    ):
        edges = self.get_edges(board, row, col)

        if (
            len(path) >= 5
            and any(edge != start_edge for edge in edges)
            and (not turned or len(path) >= 6)
        ):
            return True

        for row_change, col_change in DIRECTIONS:
            new_row = row + row_change
            new_col = col + col_change

            if not board.is_valid_position(new_row, new_col):
                continue

            if (new_row, new_col) in path:
                continue

            if not self.is_road_piece(
            board, new_row, new_col, color
            ):
                continue

            direction = (row_change, col_change)

            new_turned = turned

            if (
            previous_direction is not None
            and direction != previous_direction
            ):
                new_turned = True

            path.add((new_row, new_col))

            if self.search_road(
            board,
            color,
            new_row,
            new_col,
            start_edge,
            path,
            new_turned,
            direction,
            ):
                return True

            path.remove((new_row, new_col))

        return False

    def count_flat_stones(self, board, color):
        count = 0

        for row in range(board.size):
            for col in range(board.size):
                stack = board.get_stack(row, col)

                if (
                len(stack) == 1
                and stack[0].color == color
                and stack[0].piece_type == PieceType.FLAT
                ):
                    count += 1

        return count

    
    def is_board_full(self, board):
            for row in range(board.size):
                for col in range(board.size):
                    if board.is_empty(row, col):
                        return False

            return True

    def flat_stone_win(self, board):
        white = self.count_flat_stones(
            board, PlayerColor.WHITE
        )
        black = self.count_flat_stones(
            board, PlayerColor.BLACK
        )

        if white > black:
                return PlayerColor.WHITE
        elif black > white:
            return PlayerColor.BLACK

        return None

    
    def all_stones_win(self, game, color):
        player = game.players[color]

        return (
        player.stones_remaining == 0
        and player.capstones_remaining == 0
        )