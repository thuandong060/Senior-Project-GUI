from ChessRule import piece
from math import floor
import sys


class Knight:
    def isPathFree(self, start, end, color, piecePos, nodeArr):
        return checkPath(start, end, piecePos, nodeArr, 5)

    # This code might be changed drastically
    def minRollNeeded(self, pieceToAttack):
        if pieceToAttack.pieceType == "king" or pieceToAttack.pieceType == "queen" or \
                pieceToAttack.pieceType == "knight" or pieceToAttack.pieceType == "rook" or \
                pieceToAttack.pieceType == "bishop" or pieceToAttack.pieceType == "pawn":
            return 6
        if pieceToAttack.pieceType == "knight" or pieceToAttack.pieceType == "rook" or \
                pieceToAttack.pieceType == "bishop" or pieceToAttack.pieceType == "pawn":
            return 5
        if pieceToAttack.pieceType == "bishop" or pieceToAttack.pieceType == "knight" or \
                pieceToAttack.pieceType == "pawn":
            return 4
        if pieceToAttack.pieceType == "pawn":
            return 3 or 2


class King:
    def isPathFree(self, start, end, color, piecePos, nodeArr):
        return checkPath(start, end, piecePos, nodeArr, 3)

    # This code might be changed drastically
    @staticmethod
    def minRollNeeded(pieceToAttack):
        if pieceToAttack.pieceType == "king" or pieceToAttack.pieceType == "queen" or \
                pieceToAttack.pieceType == "knight" or pieceToAttack.pieceType == "rook" \
                or pieceToAttack.pieceType == "bishop" or pieceToAttack.pieceType == "pawn":
            return 6
        if pieceToAttack.pieceType == "king" or pieceToAttack.pieceType == "queen" or \
                pieceToAttack.pieceType == "knight" or pieceToAttack.pieceType == "rook" or \
                pieceToAttack.pieceType == "bishop" or pieceToAttack.pieceType == "pawn":
            return 5
        if pieceToAttack.pieceType == "king" or pieceToAttack.pieceType == "queen" or \
                pieceToAttack.pieceType == "knight" or pieceToAttack.pieceType == "bishop" or \
                pieceToAttack.pieceType == "pawn":
            return 4
        if pieceToAttack.pieceType == "pawn":
            return 3 or 2 or 1


class Queen:
    def isPathFree(self, start, end, color, piecePos, nodeArr):
        return checkPath(start, end, piecePos, nodeArr, 3)

    # This code might be changed drastically
    @staticmethod
    def minRollNeeded(pieceToAttack):
        if pieceToAttack.pieceType == "king" or pieceToAttack.pieceType == "queen" or \
                pieceToAttack.pieceType == "knight" or pieceToAttack.pieceType == "rook" or \
                pieceToAttack.pieceType == "bishop" or pieceToAttack.pieceType == "pawn":
            return 6
        if pieceToAttack.pieceType == "king" or pieceToAttack.pieceType == "queen" or \
                pieceToAttack.pieceType == "knight" or pieceToAttack.pieceType == "rook" or \
                pieceToAttack.pieceType == "bishop" or pieceToAttack.pieceType == "pawn":
            return 5
        if pieceToAttack.pieceType == "king" or pieceToAttack.pieceType == "queen" or \
                pieceToAttack.pieceType == "knight" or pieceToAttack.pieceType == "bishop" or \
                pieceToAttack.pieceType == "pawn":
            return 4
        if pieceToAttack.pieceType == "pawn":
            return 3 or 2


class Bishop:
    def isPathFree(self, start, end, color, piecePos, nodeArr):
        # Make sure the bishop is moving towards enemy lines
        if movingDir(color, start, end):
            return checkPath(start, end, piecePos, nodeArr, 1)
        else:
            return False

    # This code might be changed drastically
    @staticmethod
    def minRollNeeded(pieceToAttack):
        if pieceToAttack.pieceType == "king" or pieceToAttack.pieceType == "queen" or \
                pieceToAttack.pieceType == "knight" or pieceToAttack.pieceType == "rook" or \
                pieceToAttack.pieceType == "bishop" or pieceToAttack.pieceType == "pawn":
            return 6 or 5
        if pieceToAttack.pieceType == "bishop" or pieceToAttack.pieceType == "pawn":
            return 4
        if pieceToAttack.pieceType == "pawn":
            return 3


class Pawn:
    def isPathFree(self, start, end, color, piecePos, nodeArr):
        # Make sure the pawn is moving towards enemy lines
        if movingDir(color, start, end):
            return checkPath(start, end, piecePos, nodeArr, 1)
        else:
            return False

    # This code might be changed drastically
    @staticmethod
    def minRollNeeded(pieceToAttack):
        if pieceToAttack.pieceType == "king" or pieceToAttack.pieceType == "queen" or \
                pieceToAttack.pieceType == "knight" or pieceToAttack.pieceType == "rook" or \
                pieceToAttack.pieceType == "bishop" or pieceToAttack.pieceType == "pawn":
            return 6
        if pieceToAttack.pieceType == "bishop" or pieceToAttack.pieceType == "pawn":
            return 5
        if pieceToAttack.pieceType == "pawn":
            return 4


class Rook:
    def isPathFree(self, start, end, color, piecePos, nodeArr):
        return checkPath(start, end, piecePos, nodeArr, 1)

    # This code might be changed drastically
    @staticmethod
    def minRollNeeded(pieceToAttack):
        if pieceToAttack.pieceType == "king" or pieceToAttack.pieceType == "queen" or \
                pieceToAttack.pieceType == "knight" or pieceToAttack.pieceType == "rook" or \
                pieceToAttack.pieceType == "bishop" or pieceToAttack.pieceType == "pawn":
            return 6
        if pieceToAttack.pieceType == "king" or pieceToAttack.pieceType == "queen" or \
                pieceToAttack.pieceType == "knight" or pieceToAttack.pieceType == "bishop" or \
                pieceToAttack.pieceType == "pawn":
            return 5
        if pieceToAttack.pieceType == "king" or pieceToAttack.pieceType == "queen":
            return 4


def checkPath(start, end, piecePos, nodeArr, maxMoves):
    currentSquare = start
    nodeArr[start[1]][start[0]] = [1, 0, 0, 0]
    pathLength = 0
    while True:
        nextSquare = 0
        blockedIn = True
        xIter = 0
        yIter = 0

        # Check all eight squares around the current square and set their weights appropriately.
        for yCord in range(-1, 2):
            for xCord in range(-1, 2):
                if not (xCord == 0 and yCord == 0) and \
                        not (currentSquare[0] + xCord < 0 or currentSquare[0] + xCord > 7) and \
                        not (currentSquare[1] + yCord < 0 or currentSquare[1] + yCord > 7):
                    if piecePos[currentSquare[1] + yCord][currentSquare[0] + xCord] == "0" and \
                            not nodeArr[currentSquare[1] + yCord][currentSquare[0] + xCord][0] == 1:
                        distFromStart = \
                            floor(piece.piece.distance([currentSquare[0] + xCord, currentSquare[1] + yCord],
                            [currentSquare[0], currentSquare[1]]) * 10) + nodeArr[currentSquare[1]][currentSquare[0]][1]
                        distFromEnd = \
                            floor(piece.piece.distance([currentSquare[0] + xCord, currentSquare[1] + yCord], end) * 10)
                        if nodeArr[currentSquare[1] + yCord][currentSquare[0] + xCord][1] == 0 or \
                                distFromStart < nodeArr[currentSquare[1] + yCord][currentSquare[0] + xCord][0]:
                            nodeArr[currentSquare[1] + yCord][currentSquare[0] + xCord] = \
                                [0, distFromStart, distFromEnd, distFromStart + distFromEnd]

        # Check all tiles on the board for the one with the next lowest cost.
        for row in nodeArr:
            for tile in row:
                if nextSquare == 0 and not nodeArr[yIter][xIter][3] == sys.maxsize and \
                        not nodeArr[yIter][xIter][0] == 1:
                    blockedIn = False
                    nextSquare = [xIter, yIter]
                elif not nodeArr[yIter][xIter][3] == sys.maxsize and not nodeArr[yIter][xIter][0] == 1 and \
                        nodeArr[yIter][xIter][3] <= nodeArr[nextSquare[1]][nextSquare[0]][3]:
                    if nodeArr[yIter][xIter][3] == nodeArr[nextSquare[1]][nextSquare[0]][3]:
                        if nodeArr[yIter][xIter][2] <= nodeArr[nextSquare[1]][nextSquare[0]][2]:
                            blockedIn = False
                            nextSquare = [xIter, yIter]
                    else:
                        blockedIn = False
                        nextSquare = [xIter, yIter]
                xIter += 1
            xIter = 0
            yIter += 1

        # Break if a next square could not be found
        if nextSquare == 0:
            break

        # Set the current tile to the one with the next lowest cost.
        nodeArr[nextSquare[1]][nextSquare[0]][0] = 1
        currentSquare = nextSquare

        # If the algorithm has reached its destination, trace back the path taken to determine if it is possible
        # for the current piece to make this movement.
        if currentSquare == end:
            while not currentSquare == start:
                for yCord in range(-1, 2):
                    for xCord in range(-1, 2):
                        if not (xCord == 0 and yCord == 0) and \
                                not (currentSquare[0] + xCord < 0 or currentSquare[0] + xCord > 7) and \
                                not (currentSquare[1] + yCord < 0 or currentSquare[1] + yCord > 7):
                            if nextSquare == currentSquare and \
                                    nodeArr[currentSquare[1] + yCord][currentSquare[0] + xCord][0] == 1:
                                nextSquare = [currentSquare[0] + xCord, currentSquare[1] + yCord]
                            elif nodeArr[currentSquare[1] + yCord][currentSquare[0] + xCord][3] <= \
                                    nodeArr[nextSquare[1]][nextSquare[0]][3] and \
                                    nodeArr[currentSquare[1] + yCord][currentSquare[0] + xCord][0] == 1:
                                nextSquare = [currentSquare[0] + xCord, currentSquare[1] + yCord]
                pathLength += 1
                nodeArr[currentSquare[1]][currentSquare[0]][0] = 2
                currentSquare = nextSquare

            # If this path is longer than the max moves of the piece, the movement is invalid.
            if pathLength > maxMoves:
                break

            # If the path is within the movement area of the piece, the movement is valid.
            resetBoard(nodeArr)
            return True

        # If the path is longer than the max moves or the piece was not able to find a new square to check,
        # the movement is invalid.
        if pathLength > maxMoves or blockedIn:
            break

    # If the program breaks from the loop, the movement is not possible.
    resetBoard(nodeArr)
    return False


def resetBoard(nodeArr):
    # Print is a debug statement.
    print(str(nodeArr[0]) + "\n"\
          + str(nodeArr[1]) + "\n"\
          + str(nodeArr[2]) + "\n"\
          + str(nodeArr[3]) + "\n"\
          + str(nodeArr[4]) + "\n"\
          + str(nodeArr[5]) + "\n"\
          + str(nodeArr[6]) + "\n"\
          + str(nodeArr[7]) + "\n\n")
    # Go through the pathfinding board and change all tiles back to their default values.
    xIter = 0
    yIter = 0

    for row in nodeArr:
        for tile in row:
            nodeArr[yIter][xIter] = [0, 0, 0, sys.maxsize]
            xIter += 1
        xIter = 0
        yIter += 1


def movingDir(color, start, end):
    # Uses the color of a restricted movement piece to make sure it is moving in the right direction.
    if color == 0 and end[1] < start[1]:
        return True
    elif color == 1 and end[1] > start[1]:
        return True
    else:
        return False
