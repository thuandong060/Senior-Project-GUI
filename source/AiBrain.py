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
        print("Evaluating move FROM: " + str(move.getFromPos()) + " TO: " + str(move.getToPos()))

        overallValue = 0
        additionKing = 80
        additionBishop1 = 80
        additionBishop2 = 80
        piece = currentBoard.piecePosCopy[move.getFromPos()[1]][move.getFromPos()[0]]

        # Subtract smallest variance
        overallValue -= self.subtractVariance(move.getFromPos(), move.getToPos())

        # Random opening moves
        if currentBoard.turnCount < 2:
            if not piece.pieceType == "pawn":
                overallValue -= 80

            overallValue += random.randint(0, 80)
        else:
            if piece.pieceType == "queen":
                overallValue += 30

            if piece.pieceType == "rook":
                overallValue += 10

            if piece.pieceType == "knight":
                overallValue += 20

        # Add bonuses for moving certain piece types
        if currentBoard.turnCount < 6:
            if piece.pieceType == "rook":
                overallValue += 50

        # If the piece is white...
        if piece.pieceColor == 0:
            # Discourage king and bishops from moving while it has pieces
            if piece.pieceType == "king":
                overallValue -= currentBoard.whiteKingPieceCount * 10

            if piece.pieceType == "bishop" and piece.pieceCommander == 0:
                overallValue -= currentBoard.whiteBishop1PieceCount * 10

            if piece.pieceType == "bishop" and piece.pieceCommander == 2:
                overallValue -= currentBoard.whiteBishop2PieceCount * 10

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
            # Discourage king and bishops from moving while it has pieces
            if piece.pieceType == "king":
                overallValue -= currentBoard.blackKingPieceCount * 10

            if piece.pieceType == "bishop" and piece.pieceCommander == 0:
                overallValue -= currentBoard.blackBishop1PieceCount * 10

            if piece.pieceType == "bishop" and piece.pieceCommander == 2:
                overallValue -= currentBoard.blackBishop2PieceCount * 10

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
                if caller == 0:
                    eval = self.evaluateSingleMove(currentBoard, move)
                    if eval > bestEval:
                        bestEval = eval
                        moveToMake = move
                else:
                    eval = self.evaluateSingleMove(currentBoard, move)
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
