#!/usr/bin/env python
# coding: utf-8


##################################################################
# Jin Wang
# March 2, 2021
# The following has been changed to the source code degrees.py:
# 1) 
##################################################################
from IPython.core.debugger import set_trace

"""
Tic Tac Toe Player
"""

import math
import copy

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
    movesLeft = sum(x.count(EMPTY) for x in board)
    if (movesLeft % 2) == 1:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    result = set()
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if col == EMPTY:
                result.add((i, j))         
    return result
                

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # If action is not a valid action for the board, your program should raise an exception.
    if(action[0] >= len(board) or action[1] >= len(board)):
        raise ActionIneligibleError
        
    # Importantly, the original board should be left unmodified: since Minimax will ultimately require considering many different 
    # board states during its computation. This means that simply updating a cell in board itself is not a correct implementation 
    # of the result function. You’ll likely want to make a deep copy of the board first before making any changes.
    tempBoard = copy.deepcopy(board)
    if(board[action[0]][action[1]] != EMPTY):
        raise ActionIneligibleError
    else:
        tempBoard[action[0]][action[1]] = player(board)
        
    return tempBoard



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # If one player fills a row, return that player's name
    for i, row in enumerate(board):
        if row == ["X", "X", "X"]:
            return X
        elif row == ["O", "O", "O"]:
            return O
                        
    # If one player fills a row, return that player's name
    for j in range(len(board)):
        if [x[j] for x in board] == ["X", "X", "X"]:
            return X
        elif [x[j] for x in board] == ["O", "O", "O"]:
            return O
    
    # If one player fills a diagonal line, return that player's name
    if [board[i][i] for i in range(len(board))] == ["X", "X", "X"]:
        return X
    elif [board[i][i] for i in range(len(board))] == ["O", "O", "O"]:
        return O

    if [board[i][len(board) - i - 1] for i in range(len(board))] == ["X", "X", "X"]:
        return X
    elif [board[i][len(board) - i - 1] for i in range(len(board))] == ["O", "O", "O"]:
        return O
    
    # If no winner, return None
    return None



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    movesLeft = sum(x.count(EMPTY) for x in board)
    if movesLeft == 0:
        return True
    return False if winner(board) == None else True # need to test


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    res = (winner(board))
    if res == X:
        return 1
    elif res == O:
        return -1
    else:
        return 0 
        


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # If the board is a terminal board, the minimax function should return None
    if terminal(board):
        return None

    # The move returned should be the optimal action (i, j) that is one of the allowable actions on the board. 
    # The maximizing player picks action a in Actions(s) that produces the highest value of Min-Value(Result(s, a)).
    if player(board) == X: 
        return maxValueAB(board)[1]
    # The minimizing player picks action a in Actions(s) that produces the lowest value of Max-Value(Result(s, a)).
    else:
        return minValueAB(board)[1]
    
    

    
def maxValueAB(board, parentThreshold = float("inf")):
    
    optAction = None
    # if Terminal(state), return Utility(state), else, return the max of min values
    if terminal(board): 
        #set_trace()
        return (utility(board), None)
    else:
        v = -float("inf")
        childThreshold = v
        for action in actions(board):
            v_original = v
            v = max(v, minValueAB(result(board, action), childThreshold)[0])
            # set_trace()
            if v > v_original:
                optAction = action
            #set_trace()
            if v > parentThreshold:
                return(v, optAction)
        return (v, optAction)


    
def minValueAB(board, parentThreshold = -float("inf")):
    
    optAction = None
    # if Terminal(state), return Utility(state), else, return the max of min values
    if terminal(board): 
        #set_trace()
        return (utility(board), None)
    else:
        v = float("inf")
        childThreshold = v
        for action in actions(board):
            v_original = v
            v = min(v, maxValueAB(result(board, action), childThreshold)[0])
            # set_trace()
            if v < v_original:
                optAction = action
            if v < parentThreshold:
                return(v, optAction)
        return (v, optAction)





