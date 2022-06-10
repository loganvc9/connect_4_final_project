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


def score_pos(board, piece):
    '''assigns a score to different piece drops for the minimax algorithm'''
    score = 0
    
    # center score
    center_col = [int(i) for i in list(board[:, 7//2])]
    num_in_center = center_col.count(piece)
    score += num_in_center * 3

    # check horizontal score
    for r in range(6):
        full_row = [int(i) for i in list(board[r,:])]
        for column in range(4):
            window = full_row[column:column+4]
            opp_piece = 1
            if piece == 1:
                opp_piece = 2
            if window.count(piece) == 4:
                score += 100
            elif window.count(piece) == 3 and window.count(0) == 1:
                score += 5
            elif window.count(piece) == 2 and window.count(0) == 2:
                score += 2
            if window.count(opp_piece) == 3 and window.count(0) == 1:
                score -= 4
    
    # check vertical score
    for column in range(7):
        full_col = [int(i) for i in list(board[:, column])]
        for r in range(3):
            window = full_col[r:r+4]
            opp_piece = 1
            if piece == 1:
                opp_piece = 2
            if window.count(piece) == 4:
                score += 100
            elif window.count(piece) == 3 and window.count(0) == 1:
                score += 5 
            elif window.count(piece) == 2 and window.count(0) == 2:
                score += 2
            if window.count(opp_piece) == 3 and window.count(0) == 1:
                score -= 4

    #check positive slope diagonal score
    for r in range(3):
        for c in range(4):
            window = [board[r+i][c+i] for i in range(4)]
            opp_piece = 1
            if piece == 1:
                opp_piece = 2
            if window.count(piece) == 4:
                score += 100
            elif window.count(piece) == 3 and window.count(0) == 1:
                score += 5
            elif window.count(piece) == 2 and window.count(0) == 2:
                score += 2
            if window.count(opp_piece) == 3 and window.count(0) == 1:
                score -= 4

    #check negative slope diagonal score
    for r in range(3):
        for c in range(4):
            window = [board[r+3-i][c+i] for i in range(4)]
            opp_piece = 1
            if piece == 1:
                opp_piece = 2
            if window.count(piece) == 4:
                score += 100
            elif window.count(piece) == 3 and window.count(0) == 1:
                score += 5
            elif window.count(piece) == 2 and window.count(0) == 2:
                score += 2
            if window.count(opp_piece) == 3 and window.count(0) == 1:
                score -= 4
    return score

def is_terminal_node(board):
    '''determines when there is a terminal node (aka when the game ends)'''
    return winning(board, 1) or winning(board, 2) or len([col for col in range(7) if is_valid_loc(board, col)]) == 0

def minimax(board, depth, maximizingPlayer):
    '''the minimax recursive algorithm'''
    
    valid_locations = [col for col in range(7) if is_valid_loc(board, col)]
    terminal_node = is_terminal_node(board)
    if depth == 0 or terminal_node:
        if terminal_node:
            if winning(board, 2):
                return (None, 1000000000000)
            elif winning(board, 1):
                return (None, -1000000000000)
            else: # no more moves so game is over
                return (None, 0)
        else:
            return (None, score_pos(board, 2))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = next_open_row(board, col)
            board_copy = board.copy()
            drop_piece(board_copy, row, col, 2)
            new_score = minimax(board_copy, depth-1, False)[1]
            if new_score > value:
                value = new_score
                column = col
        return column, value
    else: #minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = next_open_row(board, col)
            board_copy = board.copy()
            drop_piece(board_copy, row, col, 1)
            new_score = minimax(board_copy, depth-1, True)[1]
            if new_score < value:
                value = new_score
                column = col
        return column, value

def best_move(board, piece):
    '''chooses the best move based on the scoring guidelines. This is not used in minimax'''
    best_score = -10000
    valid_locations = []
    for col in range(7):
        if is_valid_loc(board, col):
            valid_locations.append(col)
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_pos(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col


def print_board(board):
    '''Flips the board around the top row, since the array interprets what we consider (0,0) to be 
    the top left as opposed to what we want which is the bottom left'''
    print(np.flip(board, 0))

board = create_board()
game_over = False
turn = random.randint(0,1)

#initialize pygame
pygame.init()

#defining some colors
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
green = (0, 255, 0)

#loading a font from pygame fonts
font = pygame.font.SysFont('impact', 90, False, False)

#rows/columns on board
rows = 6
columns = 7

#size of each 'square' and height/width of board
slotsize = 100
board_width = slotsize * columns
board_height = slotsize * (rows + 1)

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
    if 0 not in board[-1]:
        end_msg = font.render("TIE GAME!", True, green)
        end_rect = end_msg.get_rect(center=(board_width/2, board_height/2))
        display.blit(end_msg, end_rect)
        pygame.display.update()
        pygame.time.wait(5000)
        sys.exit()
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
                    
                    turn += 1
                    draw_board(np.flip(board,0))

    #player two turn
    if turn % 2 == 1 and not game_over:
        
        #For easy AI uncomment what is below
        #col = random.randint(0, 6)

        #For medium uncomment below
        #col = best_move(board, 2)

        col, minimax_score = minimax(board, 4, True)

        if is_valid_loc(board, col):
            pygame.time.wait(500)
            row = next_open_row(board, col)
            drop_piece(board, row, col, 2)

            if winning(board, 2):
                winner = "Player 2"
                game_over = True
    
            turn += 1

    draw_board(np.flip(board,0))


    if game_over:
        end_msg = font.render("GAME OVER", True, green)
        win_msg = font.render(f"{winner} Wins!", True, green)
        end_rect = end_msg.get_rect(center=(board_width/2, board_height/2-60))
        win_rect = win_msg.get_rect(center=(board_width/2, board_height/2+60))
        display.blit(end_msg, end_rect)
        display.blit(win_msg, win_rect)
        pygame.display.update()
        pygame.time.wait(5000)
                
                