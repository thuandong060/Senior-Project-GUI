import numpy
import PiecesType
from source import main
import piece


class Knight(piece):
    def _init_(self, start, end, Piecetype):
        start = super().startingPosition
        end = super().endingPosition
        Piecetype = PiecesType.Knight
        val = 0.0
        if start == end:
            return False
        if start.x == end.x:
            val = abs(end.y - start.y)
        elif start.y == end.y:
            val = abs(end.x - start.x)
        else:
            val = numpy.linarg(start - end)

        if val <= 5:
            return True
        else:
            return False

    def minRollNeeded(self, pieceToAttack):
        if pieceToAttack == PiecesType.King or pieceToAttack == PiecesType.Queen or pieceToAttack == PiecesType.Knight or pieceToAttack == PiecesType.Rook or pieceToAttack == PiecesType.Bishop or pieceToAttack == PiecesType.Pawn:
            return 6
        if pieceToAttack == PiecesType.Knight or pieceToAttack == PiecesType.Rook or pieceToAttack == PiecesType.Bishop or pieceToAttack == PiecesType.Pawn:
            return 5
        if pieceToAttack == PiecesType.Bishop or pieceToAttack == PiecesType.Knight or pieceToAttack == PiecesType.Pawn:
            return 4
        if pieceToAttack == PiecesType.Pawn:
            return 3 or 2

    def isPathFree(self, start, end):
        start = super().startingPosition
        end = super().endingPosition
        if start.x == end.x and start.y > end.y:
            for i in range(start.y - 1, end.y):
                if main.pieceSet[i][start.x] != "0":
                    return True
        elif start.x < end.x and start.y == end.y:
            for i in range(start.x + 1, end.x):
                if main.pieceSet[start.y][i] != "0":
                    return True
        elif start.x == end.x and start.y < end.y:
            for i in range(start.y + 1, end.y):
                if main.pieceSet[i][start.x] != "0":
                    return False
        elif start.x > end.x and start.y == end.y:
            for i in range(start.x - 1, end.x, -1):
                if main.pieceSet[start.y][i] != "0":
                    return False

        elif start.x < end.x and start.y > end.y:
            for i in range(end.x - start.x, 0, -1):
                if main.pieceSet[start.x + i][start.y - i] != "0":
                    return False

        elif start.x < end.x and start.y < end.y:
            for row in range(start.x + 1, end.x):
                for column in range(start.y + 1, end.y):
                    if main.pieceSet[row][column] != "0":
                        return False

        elif start.x > end.x and start.y < end.y:
            for row in range(start.x - 1, end.x, -1):
                for column in range(start.y + 1, end.y):
                    if main.pieceSet[row][column] != "0":
                        return False

        elif start.x > end.x and start.y > end.y:
            for row in range(start.x - 1, end.x, -1):
                for column in range(start.y - 1, end.y, -1):
                    if main.pieceSet[row][column] != "0":
                        return False
