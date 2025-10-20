from random import choice
from math import inf

game_board = [[0, 0, 0],
              [0, 0, 0],
              [0, 0, 0]]

def display_board(board):
    player_symbols = {1: 'X', -1: 'O', 0: ' '}
    for row_index in board:
        for symbol_value in row_index:
            symbol = player_symbols[symbol_value]
            print(f'| {symbol} |', end='')
        print('\n' + '---------------')
    print('===============')

def reset_board(board):
    for row_index, row in enumerate(board):
        for col_index, col in enumerate(row):
            board[row_index][col_index] = 0

def check_win_for_player(board, player):
    conditions = [[board[0][0], board[0][1], board[0][2]],
                     [board[1][0], board[1][1], board[1][2]],
                     [board[2][0], board[2][1], board[2][2]],
                     [board[0][0], board[1][0], board[2][0]],
                     [board[0][1], board[1][1], board[2][1]],
                     [board[0][2], board[1][2], board[2][2]],
                     [board[0][0], board[1][1], board[2][2]],
                     [board[0][2], board[1][1], board[2][0]]]

    if [player, player, player] in conditions:
        return True

    return False

def is_game_over(board):
    return check_win_for_player(board, 1) or check_win_for_player(board, -1)

def print_game_result(board):
    if check_win_for_player(board, 1):
        print('X has won! ' + '\n')

    elif check_win_for_player(board, -1):
        print('O\'s have won! ' + '\n')

    else:
        print('Draw' + '\n')

def get_empty_cells(board):
    empty_cells = []
    for row_index, row in enumerate(board):
        for col_index, col in enumerate(row):
            if board[row_index][col_index] == 0:
                empty_cells.append([row_index, col_index])

    return empty_cells

def is_board_full(board):
    if len(get_empty_cells(board)) == 0:
        return True
    return False

def make_move(board, row_index, col_index, player):
    board[row_index][col_index] = player

def human_player_move(board):
    is_valid_move = True
    move_coordinates = {1: [0, 0], 2: [0, 1], 3: [0, 2],
                        4: [1, 0], 5: [1, 1], 6: [1, 2],
                        7: [2, 0], 8: [2, 1], 9: [2, 2]}
    while is_valid_move:
        try:
            player_move_input = int(input('Enter a number between 1-9: '))
            if player_move_input < 1 or player_move_input > 9:
                print('Invalid Move! Try again!')
            elif not (move_coordinates[player_move_input] in get_empty_cells(board)):
                print('Invalid Move! Try again!')
            else:
                make_move(board, move_coordinates[player_move_input][0], move_coordinates[player_move_input][1], 1)
                display_board(board)
                is_valid_move = False
        except(KeyError, ValueError):
            print('Enter a number!')

def evaluate_score(board):
    if check_win_for_player(board, 1):
        return 10

    elif check_win_for_player(board, -1):
        return -10

    else:
        return 0

def minimax_alpha_beta(board, depth, alpha, beta, player):
    row = -1
    col = -1
    if depth == 0 or is_game_over(board):
        return [row, col, evaluate_score(board)]

    else:
        for current_cell in get_empty_cells(board):
            make_move(board, current_cell[0], current_cell[1], player)
            minimax_score = minimax_alpha_beta(board, depth - 1, alpha, beta, -player)
            if player == 1:
                # X is always the max player
                if minimax_score[2] > alpha:
                    alpha = minimax_score[2]
                    row = current_cell[0]
                    col = current_cell[1]

            else:
                if minimax_score[2] < beta:
                    beta = minimax_score[2]
                    row = current_cell[0]
                    col = current_cell[1]

            make_move(board, current_cell[0], current_cell[1], 0)

            if alpha >= beta:
                break

        if player == 1:
            return [row, col, alpha]

        else:
            return [row, col, beta]

def ai_move_o(board):
    if len(get_empty_cells(board)) == 9:
        row_index = choice([0, 1, 2])
        col_index = choice([0, 1, 2])
        make_move(board, row_index, col_index, -1)
        display_board(board)

    else:
        result = minimax_alpha_beta(board, len(get_empty_cells(board)), -inf, inf, -1)
        make_move(board, result[0], result[1], -1)
        display_board(board)

def ai_move_x(board):
    if len(get_empty_cells(board)) == 9:
        row_index = choice([0, 1, 2])
        col_index = choice([0, 1, 2])
        make_move(board, row_index, col_index, 1)
        display_board(board)

    else:
        result = minimax_alpha_beta(board, len(get_empty_cells(board)), -inf, inf, 1)
        make_move(board, result[0], result[1], 1)
        display_board(board)

def execute_move(board, player, mode):
    if mode == 1:
        if player == 1:
            human_player_move(board)

        else:
            ai_move_o(board)
    else:
        if player == 1:
            ai_move_o(board)
        else:
            ai_move_x(board)

def play_game_pvc():
    while True:
        try:
            player_order = int(input('Enter to play 1st or 2nd: '))
            if not (player_order == 1 or player_order == 2):
                print('Please pick 1 or 2')
            else:
                break
        except(KeyError, ValueError):
            print('Enter a number')

    reset_board(game_board)
    if player_order == 2:
        current_player = -1
    else:
        current_player = 1

    while not (is_board_full(game_board) or is_game_over(game_board)):
        execute_move(game_board, current_player, 1)
        current_player *= -1

    print_game_result(game_board)

# Driver Code
print("=================================================")
print("TIC-TAC-TOE using MINIMAX with ALPHA-BETA Pruning")
print("=================================================")
play_game_pvc()
