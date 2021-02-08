from math import sqrt
from math import floor
import random
import sys


class Knight:
    def isPathFree(self, start, end, color, piecePos, nodeArr):
        return checkPath(start, end, piecePos, nodeArr, 5)

    def checkAttackInRange(self, start, end, color):
        return checkAttackDistance(start, end, 1)

    def checkKnightSpecialInRange(self, end, color, piecePos):
        specialPossible = False
        for yCord in range(-1, 2):
            for xCord in range(-1, 2):
                if not piecePos[end[1] + yCord][end[0] + xCord] == "0" and \
                        not piecePos[end[1] + yCord][end[0] + xCord].pieceColor == color:
                    specialPossible = True
        return specialPossible

    def rollCapture(self, end, piecePos):
        return rollDie(Knight.minRollNeeded(self, piecePos[end[1]][end[0]].pieceType))

    def rollCaptureSpecial(self, end, piecePos):
        return rollDieSpecial(Knight.minRollNeeded(self, piecePos[end[1]][end[0]].pieceType))

    def minRollNeeded(self, pieceToAttack):
        if pieceToAttack == "king" or pieceToAttack == "queen":
            return 6
        elif pieceToAttack == "rook":
            return 5
        elif pieceToAttack == "bishop" or pieceToAttack == "knight":
            return 4
        else:
            return 2

class King:
    def isPathFree(self, start, end, color, piecePos, nodeArr):
        return checkPath(start, end, piecePos, nodeArr, 3)

    def checkAttackInRange(self, start, end, color):
        return checkAttackDistance(start, end, 1)

    def rollCapture(self, end, piecePos):
        return rollDie(King.minRollNeeded(self, piecePos[end[1]][end[0]].pieceType))

    def minRollNeeded(self, pieceToAttack):
        if pieceToAttack == "rook":
            return 5
        elif pieceToAttack == "king" or pieceToAttack == "queen" or \
                pieceToAttack == "knight" or pieceToAttack == "bishop":
            return 4
        else:
            return 1


class Queen:
    def isPathFree(self, start, end, color, piecePos, nodeArr):
        return checkPath(start, end, piecePos, nodeArr, 3)

    def checkAttackInRange(self, start, end, color):
        return checkAttackDistance(start, end, 1)

    def rollCapture(self, end, piecePos):
        return rollDie(Queen.minRollNeeded(self, piecePos[end[1]][end[0]].pieceType))

    def minRollNeeded(self, pieceToAttack):
        if pieceToAttack == "rook":
            return 5
        elif pieceToAttack == "king" or pieceToAttack == "queen" or \
                pieceToAttack == "knight" or pieceToAttack == "bishop":
            return 4
        else:
            return 2


class Bishop:
    def isPathFree(self, start, end, color, piecePos, nodeArr):
        # Make sure the bishop is moving towards enemy lines
        if movingDir(color, start, end):
            return checkPath(start, end, piecePos, nodeArr, 1)
        else:
            return False

    def checkAttackInRange(self, start, end, color):
        # Make sure the pawn is attacking towards enemy lines
        if movingDir(color, start, end):
            return checkAttackDistance(start, end, 1)
        else:
            return False

    def rollCapture(self, end, piecePos):
        return rollDie(Bishop.minRollNeeded(self, piecePos[end[1]][end[0]].pieceType))


    def minRollNeeded(self, pieceToAttack):
        if pieceToAttack == "king" or pieceToAttack == "queen" or \
                pieceToAttack == "knight" or pieceToAttack == "rook":
            return 5
        elif pieceToAttack == "bishop":
            return 4
        else:
            return 3


class Pawn:
    def isPathFree(self, start, end, color, piecePos, nodeArr):
        # Make sure the pawn is moving towards enemy lines
        if movingDir(color, start, end):
            return checkPath(start, end, piecePos, nodeArr, 1)
        else:
            return False

    def checkAttackInRange(self, start, end, color):
        # Make sure the pawn is attacking towards enemy lines
        if movingDir(color, start, end):
            return checkAttackDistance(start, end, 1)
        else:
            return False

    def rollCapture(self, end, piecePos):
        return rollDie(Pawn.minRollNeeded(self, piecePos[end[1]][end[0]].pieceType))

    def minRollNeeded(self, pieceToAttack):
        if pieceToAttack == "king" or pieceToAttack == "queen" or \
                pieceToAttack == "knight" or pieceToAttack == "rook":
            return 6
        elif pieceToAttack == "bishop":
            return 5
        else:
            return 4


class Rook:
    def isPathFree(self, start, end, color, piecePos, nodeArr):
        return checkPath(start, end, piecePos, nodeArr, 1)

    def checkAttackInRange(self, start, end, color):
        return checkAttackDistance(start, end, 3)

    def rollCapture(self, end, piecePos):
        return rollDie(Rook.minRollNeeded(self, piecePos[end[1]][end[0]].pieceType))

    def minRollNeeded(self, pieceToAttack):
        if pieceToAttack == "rook":
            return 6
        elif pieceToAttack == "knight" or pieceToAttack == "bishop" or \
                pieceToAttack == "pawn":
            return 5
        else:
            return 4


def checkAttackDistance(start, end, maxDist):
    # Can be simplified. Like this for debugging.
    print(str(abs(end[0] - start[0])) + " " + str(abs(end[1] - start[1])))
    if abs(end[0] - start[0]) <= maxDist and abs(end[1] - start[1]) <= maxDist:
        return True
    else:
        return False


def rollDie(rollRequired):
    # Can be simplified. Like this for debugging.
    isCaptureSuccessful = False
    tempInt = random.randint(1, 6)
    print("Roll of " + str(rollRequired) + " needed. Rolled " + str(tempInt))
    if tempInt >= rollRequired:
        isCaptureSuccessful = True
    return isCaptureSuccessful


def rollDieSpecial(rollRequired):
    # Can be simplified. Like this for debugging.
    isCaptureSuccessful = False
    tempInt = random.randint(1, 6)
    tempIntSub = tempInt - 1
    print("Roll of " + str(rollRequired) + " needed. Rolled " + str(tempInt) + ". Roll modified to " + str(tempIntSub))
    if tempIntSub >= rollRequired:
        isCaptureSuccessful = True
    return isCaptureSuccessful


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
                            floor(distance([currentSquare[0] + xCord, currentSquare[1] + yCord],
                            [currentSquare[0], currentSquare[1]]) * 10) + nodeArr[currentSquare[1]][currentSquare[0]][1]
                        distFromEnd = \
                            floor(distance([currentSquare[0] + xCord, currentSquare[1] + yCord], end) * 10)
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


def distance(start, end):
    if start[0] == end[0]:
        value = abs(end[1] - start[1])
    elif start[1] == end[1]:
        value = abs(end[0] - start[0])
    else:
        # Use if doesn't work numpy.linarg(start - end)
        value = sqrt(pow((end[0] - start[0]), 2) + pow((end[1] - start[1]), 2))
    return value
