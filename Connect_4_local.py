import numpy as np
import random
import pygame 
import sys
import math

def create_board():
    '''Creates the 6 row by seven column game board'''
    board = np.zeros((6,7))
    return board

def drop_piece(board, row, col, piece):
    '''Drops the game piece into the specified column'''
    board[row][col] = piece

def is_valid_loc(board, col):
    '''Checks to see if the top row of the column has been filled to see if you can still drop pieces in the column'''
    return board[5][col] == 0

def next_open_row(board, col):
    '''Determines which row is the next open row for the column you are dropping the piece into'''
    for row in range(6):
        if board[row][col] == 0:
            return row

def winning(board, piece):
    '''Determines whether your last move was a winning move'''
    # check horizontal
    for c in range(4):
        for r in range(6):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    # check vertical
    for c in range(7):
        for r in range(3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    # check positive slope diagonal
    for c in range(4):
        for r in range(3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # check negative slope diagonal
    for c in range(4):
        for r in range(3, 6):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def print_board(board):
    '''Flips the board around the top row, since the array interprets what we consider (0,0) to be 
    the top left as opposed to what we want which is the bottom left'''
    print(np.flip(board, 0))

board = create_board()
game_over = False
turn = 0

#initialize pygame
pygame.init()

#defining some colors
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
green = (0, 255, 0)

#loading a font from pygame fonts
font = pygame.font.SysFont('impact', 90)

#rows/columns on board
rows = 6
columns = 7

#size of each 'square' and height/width of board
slotsize = 100
board_width = slotsize * columns
board_height = slotsize * (rows + 1)

#defines the pygame window
display = pygame.display.set_mode((board_width, board_height))
    
def draw_board(board):
    '''draws the board using pygame'''
    for i in range(columns):
        for j in range(rows):
            pygame.draw.rect(display, blue, ((i*100, (j*100)+100, 100, 100)))
            if board[j][i] == 0:
                pygame.draw.circle(display, black, ((i*100)+50, (j*100)+150), 42.5)
            elif board[j ][i] == 1:
                pygame.draw.circle(display, yellow, ((i*100)+50, (j*100)+150), 42.5)
            else:
                pygame.draw.circle(display, red, ((i*100)+50, (j*100)+150), 42.5)
    pygame.display.update()

draw_board(board)
pygame.display.update()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(display, black, (0, 0, 700, 100))
            x_pixel = event.pos[0]
            if turn % 2 == 0:
                pygame.draw.circle(display, yellow, (x_pixel, 50), 42.5)
            else:
                pygame.draw.circle(display, red, (x_pixel, 50), 42.5)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # player one turn
            if turn % 2 == 0:
                x_pixel = event.pos[0]
                col = int(math.floor(x_pixel/100))

                if is_valid_loc(board, col):
                    row = next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning(board, 1):
                        winner = "Player 1"
                        game_over = True

            #player two turn
            else:
                x_pixel = event.pos[0]
                col = int(math.floor(x_pixel/100))

                if is_valid_loc(board, col):
                    row = next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning(board, 2):
                        winner = "Player 2"
                        game_over = True
    
            draw_board(np.flip(board,0))

            turn += 1

            if game_over:
                end_msg = font.render("GAME OVER", True, green)
                win_msg = font.render(f"{winner} Wins!", True, green)
                end_rect = end_msg.get_rect(center=(board_width/2, board_height/2-60))
                win_rect = win_msg.get_rect(center=(board_width/2, board_height/2+60))
                display.blit(end_msg, end_rect)
                display.blit(win_msg, win_rect)
                pygame.display.update()
                pygame.time.wait(5000)
                
                