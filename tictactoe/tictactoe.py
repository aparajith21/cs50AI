"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy
X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if terminal(board):
        return None
    
    knt = int(0)
    for i in range(3):
        for j in range(3):
            if board[i][j] != EMPTY:
                knt += 1
    if knt % 2 == 0:
        return X
    else:
        return O
            


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    if terminal(board):
        return None
        
    actions_possible = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions_possible.add((i, j))
    return actions_possible
    
def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    
    if action not in actions(board):
        raise ValueError("Action is not valid")
    else:
        copy_board = deepcopy(board)
        (i, j) = action
        copy_board[i][j] = player(board)
        
    return copy_board
        


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if board[0][0] == board[1][1] == board[2][2] != None:
        return board[0][0]
    elif board[0][2] == board[1][1] == board[2][0] != None:
        return board[1][1]
    elif board[0][0] == board[0][1] == board[0][2] != None:
        return board[0][1]
    elif board[1][0] == board[1][1] == board[1][2] != None:
        return board[1][1]
    elif board[2][0] == board[2][1] == board[2][2] != None:
        return board[2][1]
    elif board[0][0] == board[1][0] == board[2][0] != None:
        return board[1][0]
    elif board[0][1] == board[1][1] == board[2][1] != None:
        return board[1][1]
    elif board[0][2] == board[1][2] == board[2][2] != None:
        return board[2][2]
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    Winner = winner(board)
    if Winner == O:
        return -1
    elif Winner == X:
        return 1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if board == [[EMPTY] * 3] * 3:
        return (0, 0)
    if terminal(board):
        return None        
    optimal_action = None
    Player = player(board)
    if Player == X:
        max = float("-inf")
        for action in actions(board):
            max_result = minimise(result(board, action))
            if max_result > max:
                optimal_action = action
                max = max_result
    elif Player == O:
        min = float("inf")
        for action in actions(board):
            min_result = maximise(result(board, action))
            if min_result < min:
                optimal_action = action
                min = min_result
    return optimal_action
    
def maximise(board):
    if terminal(board):
        return utility(board)
        
    maximum = float("-inf")
    for action in actions(board):
        maximum = max(maximum, minimise(result(board, action)))
        if maximum == 1:
            return 1
    
    return maximum
    
def minimise(board):
    if terminal(board):
        return utility(board)
        
    minimum = float("inf")
    for action in actions(board):
        minimum = min(minimum, maximise(result(board, action)))
        if minimum == -1:
            return -1
    
    return minimum
                
