from tkinter import *
from tkinter import colorchooser
import tkinter.ttk as ttk
import pygame
import numpy as np
from Board import Board
from WinManager import WinManager
from Players import HumanPlayer
from Players import ComputerPlayer
import random


gui = Tk()
gui.iconbitmap("icon.ico")
gui.title("Connect4")
gui["bg"] = "black"
gui.minsize(width=700, height=700)
title = Label(gui, text="Connect4", font=("monospace", 80), fg="white", bg="black", pady=100)
title.pack()
# Game Variables
mode = ""
r_count = IntVar()
c_count = IntVar()
cell_size = 100
player1_color = (255, 0, 0)
player1_turn = 0
player1_piece = 1
player1_depth = IntVar()
player2_color = (255, 255, 0)
player2_turn = 1
player2_piece = 2
player2_depth = IntVar()
default_color = (0, 0, 0)
default_piece = 0
grid_color = (0, 0, 255)


def pick_def_color():
    global default_color
    global def_color_btn
    default_color, btn_color = colorchooser.askcolor()
    def_color_btn["bg"] = btn_color


def pick_grid_color():
    global grid_color
    global grid_color_btn
    grid_color, btn_color = colorchooser.askcolor()
    grid_color_btn["bg"] = btn_color


def pick_pl1_color():
    global player1_color
    global pl1_color_btn
    player1_color, btn_color = colorchooser.askcolor()
    pl1_color_btn["bg"] = btn_color


def pick_pl2_color():
    global player2_color
    global pl2_color_btn
    player2_color, btn_color = colorchooser.askcolor()
    pl2_color_btn["bg"] = btn_color


def save_start():
    global new
    new.destroy()
    global gui
    gui.destroy()


def click(sender):
    global mode
    if sender == "pvp_btn":
        mode = "PvP"
    elif sender == "pvc_btn":
        mode = "PvC"
    elif sender == "cvc_btn":
        mode = "CvC"
        global new
    new = Toplevel(gui)
    new.iconbitmap("icon.ico")
    new.title("Connect4")
    r_lab = Label(new, text="Rows:", padx=10, pady=10)
    r_lab.grid(row=1, column=0, padx=10, pady=10)
    r_om = ttk.OptionMenu(new, r_count, 6, 5, 6, 7, 8)
    r_om.grid(row=1, column=1, padx=10, pady=10)
    c_lab = Label(new, text="Columns:", padx=10, pady=10)
    c_lab.grid(row=2, column=0, padx=10, pady=10)
    c_om = ttk.OptionMenu(new, c_count, 7, 5, 6, 7, 8, 9, 10)
    c_om.grid(row=2, column=1, padx=10, pady=10)
    global def_color_btn
    def_color_lab = Label(new, text="Default Color:", padx=10, pady=10)
    def_color_lab.grid(row=3, column=0, padx=10, pady=10)
    def_color_btn = Button(new, text="          ", command=pick_def_color, bg="black")
    def_color_btn.grid(row=3, column=1, padx=10, pady=10)
    global grid_color_btn
    grid_color_lab = Label(new, text="Grid Color:", padx=10, pady=10)
    grid_color_lab.grid(row=4, column=0, padx=10, pady=10)
    grid_color_btn = Button(new, text="          ", command=pick_grid_color, bg="blue")
    grid_color_btn.grid(row=4, column=1, padx=10, pady=10)
    global pl1_color_btn
    pl1_text = ""
    if mode == "PvP":
        pl1_text = "Player 1 Piece Color:"
    elif mode == "PvC":
        pl1_text = "Player Piece Color:"
    elif mode == "CvC":
        pl1_text = "Computer 1 Piece Color:"
    pl1_color_lab = Label(new, text=pl1_text, padx=10, pady=10)
    pl1_color_lab.grid(row=5, column=0, padx=10, pady=10)
    pl1_color_btn = Button(new, text="          ", command=pick_pl1_color, bg="red")
    pl1_color_btn.grid(row=5, column=1, padx=10, pady=10)
    global pl2_color_btn
    pl2_text = ""
    if mode == "PvP":
        pl2_text = "Player 2 Piece Color:"
    elif mode == "PvC":
        pl2_text = "Computer Piece Color:"
    elif mode == "CvC":
        pl2_text = "Computer 2 Piece Color:"
    pl2_color_lab = Label(new, text=pl2_text, padx=10, pady=10)
    pl2_color_lab.grid(row=6, column=0, padx=10, pady=10)
    pl2_color_btn = Button(new, text="          ", command=pick_pl2_color, bg="yellow")
    pl2_color_btn.grid(row=6, column=1, padx=10, pady=10)
    save_btn = Button(new, text="Save and Start Game", command=save_start)
    save_btn.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
    if mode == "PvC":
        pl2_depth_lab = Label(new, text="Computer Depth", padx=10, pady=10)
        pl2_depth_lab.grid(row=7, column=0, padx=10, pady=10)
        pl2_depth_om = ttk.OptionMenu(new, player2_depth, 4, 1, 2, 3, 4, 5, 6, 7, 8)
        pl2_depth_om.grid(row=7, column=1, padx=10, pady=10)
        save_btn.grid(row=8, column=0, columnspan=2, padx=10, pady=10)
    elif mode == "CvC":
        pl1_depth_lab = Label(new, text="Computer 1 Depth", padx=10, pady=10)
        pl1_depth_lab.grid(row=7, column=0, padx=10, pady=10)
        pl1_depth_om = ttk.OptionMenu(new, player1_depth, 4, 1, 2, 3, 4, 5, 6, 7, 8)
        pl1_depth_om.grid(row=7, column=1, padx=10, pady=10)
        pl2_depth_lab = Label(new, text="Computer 2 Depth", padx=10, pady=10)
        pl2_depth_lab.grid(row=8, column=0, padx=10, pady=10)
        pl2_depth_om = ttk.OptionMenu(new, player2_depth, 4, 1, 2, 3, 4, 5, 6, 7, 8)
        pl2_depth_om.grid(row=8, column=1, padx=10, pady=10)
        save_btn.grid(row=9, column=0, columnspan=2, padx=10, pady=10)


pvp_btn = Button(gui, text="Player vs Player", font=("monospace", 30), fg="white", bg="black", bd=10,
                 command=lambda: click("pvp_btn"))
pvp_btn.pack(pady=10, ipadx=100)
pvc_btn = Button(gui, text="Player vs Computer", font=("monospace", 30), fg="white", bg="black", bd=10,
                 command=lambda: click("pvc_btn"))
pvc_btn.pack(pady=10, ipadx=70)
cvc_btn = Button(gui, text="Computer vs Computer", font=("monospace", 30), fg="white", bg="black", bd=10,
                 command=lambda: click("cvc_btn"))
cvc_btn.pack(pady=10, ipadx=40)

gui.mainloop()


def create_screen(column_count, row_count, cell_size):
    pygame.init()
    width = int(column_count * cell_size)
    height = int((row_count + 1) * cell_size)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Connect4")
    icon = pygame.image.load("icon.ico")
    pygame.display.set_icon(icon)
    pygame.display.update()
    return screen


def create_board(column_count, row_count):
    board = np.zeros((row_count, column_count))
    return np.flip(board, 0)


# Main Game
row_count = int(str(r_count.get()))
column_count = int(str(c_count.get()))
screen = create_screen(column_count, row_count, cell_size)
board = create_board(column_count, row_count)
b = Board(screen, board, row_count, column_count, default_color, default_piece, grid_color, player1_color, player1_piece,
       player2_color, player2_piece, cell_size)
turn = random.randint(player1_turn, player2_turn)
pl1_win_text = ""
pl2_win_text = ""
if mode == "PvP":
    player1 = HumanPlayer(board, turn, player1_piece, row_count, default_piece, cell_size)
    pl1_win_text = "Player 1 Wins!"
    player2 = HumanPlayer(board, turn, player2_piece, row_count, default_piece, cell_size)
    pl2_win_text = "Player 2 Wins!"
elif mode == "PvC":
    player1 = HumanPlayer(board, turn, player1_piece, row_count, default_piece, cell_size)
    pl1_win_text = "Player Wins!!!"
    player2 = ComputerPlayer(board, turn, player2_piece, player1_piece, player2_depth, row_count, column_count, default_piece)
    pl2_win_text = "Computer Wins..."
elif mode == "CvC":
    player1 = ComputerPlayer(board, turn, player1_piece, player2_piece, player1_depth, row_count, column_count, default_piece)
    pl1_win_text = "Computer 1 Wins"
    player2 = ComputerPlayer(board, turn, player2_piece, player1_piece, player2_depth, row_count, column_count, default_piece)
    pl2_win_text = "Computer 2 Wins"
wm = WinManager(board, "monospace", 75, player1_piece, pl1_win_text, player2_piece, pl2_win_text,
                row_count, column_count, cell_size)
game_running = True
while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
    if mode == "PvP":
        b.mouse_follow(turn, True)
    elif mode == "PvC":
        b.mouse_follow(turn, False)
    if turn == player1_turn and game_running:
        player1.play_play()
    if wm.display_win_text(screen, default_color, player1_color, player2_color):
        game_running = False
    b.draw_update()
    if turn == player2_turn and game_running:
        player2.play_play()
    if wm.display_win_text(screen, default_color, player1_color, player2_color):
        game_running = False
    b.draw_update()


over_running = True
while over_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            over_running = False
    pygame.display.update()
