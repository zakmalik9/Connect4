# Import Modules
import numpy as np
import pygame
import math
import random
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
player_color = (255, 0, 0)
computer_color = (255, 255, 0)
default_piece = 0
player_piece = 1
computer_piece = 2
window_length = 4
# SetUp the Screen
width = column_count * cell_size
height = (row_count + 1) * cell_size
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Connect4")


# Create a Matrix of the Specified Size containing all 0s
def create_board():
    brd = np.zeros((row_count, column_count))
    return brd


# Check if the Column Selected is not already Filled
def is_valid_location(brd, col):
    is_valid = brd[row_count - 1][col] == default_piece
    return is_valid


# Place the Piece into the Selected Location
def drop_piece(brd, r, col, piece):
    brd[r][col] = piece


# Get the First Row that is Empty (Starting from the Bottom)
def get_next_open_row(brd, col):
    for r in range(row_count):
        if brd[r][col] == default_piece:
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


def win_manager(brd):
    label = font.render("", 1, default_color)
    global game_running
    if winning_move(brd, player_piece):
        pygame.draw.rect(screen, default_color, (0, 0, width, cell_size))
        label = font.render("Player Wins!!!", 1, player_color)
        game_running = False
    elif winning_move(brd, computer_piece):
        pygame.draw.rect(screen, default_color, (0, 0, width, cell_size))
        label = font.render("Computer Wins...", 1, computer_color)
        game_running = False
    screen.blit(label, (40, 10))


# Go through the Matrix and draw the grid, if any player pieces then Draw them in
def draw_board(brd):
    for col in range(column_count):
        for r in range(row_count):
            pygame.draw.rect(screen, grid_color, (col * cell_size, r * cell_size + cell_size, cell_size, cell_size))
            pygame.draw.circle(screen, default_color, (col * cell_size + cell_offset, r * cell_size + cell_size + cell_offset), cell_radius)
    # for col in range(column_count):
        # for r in range(row_count):
            if brd[r][col] == 1:
                pygame.draw.circle(screen, player_color, (col * cell_size + cell_offset, r * cell_size + cell_size + cell_offset), cell_radius)
            if brd[r][col] == 2:
                pygame.draw.circle(screen, computer_color, (col * cell_size + cell_offset, r * cell_size + cell_size + cell_offset), cell_radius)


def evaluate_window(wndw, piece):
    score = 0
    if wndw.count(piece) == 4:
        score += 100
    elif wndw.count(piece) == 3 and wndw.count(0) == 1:
        score += 5
    elif wndw.count(piece) == 2 and wndw.count(0) == 2:
        score += 2
    if wndw.count(player_piece) == 4:
        score -= 99
    elif wndw.count(player_piece) == 3 and wndw.count(0) == 1:
        score -= 4
    elif wndw.count(player_piece) == 2 and wndw.count(0) == 2:
        score -= 1
    return score


def score_position(brd, piece):
    score = 0
    # Score Center
    center_array = [int(i) for i in list(brd[:, column_count//2])]
    center_count = center_array.count(piece)
    score += center_count * 3
    # Score Horizontal
    for r in range(row_count):
        r_array = [int(i) for i in list(brd[r, :])]
        for col in range(column_count - 3):
            window = r_array[col:col+window_length]
            score += evaluate_window(window, piece)
    # Score Vertical
    for col in range(column_count):
        col_array = [int(i) for i in list(brd[:, col])]
        for r in range(column_count - 3):
            window = col_array[r:r+window_length]
            score += evaluate_window(window, piece)
    # Score +Diagonals
    for r in range(row_count - 3):
        for col in range(column_count - 3):
            window = [brd[r+i][col+i] for i in range(window_length)]
            score += evaluate_window(window, piece)
    # Score -Diagonals
    for r in range(row_count - 3):
        for col in range(column_count - 3):
            window = [brd[r+3-i][col+i] for i in range(window_length)]
            score += evaluate_window(window, piece)
    return score


def get_valid_locations(brd):
    valid_locations = []
    for col in range(column_count):
        if is_valid_location(brd, col):
            valid_locations.append(col)
    return valid_locations


# def pick_best_move(brd, piece):
#     valid_locations = get_valid_locations(brd)
#     best_score = 0
#     best_col = random.choice(valid_locations)
#     for col in valid_locations:
#         r = get_next_open_row(brd, col)
#         temp_board = brd.copy()
#         drop_piece(temp_board, r, col, piece)
#         score = score_position(temp_board, piece)
#         if score > best_score:
#             best_score = score
#             best_col = col
#     return best_col


def is_terminal_node(brd):
    return winning_move(brd, player_piece) or winning_move(brd, computer_piece) or len(get_valid_locations(brd)) == 0


def minimax_ab(node, depth, alpha, beta, maximising_player):
    valid_locations = get_valid_locations(node)
    best_col = random.choice(valid_locations)
    if depth == 0 or is_terminal_node(node):
        if is_terminal_node(node):
            if winning_move(node, computer_piece):
                return None, 1000000
            elif winning_move(node, player_piece):
                return None, -1000000
            else:
                return None, 0
        else:
            return None, score_position(node, computer_piece)
    if maximising_player:
        value = -math.inf
        for col in valid_locations:
            r = get_next_open_row(node, col)
            brd_copy = node.copy()
            drop_piece(brd_copy, r, col, computer_piece)
            new_score = minimax_ab(brd_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value
    else:
        value = math.inf
        for col in valid_locations:
            r = get_next_open_row(node, col)
            brd_copy = node.copy()
            drop_piece(brd_copy, r, col, player_piece)
            new_score = minimax_ab(brd_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if beta <= alpha:
                break
        return best_col, value


# Main Game
board = create_board()
print(board)
turn = random.randint(0, 1)
font = pygame.font.SysFont("monospace", 75)
game_running = True
while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        if event.type == pygame.MOUSEMOTION:
            mouse_x = event.pos[0]
            pygame.draw.rect(screen, default_color, (0, 0, width, cell_size))
            pygame.draw.circle(screen, player_color, (mouse_x, cell_offset), cell_radius)
            pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get the x-coordinate of the Click and then Modify it to get the Column Clicked
            click_x = event.pos[0]
            # Ask for Player Input
            if turn == 0 and game_running:
                column = int(math.floor(click_x / cell_size))
                if column is not None and is_valid_location(board, column):
                    row = get_next_open_row(board, column)
                    drop_piece(board, row, column, player_piece)
                    # Increment the Turn
                    turn += 1
                    turn %= 2
    # Update the Game Board
    win_manager(board)
    draw_board(np.flip(board, 0))
    pygame.display.update()
    # AI
    if turn == 1 and game_running:
        # column = pick_best_move(brd, computer_piece)
        pygame.time.wait(500)
        column, minimax_score = minimax_ab(board, 4, -math.inf, math.inf, True)
        if column is not None and is_valid_location(board, column):
            row = get_next_open_row(board, column)
            drop_piece(board, row, column, computer_piece)
            # Increment the Turn
            turn += 1
            turn %= 2
    # Update the Game Board
    win_manager(board)
    draw_board(np.flip(board, 0))
    pygame.display.update()


over_running = True
while over_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            over_running = False
    pygame.display.update()
