import random
import time
import ChessEngine as CE

# Các bảng điểm
pieceScore = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "p": 1}

knightScores = [[1, 1, 1, 1, 1, 1, 1, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]]

bishopScores = [[4, 3, 2, 1, 1, 2, 3, 4],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [4, 3, 2, 1, 1, 2, 3, 4]]

queenScores = [[1, 1, 1, 3, 1, 1, 1, 1],
               [1, 2, 3, 3, 3, 1, 1, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 1, 2, 3, 3, 1, 1, 1],
               [1, 1, 1, 3, 1, 1, 1, 1]]

rookScores = [[4, 3, 4, 4, 4, 4, 3, 4],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [1, 1, 2, 3, 3, 2, 1, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 1, 2, 3, 3, 2, 1, 1],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [4, 3, 4, 4, 4, 4, 3, 4]]

whitePawnScores = [[8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [0, 0, 0, 0, 0, 0, 0, 0]]

blackPawnScores = [[0, 0, 0, 0, 0, 0, 0, 0],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8]]

piecePositionScores = {
    "N": knightScores,
    "Q": queenScores,
    "B": bishopScores,
    "R": rookScores,
    "bp": blackPawnScores,
    "wp": whitePawnScores
}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3

# Tìm nước đi ngẫu nhiên
def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]
# Sắp xếp nước đi theo thứ tự ưu tiên
def findBestMove(gs, validMoves):
    global nextMove
    tempCastleRight = CE.CastleRight(gs.currentCastlingRight.wks,gs.currentCastlingRight.bks,
                                           gs.currentCastlingRight.wqs,gs.currentCastlingRight.bqs)
    nextMove = None
    validMoves = moveOrdering(gs,validMoves)
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE,  CHECKMATE, 1 if gs.whiteToMove else -1)
    gs.currentCastlingRight = tempCastleRight
    return nextMove      

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth,alpha, beta, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        nextMoves = moveOrdering(gs,nextMoves)
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1,-beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore> alpha :
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore


# Chấm điểm bàn cờ
def scoreBoard(gs):
    if gs.checkMate:
        return -CHECKMATE if gs.whiteToMove else CHECKMATE
    if gs.staleMate:
        return STALEMATE

    score = 0
    for r in range(8):
        for c in range(8):
            piece = gs.board[r][c]
            if piece != "--":
                piecePositionScore = 0
                if piece[1] != "K":
                    if piece[1] == 'p':
                        piecePositionScore = piecePositionScores[piece][r][c]
                    else:
                        piecePositionScore = piecePositionScores[piece[1]][r][c]
                if piece[0] == 'w':
                    score += pieceScore[piece[1]] + 0.1 * piecePositionScore
                else:
                    score -= pieceScore[piece[1]] + 0.1 * piecePositionScore
    return score
def moveOrdering(gs, validMoves):
    # Tạo một danh sách để lưu trữ điểm số cho mỗi nước đi
    moveScores = []
    winningCapture = 0.8
    losingCapture = 0.2

    # Tính toán điểm số cho mỗi nước đi
    for move in validMoves:
        gs.makeMove(move)
        # Điểm số cơ bản dựa trên bảng điểm hiện tại
        score = scoreBoard(gs)
        gs.undoMove()

        # Thêm điểm thưởng hoặc phạt dựa trên các yếu tố khác
        if move.isCapture:
        
            score += pieceScore[move.pieceCaptured[1]]
        if move.isPawnPromotion:
            # Thêm điểm nếu là nước thăng cấp
            score += 1  # Giả sử thăng cấp được 1 điểm thưởng

        moveScores.append(score)

    # Sắp xếp các nước đi dựa trên điểm số, từ cao xuống thấp
    sortedMoves = [move for _, move in sorted(zip(moveScores, validMoves), key=lambda pair: pair[0], reverse=True)]

    return sortedMoves
# Kiểm tra nước đi có an toàn không
def is_move_safe(gs, move):
    gs.makeMove(move)
    opponent_moves = gs.getValidMoves()
    gs.undoMove()
    for opp_move in opponent_moves:
        if opp_move.endRow == move.endRow and opp_move.endCol == move.endCol:
            return False
    return True
