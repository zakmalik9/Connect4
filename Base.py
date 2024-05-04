class Base():
    def is_valid_location(self, row_count, default_piece, board, column):
        return board[row_count - 1][column] == default_piece


    def get_next_open_row(self, row_count, default_piece, board, column):
        for r in range(row_count):
            if board[r][column] == default_piece:
                return r


    def drop_piece(self, board, row, column, piece):
        board[row][column] == piece
