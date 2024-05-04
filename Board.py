import pygame
import numpy as np


class Board:
    def __init__(self, screen, board, row_count, column_count, default_color, default_piece, grid_color, player1_color, player1_piece,
                 player2_color, player2_piece, cell_size):
        self.r_count = row_count
        self.c_count = column_count
        self.def_col = default_color
        self.def_piece = default_piece
        self.grid_col = grid_color
        self.pl1_col = player1_color
        self.pl1_piece = player1_piece
        self.pl2_col = player2_color
        self.pl2_piece = player2_piece
        self.cell = cell_size
        self.screen = screen
        self.board = board


    def draw_update(self):
        cell_off = int(self.cell/2)
        cell_rad = cell_off - 5
        for c in range(self.c_count):
            for r in range(self.r_count):
                rect_pos_x = c * self.cell
                rect_pos_y = r * self.cell + self.cell
                circle_pos_x = c * self.cell + cell_off
                circle_pos_y = r * self.cell + self.cell + cell_off
                pygame.draw.rect(self.screen, self.grid_col, (rect_pos_x, rect_pos_y, self.cell, self.cell))
                pygame.draw.circle(self.screen, self.def_col, (circle_pos_x, circle_pos_y), cell_rad)
                if self.board[r][c] == self.pl1_piece:
                    pygame.draw.circle(self.screen, self.pl1_col, (circle_pos_x, circle_pos_y), cell_rad)
                elif self.board[r][c] == self.pl2_piece:
                    pygame.draw.circle(self.screen, self.pl2_col, (circle_pos_x, circle_pos_y), cell_rad)
        pygame.display.update()


    def mouse_follow(self, turn, follow_player2):
        width = int(self.c_count * self.cell)
        cell_off = int(self.cell / 2)
        cell_rad = cell_off - 5
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                mouse_x = event.pos[0]
                pygame.draw.rect(self.screen, self.def_col, (0, 0, width, self.cell))
                if turn == 0:
                    pygame.draw.circle(self.screen, self.pl1_col, (mouse_x, cell_off), cell_rad)
                if turn == 1 and follow_player2:
                    pygame.draw.circle(self.screen, self.pl2_col, (mouse_x, cell_off), cell_rad)
            pygame.display.update()
