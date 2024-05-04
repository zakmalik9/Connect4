import pygame


class WinManager:
    def check_for_win(self, board, piece):
        # Check Horizontal
        for col in range(self.c_count - 3):
            for r in range(self.r_count):
                if board[r][col] == piece and board[r][col + 1] == piece and board[r][col + 2] == piece \
                        and board[r][col + 3] == piece:
                    return True
        # Check Vertical
        for col in range(self.c_count):
            for r in range(self.r_count - 3):
                if board[r][col] == piece and board[r + 1][col] == piece and board[r + 2][col] == piece \
                        and board[r + 3][col] == piece:
                    return True
        # Check +Slope Diagonals
        for col in range(self.c_count - 3):
            for r in range(self.r_count - 3):
                if board[r][col] == piece and board[r + 1][col + 1] == piece and board[r + 2][col + 2] == piece \
                        and board[r + 3][col + 3] == piece:
                    return True
        # Check -Slope Diagonals
        for col in range(self.c_count - 3):
            for r in range(3, self.r_count):
                if board[r][col] == piece and board[r - 1][col + 1] == piece and board[r - 2][col + 2] == piece \
                        and board[r - 3][col + 3] == piece:
                    return True


    def __init__(self, board, font_name, font_size, player1_piece, player1_text, player2_piece, player2_text,
                 row_count, column_count, cell_size):
        self.board = board
        self.font = pygame.font.SysFont(font_name, font_size)
        self.pl1_piece = player1_piece
        self.pl1_text = player1_text
        self.pl2_piece = player2_piece
        self.pl2_text = player2_text
        self.r_count = row_count
        self.c_count = column_count
        self.cell = cell_size


    def display_win_text(self, screen, default_color, player1_color, player2_color):
        width = self.cell * self.c_count
        if self.check_for_win(self.board, self.pl1_piece):
            pygame.draw.rect(screen, default_color, (0, 0, width, self.cell))
            label = self.font.render(self.pl1_text, 1, player1_color)
            screen.blit(label, (40, 10))
            return True
        elif self.check_for_win(self.board, self.pl2_piece):
            pygame.draw.rect(screen, default_color, (0, 0, width, self.cell))
            label = self.font.render(self.pl2_text, 1, player2_color)
            screen.blit(label, (40, 10))
            return True
        else:
            return False
