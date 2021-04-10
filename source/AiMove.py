import copy
from sys import maxsize
from source import BoardInterface
from PyQt5.QtCore import QThread, pyqtSignal
from source import PieceMoveInfo
from time import sleep
from math import sqrt


class AiMove(QThread):
    moveDetermined = pyqtSignal(PieceMoveInfo.PieceMoveInfo)
    aiSkipDetermined = pyqtSignal()

    def __init__(self, threadBoardInput, color):
        super(AiMove, self).__init__()
        self.MIN = -maxsize - 1
        self.MAX = maxsize
        self.MAXDEPTH = 2
        self.threadBoardInput = threadBoardInput
        self.color = color
        self.isRunning = True
        self.callsDebug = 0

    def stop(self):
        self.isRunning = False

    def run(self):
        self.nextMove(self.threadBoardInput, self.color)

    def checkAdditions(self, currentBoard, move):
        additionKing = 70
        additionBishop1 = 70
        additionBishop2 = 70

        if currentBoard.piecePosCopy[move.getFromPos()[1]][move.getFromPos()[0]].pieceColor == 0:
            additionKing = additionKing - (sqrt(
                pow((currentBoard.blackKingPosition[0] - move.getToPos()[0]), 2) + pow(
                    (currentBoard.blackKingPosition[1] - move.getToPos()[1]), 2)) * 10)

            if not currentBoard.blackBishop1Position == 0:
                additionBishop1 = additionBishop1 - (sqrt(
                    pow((currentBoard.blackBishop1Position[0] - move.getToPos()[0]), 2) + pow(
                        (currentBoard.blackBishop1Position[1] - move.getToPos()[1]), 2)) * 10)

            if not currentBoard.blackBishop2Position == 0:
                additionBishop2 = additionBishop2 - (sqrt(
                    pow((currentBoard.blackBishop2Position[0] - move.getToPos()[0]), 2) + pow(
                        (currentBoard.blackBishop2Position[1] - move.getToPos()[1]), 2)) * 10)
        else:
            additionKing = additionKing - (sqrt(
                pow((currentBoard.whiteKingPosition[0] - move.getToPos()[0]), 2) + pow(
                    (currentBoard.whiteKingPosition[1] - move.getToPos()[1]), 2)) * 10)

            if not currentBoard.whiteBishop1Position == 0:
                additionBishop1 = additionBishop1 - (sqrt(
                    pow((currentBoard.whiteBishop1Position[0] - move.getToPos()[0]), 2) + pow(
                        (currentBoard.whiteBishop1Position[1] - move.getToPos()[1]), 2)) * 10)

            if not currentBoard.whiteBishop2Position == 0:
                additionBishop2 = additionBishop2 - (sqrt(
                    pow((currentBoard.whiteBishop2Position[0] - move.getToPos()[0]), 2) + pow(
                        (currentBoard.whiteBishop2Position[1] - move.getToPos()[1]), 2)) * 10)
        return additionKing + additionBishop1 + additionBishop2

    def evaluate(self, currentBoard, caller):
        if caller == 0:
            val = currentBoard.valuesOfWhitePieces - currentBoard.valuesOfBlackPieces
        else:
            val = currentBoard.valuesOfBlackPieces - currentBoard.valuesOfWhitePieces

        return val

    def minimax(self, currentBoard, alpha, beta, currentDepth, turn, caller):
        self.callsDebug += 1
        if currentDepth == 0:
            moveToMake = 0

        nextTurn = 1
        if turn == 1:
            nextTurn = 0

        if currentDepth == self.MAXDEPTH:
            return self.evaluate(currentBoard, caller)

        if turn == caller:
            bestEval = self.MIN
            for move in currentBoard.getAllPossibleMoves(turn):
                if not move == 0:
                    currentBoard.makeMove(move)

                eval = self.minimax(currentBoard, alpha, beta, currentDepth + 1, nextTurn, caller)

                if not move == 0:
                    currentBoard.undoMove()

                if caller == 0:
                    if currentDepth == 0:
                        eval += self.checkAdditions(currentBoard, move)
                        if eval > bestEval:
                            bestEval = eval
                            moveToMake = move
                    elif eval > bestEval:
                        bestEval = eval

                    if bestEval > alpha:
                        alpha = bestEval
                else:
                    if currentDepth == 0:
                        eval += self.checkAdditions(currentBoard, move)
                        if eval >= bestEval:
                            bestEval = eval
                            moveToMake = move
                    elif eval >= bestEval:
                        bestEval = eval

                    if bestEval >= alpha:
                        alpha = bestEval

                if alpha >= beta:
                    break

            if currentDepth == 0:
                return moveToMake
            else:
                return bestEval

        else:
            bestEval = self.MAX
            for move in currentBoard.getAllPossibleMoves(turn):
                if not move == 0:
                    currentBoard.makeMove(move)

                eval = self.minimax(currentBoard, alpha, beta, currentDepth + 1, nextTurn, caller)

                if not move == 0:
                    currentBoard.undoMove()

                if caller == 0:
                    if currentDepth == 0:
                        eval += self.checkAdditions(currentBoard, move)
                        if eval < bestEval:
                            bestEval = eval
                            moveToMake = move
                    elif eval < bestEval:
                        bestEval = eval

                    if bestEval < beta:
                        beta = bestEval
                else:
                    if currentDepth == 0:
                        eval += self.checkAdditions(currentBoard, move)
                        if eval <= bestEval:
                            bestEval = eval
                            moveToMake = move
                    elif eval <= bestEval:
                        bestEval = eval

                    if bestEval <= beta:
                        beta = bestEval

                if beta <= alpha:
                    break

            if currentDepth == 0:
                return moveToMake
            else:
                return bestEval

    def nextMove(self, currentBoard, color):
        if self.isRunning:
            print("Ai Trigger")
            currentBoard.getValuesOfPieces()
            currentBoard.updateKingPositions()
            alpha = self.MIN
            beta = self.MAX

            currentDepth = 0

            overallBestMove = self.minimax(currentBoard, alpha, beta, currentDepth, color, color)

            print(self.callsDebug)

            sleep(2)

        while self.isRunning and currentBoard.getPaused():
            sleep(2)

        if self.isRunning:
            if overallBestMove == 0 and len(currentBoard.getAllPossibleMoves(color)) == 1:
                self.moveDetermined.emit(currentBoard.getAllPossibleMoves(color)[0])
            elif overallBestMove == 0:
                self.aiSkipDetermined.emit()
            else:
                self.moveDetermined.emit(overallBestMove)

    #def getCopy(self, currentBoard):
        # TODO get copy of currentBoard
    #    return currentBoard
        #return copy.deepcopy(currentBoard)
    """
    def valuePiece(self, board, yIter, xIter):
        # return the value of pieces
        if board.piecePosCopy[yIter][xIter].pieceType == "knight":
            return 6 + board.piecePosCopy[yIter][xIter].knightSpecial
        elif board.piecePosCopy[yIter][xIter].pieceType == "king":
            return 30
        elif board.piecePosCopy[yIter][xIter].pieceType == "queen":
            return 10
        elif board.piecePosCopy[yIter][xIter].pieceType == "bishop":
            return 6
        elif board.piecePosCopy[yIter][xIter].pieceType == "rook":
            return 8
        else:
            return 1

    def eval(self, board, yIter, xIter):
        # return the value of piece and the position
        val = self.valuePiece(board, yIter, xIter)
        res = 1
        # is position of an attack
        #if yIter // 4 != board.piecePosCopy[yIter][xIter].pieceColor:
        #    res += 1

        if board.getTurn() == 0:
            if yIter <= 3:
                res += 1
        else:
            if yIter >= 4:
                res += 1

        # is center
        if 2 <= xIter < 6:
            res += 1
        return res * val

    def evaluate(self, board):
        score = 0

        xIter = 0
        yIter = 0
        for row in board.piecePosCopy:
            for tile in row:
                # If the tile has a piece...
                if not board.piecePosCopy[yIter][xIter] == "0":
                    val = 0
                    val += board.getMovesRemaining()[board.piecePosCopy[yIter][xIter].pieceCommander]
                    val += self.eval(board, yIter, xIter)
                    if not board.piecePosCopy[yIter][xIter].pieceColor == board.getTurn():
                        val *= -1
                    score += val
                xIter += 1
            xIter = 0
            yIter += 1

        return score

    def minimax(self, currentBoard, alpha, beta, depth):
        # test is game over
        gameOver = currentBoard.isGameOver()
        if (gameOver > 0):
            if (gameOver == 1):
                return self.MAX
            elif gameOver == 2:
                return self.MIN
            return 0

        if depth == self.MAXDEPTH:
            return self.evaluate(currentBoard)

        best = 0
        if currentBoard.getTurn() == 1:
            best = self.MIN
        else:
            best = self.MAX

        for move in currentBoard.getAllPossibleMoves():
            copyOfBoard = BoardInterface.BoardInterface(currentBoard.mainBoard)
            copyOfBoard.updatePiecePosCopy(currentBoard.piecePosCopy)
            copyOfBoard.makeMove(move)

            val = self.minimax(copyOfBoard, alpha, beta, depth + 1)

            if currentBoard.getTurn() == 1:
                best = max(best, val)
                alpha = max(best, alpha)
            else:
                best = min(best, val)
                beta = min(best, beta)

            if beta <= alpha:
                break

        return best

    def nextMove(self, currentBoard):
        print("Ai Trigger")
        best = self.MIN
        alpha = self.MIN
        beta = self.MAX
        bestmove = 0
        for move in currentBoard.getAllPossibleMoves():
            copyOfBoard = BoardInterface.BoardInterface(currentBoard.mainBoard)
            copyOfBoard.updatePiecePosCopy(currentBoard.piecePosCopy)
            copyOfBoard.makeMove(move)

            val = self.minimax(copyOfBoard, alpha, beta, 0)

            if (val > best):
                bestmove = move
            best = max(best, val)
            alpha = max(best, alpha)
            if beta <= alpha:
                break

        sleep(2)

        while currentBoard.getPaused():
            sleep(2)

        if bestmove == 0 and len(currentBoard.getAllPossibleMoves()) == 1:
            self.moveDetermined.emit(currentBoard.getAllPossibleMoves()[0])
        elif bestmove == 0:
            self.aiSkipDetermined.emit()
        else:
            self.moveDetermined.emit(bestmove)
    """



