from sys import maxsize
from PyQt5.QtCore import QThread, pyqtSignal
from source import PieceMoveInfo
from math import sqrt


class AiBrain(QThread):
    foundBestMove = pyqtSignal(PieceMoveInfo.PieceMoveInfo)
    noMove = pyqtSignal()

    def __init__(self, currentBoard, color, callingCommander):
        super(AiBrain, self).__init__()
        self.MIN = -maxsize - 1
        self.MAX = maxsize
        self.MAXDEPTH = 2
        self.currentBoard = currentBoard
        self.color = color
        self.callingCommander = callingCommander
        self.isRunning = True

    def stop(self):
        self.isRunning = False

    def run(self):
        self.findBestMove()

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
        if self.isRunning:
            if currentDepth == 0:
                moveToMake = 0

            nextTurn = 1
            if turn == 1:
                nextTurn = 0

            if currentDepth == self.MAXDEPTH:
                return self.evaluate(currentBoard, caller)

            if turn == caller:
                bestEval = self.MIN
                for move in currentBoard.getAllPossibleMoves(turn, self.callingCommander):
                    if self.isRunning:
                        currentBoard.makeMove(move)
                    else:
                        return 0

                    eval = self.minimax(currentBoard, alpha, beta, currentDepth + 1, nextTurn, caller)

                    if self.isRunning:
                        currentBoard.undoMove()
                    else:
                        return 0

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
                    if bestEval == self.MIN:
                        return 0
                    else:
                        moveToMake.setValue(bestEval)
                        return moveToMake

                else:
                    return bestEval

            else:
                bestEval = self.MAX
                for move in currentBoard.getAllPossibleMoves(turn, -1):
                    if self.isRunning:
                        currentBoard.makeMove(move)
                    else:
                        return 0

                    eval = self.minimax(currentBoard, alpha, beta, currentDepth + 1, nextTurn, caller)

                    if self.isRunning:
                        currentBoard.undoMove()
                    else:
                        return 0

                    if caller == 0:
                        if eval < bestEval:
                            bestEval = eval

                        if bestEval < beta:
                            beta = bestEval
                    else:
                        if eval <= bestEval:
                            bestEval = eval

                        if bestEval <= beta:
                            beta = bestEval

                    if beta <= alpha:
                        break

                return bestEval

    def findBestMove(self):
        if self.isRunning:
            print("Ai Trigger")
            self.currentBoard.getValuesOfPieces()
            self.currentBoard.updateKingPositions()
            alpha = self.MIN
            beta = self.MAX

            currentDepth = 0

            bestMove = self.minimax(self.currentBoard, alpha, beta, currentDepth, self.color, self.color)

        if self.isRunning:
            if bestMove == 0:
                self.noMove.emit()
            else:
                self.foundBestMove.emit(bestMove)
