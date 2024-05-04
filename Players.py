import pygame
import math
from Base import Base
from Minimax import MiniMax


class Players(Base):
    def play(self, turn, board, column, piece, row_count, default_piece):
        if column is not None and self.is_valid_location(row_count, default_piece, board, column):
            row = self.get_next_open_row(row_count, default_piece, board, column)
            self.drop_piece(board, row, column, piece)
            turn += 1
            turn %= 2


class HumanPlayer(Players):
    def __init__(self, board, turn, player_piece, row_count, default_piece, cell_size):
        self.board = board
        self.turn = turn
        self.piece = player_piece
        self.r_count = row_count
        self.def_piece = default_piece
        self.cell = cell_size


    def get_click_position(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                return event.pos[0]


    def get_column(self):
        click_x = self.get_click_position()
        return int(math.floor(click_x / self.cell))


    def play_play(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_x = event.pos[0]
                column = int(math.floor(click_x / self.cell))
                self.play(self.board, self.turn, column, self.piece, self.r_count, self.def_piece)


class ComputerPlayer(MiniMax, Players):
    def __init__(self, board, turn, computer_piece, opponent_piece, depth, row_count, column_count, default_piece):
        self.board = board
        self.turn = turn
        self.piece = computer_piece
        self.opp_piece = opponent_piece
        self.depth = depth
        self.r_count = row_count
        self.c_count = column_count
        self.def_piece = default_piece


    def get_column(self):
        column = self.execute_minimax(self.board, self.depth, -math.inf, math.inf, True, self.piece, self.opp_piece,
                                      self.r_count, self.c_count, self.def_piece)[0]
        return column


    def play_play(self):
        column = self.get_column()
        self.play(self.board, self.turn, column, self.piece, self.r_count, self.def_piece)

