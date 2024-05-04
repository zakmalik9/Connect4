# Import Modules
import numpy as np
import pygame
import math
# Initialize PyGame
pygame.init()
# Game Variables
row_count = 6
column_count = 7
cell_size = 100
cell_offset = int(cell_size/2)
cell_radius = cell_offset - 5
grid_color = (0, 0, 255)
default_color = (0, 0, 0)
player1_color = (255, 0, 0)
player2_color = (255, 255, 0)
# SetUp the Screen
width = column_count * cell_size
height = (row_count + 1) * cell_size
screen = pygame.display.set_mode((width, height))


# Create a Matrix of the Specified Size containing all 0s
def create_board():
    brd = np.zeros((row_count, column_count))
    return brd


# Check if the Column Selected is not already Filled
def is_valid_location(brd, col):
    is_valid = brd[row_count - 1][col] == 0
    return is_valid


# Place the Piece into the Selected Location
def drop_piece(brd, r, col, piece):
    brd[r][col] = piece


# Get the First Row that is Empty (Starting from the Bottom)
def get_next_open_row(brd, col):
    for r in range(row_count):
        if brd[r][col] == 0:
            return r


# Check if a Player won
def winning_move(brd, piece):
    # Check Horizontal
    for col in range(column_count - 3):
        for r in range(row_count):
            if brd[r][col] == piece and brd[r][col+1] == piece and brd[r][col+2] == piece and brd[r][col+3] == piece:
                return True
    # Check Vertical
    for col in range(column_count):
        for r in range(row_count - 3):
            if brd[r][col] == piece and brd[r+1][col] == piece and brd[r+2][col] == piece and brd[r+3][col] == piece:
                return True
    # Check +Slope Diagonals
    for col in range(column_count - 3):
        for r in range(row_count - 3):
            if brd[r][col] == piece and brd[r+1][col+1] == piece and brd[r+2][col+2] == piece and brd[r+3][col+3] == piece:
                return True
    # Check -Slope Diagonals
    for col in range(column_count - 3):
        for r in range(3, row_count):
            if brd[r][col] == piece and brd[r-1][col+1] == piece and brd[r-2][col+2] == piece and brd[r-3][col+3] == piece:
                return True


# Go through the Matrix and draw the grid, if any player pieces then Draw them in
def draw_board(brd):
    for col in range(column_count):
        for r in range(row_count):
            pygame.draw.rect(screen, grid_color, (col * cell_size, r * cell_size + cell_size, cell_size, cell_size))
            pygame.draw.circle(screen, default_color, (col * cell_size + cell_offset, r * cell_size + cell_size + cell_offset), cell_radius)
    for col in range(column_count):
        for r in range(row_count):
            if brd[r][col] == 1:
                pygame.draw.circle(screen, player1_color, (col * cell_size + cell_offset, r * cell_size + cell_size + cell_offset), cell_radius)
            if brd[r][col] == 2:
                pygame.draw.circle(screen, player2_color, (col * cell_size + cell_offset, r * cell_size + cell_size + cell_offset), cell_radius)


# Main Game
board = create_board()
turn = 0
font = pygame.font.SysFont("monospace", 75)
game_running = True
while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        if event.type == pygame.MOUSEMOTION:
            mouse_x = event.pos[0]
            pygame.draw.rect(screen, default_color, (0, 0, width, cell_size))
            if turn == 0:
                pygame.draw.circle(screen, player1_color, (mouse_x, cell_offset), cell_radius)
            elif turn == 1:
                pygame.draw.circle(screen, player2_color, (mouse_x, cell_offset), cell_radius)
            pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get the x-coordinate of the Click and then Modify it to get the Column Clicked
            click_x = event.pos[0]
            column = int(math.floor(click_x / cell_size))
            # Ask for Player 1 Input
            if turn == 0:
                if is_valid_location(board, column):
                    row = get_next_open_row(board, column)
                    drop_piece(board, row, column, 1)
                    if winning_move(board, 1):
                        pygame.draw.rect(screen, default_color, (0, 0, width, cell_size))
                        label = font.render("Player 1 Wins!", 1, player1_color)
                        screen.blit(label, (40, 10))
                        game_running = False
                else:
                    turn -= 1
            # Ask for Player 2 Input
            elif turn == 1:
                if is_valid_location(board, column):
                    row = get_next_open_row(board, column)
                    drop_piece(board, row, column, 2)
                    if winning_move(board, 2):
                        pygame.draw.rect(screen, default_color, (0, 0, width, cell_size))
                        label = font.render("Player 2 Wins!", 1, player2_color)
                        screen.blit(label, (40, 10))
                        game_running = False
                else:
                    turn -= 1
            # Increment the Turn
            turn += 1
            turn %= 2
    # Update the Game Board
    draw_board(np.flip(board, 0))
    pygame.display.update()


over_running = True
while over_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            over_running = False
    pygame.display.update()
