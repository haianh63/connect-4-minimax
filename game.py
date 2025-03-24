import numpy as np
import math

BOARD_ROW = 6
BOARD_COL = 7
HUMAN_PIECE = 1
AI_PIECE = 2
EVALUATING_BOARD = np.array([[3, 4, 5, 7, 5, 4, 3],
                             [4, 6, 8, 10, 8, 6, 4],
                             [5, 7, 11, 13, 11, 7, 5],
                             [5, 7, 11, 13, 11, 7, 5],
                             [4, 6, 8, 10, 8, 6, 4],
                             [3, 4, 5, 7, 5, 4, 3]])

def isWinning(board, piece):
    for r in range(0, BOARD_ROW):
        for c in range(0, BOARD_COL - 3):
            if (board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece):
                return True

    for r in range(0, BOARD_ROW - 3):
        for c in range(0, BOARD_COL):
            if (board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece):
                return True

    for r in range(0, BOARD_ROW - 3):
        for c in range(0, BOARD_COL - 3):
            if (board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece):
                return True

    for r in range(0, BOARD_ROW - 3):
        for c in range(3, BOARD_COL):
            if (board[r][c] == piece and board[r + 1][c - 1] == piece and board[r + 2][c - 2] == piece and board[r + 3][c - 3] == piece):
                return True
    return False
            
def getValidPositions(board):
    validPositions = []
    for col in range(0, BOARD_COL):
        if board[0][col] == 0:
            validPositions.append(col)
    return validPositions
    
def isRunOutMove(board):
    return len(getValidPositions(board)) == 0

def dropPiece(board, col, piece):
    for row in range(BOARD_ROW - 1, -1, -1):
        if board[row][col] == 0:
            board[row][col] = piece
            break

def evaluatingFunction(board):
    human_score = np.sum(EVALUATING_BOARD[board == HUMAN_PIECE])
    ai_score = np.sum(EVALUATING_BOARD[board == AI_PIECE])

    return ai_score - human_score

def minimax(board, depth, maximizingPlayer):
    if depth == 0:
        return (None, evaluatingFunction(board))
    elif isWinning(board, AI_PIECE):
        return (None, math.inf)
    elif isWinning(board, HUMAN_PIECE):
        return (None, -math.inf)
    elif isRunOutMove(board):
        return (None, 0)
    validPositions = getValidPositions(board)
    if maximizingPlayer:
        maxEval = -math.inf
        column = validPositions[0]
        for col in validPositions:
            new_board = np.copy(board)
            dropPiece(new_board, col, AI_PIECE)
            eval = minimax(new_board, depth - 1, False)[1]
            if eval > maxEval:
                maxEval = eval
                column = col
        return (column, maxEval)
    else:
        minEval = math.inf
        column = validPositions[0]
        for col in validPositions:
            new_board = np.copy(board)
            dropPiece(new_board, col, HUMAN_PIECE)
            eval = minimax(new_board, depth - 1, True)[1]
            if eval < minEval:
                minEval = eval
                column = col
            
        return (column, minEval)
    
def minimax(board, depth, alpha, beta, maximizingPlayer):
    if depth == 0:
        return (None, evaluatingFunction(board))
    elif isWinning(board, AI_PIECE):
        return (None, math.inf)
    elif isWinning(board, HUMAN_PIECE):
        return (None, -math.inf)
    elif isRunOutMove(board):
        return (None, 0)
    validPositions = getValidPositions(board)
    if maximizingPlayer:
        maxEval = -math.inf
        column = validPositions[0]
        for col in validPositions:
            new_board = np.copy(board)
            dropPiece(new_board, col, AI_PIECE)
            eval = minimax(new_board, depth - 1, alpha, beta, False)[1]
            if eval > maxEval:
                maxEval = eval
                column = col
            alpha = max(alpha, maxEval)
            if beta <= alpha:
                break
        return (column, maxEval)
    else:
        minEval = math.inf
        column = validPositions[0]
        for col in validPositions:
            new_board = np.copy(board)
            dropPiece(new_board, col, HUMAN_PIECE)
            eval = minimax(new_board, depth - 1, alpha, beta, True)[1]
            if eval < minEval:
                minEval = eval
                column = col
            beta = min(beta, minEval)
            if beta <= alpha:
                break
        return (column, minEval)