from sys import maxsize
from PyQt5.QtCore import QThread, pyqtSignal
from source import PieceMoveInfo
import random


class AiBrain(QThread):
    foundBestMove = pyqtSignal(PieceMoveInfo.PieceMoveInfo)
    noMove = pyqtSignal()

    def __init__(self, currentBoard, color, callingCommander):
        super(AiBrain, self).__init__()
        self.MIN = -maxsize - 1
        self.MAX = maxsize
        self.MAXDEPTH = 1
        self.currentBoard = currentBoard
        self.color = color
        self.callingCommander = callingCommander
        self.isRunning = True

    def stop(self):
        self.isRunning = False

    def run(self):
        self.findBestMove()

    def subtractVariance(self, startPos, endPos):
        if abs(startPos[0] - endPos[0]) < abs(startPos[1] - endPos[1]):
            return (abs(startPos[0] - endPos[0]) * 10)
        else:
            return (abs(startPos[1] - endPos[1]) * 10)

    def evaluateSingleMove(self, currentBoard, move):
        overallValue = 0
        additionKing = 140
        additionBishop1 = 140
        additionBishop2 = 140

        if currentBoard.turnCount < 2:
            overallValue += random.randint(0, 20)

        # Subtract smallest variance
        overallValue -= self.subtractVariance(move.getFromPos(), move.getToPos())

        # If the piece is white...
        if currentBoard.piecePosCopy[move.getFromPos()[1]][move.getFromPos()[0]].pieceColor == 0:
            # Get value for distance to black king...
            additionKing -= ((abs(currentBoard.blackKingPosition[0] - move.getToPos()[0]) +
                                            abs(currentBoard.blackKingPosition[1] - move.getToPos()[1])) * 10)

            # If the black bishop1 exists...
            if not currentBoard.blackBishop1Position == 0:
                # Get value for distance to black bishop1...
                additionBishop1 -= ((abs(currentBoard.blackBishop1Position[0] - move.getToPos()[0]) +
                                     abs(currentBoard.blackBishop1Position[1] - move.getToPos()[1])) * 10)
            # Else return 0
            else:
                additionBishop1 = 0

            # If the black bishop2 exists...
            if not currentBoard.blackBishop2Position == 0:
                # Get value for distance to black bishop2...
                additionBishop2 -= ((abs(currentBoard.blackBishop2Position[0] - move.getToPos()[0]) +
                                     abs(currentBoard.blackBishop2Position[1] - move.getToPos()[1])) * 10)
            # Else return 0
            else:
                additionBishop2 = 0
        # If the piece is black...
        else:
            # Get value for distance to white king...
            additionKing -= ((abs(currentBoard.whiteKingPosition[0] - move.getToPos()[0]) +
                              abs(currentBoard.whiteKingPosition[1] - move.getToPos()[1])) * 10)

            # If the white bishop1 exists...
            if not currentBoard.whiteBishop1Position == 0:
                # Get value for distance to white bishop1...
                additionBishop1 -= ((abs(currentBoard.whiteBishop1Position[0] - move.getToPos()[0]) +
                                     abs(currentBoard.whiteBishop1Position[1] - move.getToPos()[1])) * 10)
            # Else return 0
            else:
                additionBishop1 = 0

            # If the white bishop2 exists...
            if not currentBoard.whiteBishop2Position == 0:
                # Get value for distance to white bishop2...
                additionBishop2 -= ((abs(currentBoard.whiteBishop2Position[0] - move.getToPos()[0]) +
                                     abs(currentBoard.whiteBishop2Position[1] - move.getToPos()[1])) * 10)
            # Else return 0
            else:
                additionBishop2 = 0

        # Add the distance to the closest command piece to the overall value.
        if additionBishop1 > additionKing and additionBishop1 > additionBishop2:
            overallValue += additionBishop1
        elif additionBishop2 > additionKing and additionBishop2 > additionBishop1:
            overallValue += additionBishop2
        else:
            overallValue += additionKing

        return overallValue

    def evaluateAllMoves(self, currentBoard, turn, caller):
        if self.isRunning:
            bestEval = self.MIN

            for move in currentBoard.getAllPossibleMoves(turn, self.callingCommander):
                eval = 0

                if caller == 0:
                    eval += self.evaluateSingleMove(currentBoard, move)
                    if eval > bestEval:
                        bestEval = eval
                        moveToMake = move
                else:
                    eval += self.evaluateSingleMove(currentBoard, move)
                    if eval >= bestEval:
                        bestEval = eval
                        moveToMake = move

            if bestEval == self.MIN:
                return 0
            else:
                moveToMake.setValue(bestEval)
                return moveToMake

    def findBestMove(self):
        if self.isRunning:
            # Set up alpha, beta, and the value of pieces.
            self.currentBoard.getValuesOfPieces()

            bestMove = self.evaluateAllMoves(self.currentBoard, self.color, self.color)

        if self.isRunning:
            # If the AI cannot make a move, emit that.
            if bestMove == 0:
                self.noMove.emit()
            # If the AI can make a move, emit it.
            else:
                print("Val = " + str(bestMove.getValue()))
                self.foundBestMove.emit(bestMove)
