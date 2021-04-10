from source import PieceMoveInfo
import copy

class BoardInterface:
    def __init__(self, mainBoard):
        super(BoardInterface, self).__init__()
        
        self.mainBoard = mainBoard
        self.piecePosCopy = [["0", "0", "0", "0", "0", "0", "0", "0"],
                             ["0", "0", "0", "0", "0", "0", "0", "0"],
                             ["0", "0", "0", "0", "0", "0", "0", "0"],
                             ["0", "0", "0", "0", "0", "0", "0", "0"],
                             ["0", "0", "0", "0", "0", "0", "0", "0"],
                             ["0", "0", "0", "0", "0", "0", "0", "0"],
                             ["0", "0", "0", "0", "0", "0", "0", "0"],
                             ["0", "0", "0", "0", "0", "0", "0", "0"]]
        self.allPossibleMoves = []
        self.whiteMovesRemaining = [1, 1, 1]
        self.blackMovesRemaining = [1, 1, 1]
        self.deletedElements = []
        self.movesMade = []
        self.valuesOfWhitePieces = 0
        self.valuesOfBlackPieces = 0

        self.whiteKingPosition = 0
        self.whiteBishop1Position = 0
        self.whiteBishop2Position = 0

        self.blackKingPosition = 0
        self.blackBishop1Position = 0
        self.blackBishop2Position = 0

        # TODO return 0 if not game over and 1 is black win and 2 white win and 3 is tie
    def isGameOver(self):
        return 0

    def valuePiece(self, pieceType):
        if pieceType == "knight":
            return 300
        elif pieceType == "king":
            return 1500
        elif pieceType == "queen":
            return 900
        elif pieceType == "bishop":
            return 1500
        elif pieceType == "rook":
            return 500
        else:
            return 100

    def updateKingPositions(self):
        self.whiteKingPosition = 0
        self.whiteBishop1Position = 0
        self.whiteBishop2Position = 0

        self.blackKingPosition = 0
        self.blackBishop1Position = 0
        self.blackBishop2Position = 0

        whiteBishop = 0
        blackBishop = 0
        xIter = 0
        yIter = 0

        for row in self.piecePosCopy:
            for tile in row:
                if not self.piecePosCopy[yIter][xIter] == "0":
                    if self.piecePosCopy[yIter][xIter].pieceType == "king":
                        if self.piecePosCopy[yIter][xIter].pieceColor == 0:
                            self.whiteKingPosition = [xIter, yIter]
                        else:
                            self.blackKingPosition = [xIter, yIter]
                    elif self.piecePosCopy[yIter][xIter].pieceType == "bishop":
                        if self.piecePosCopy[yIter][xIter].pieceColor == 0:
                            if whiteBishop == 0:
                                self.whiteBishop1Position = [xIter, yIter]
                                whiteBishop = 1
                            else:
                                self.whiteBishop2Position = [xIter, yIter]
                        else:
                            if blackBishop == 0:
                                self.blackBishop1Position = [xIter, yIter]
                                blackBishop = 1
                            else:
                                self.blackBishop2Position = [xIter, yIter]
                xIter += 1
            xIter = 0
            yIter += 1

    def getValuesOfPieces(self):
        self.valuesOfWhitePieces = 0
        self.valuesOfBlackPieces = 0
        xIter = 0
        yIter = 0

        for row in self.piecePosCopy:
            for tile in row:
                if not self.piecePosCopy[yIter][xIter] == "0":
                    if not self.piecePosCopy[yIter][xIter].pieceColor == 0:
                        self.valuesOfWhitePieces += self.valuePiece(self.piecePosCopy[yIter][xIter].pieceType)
                    else:
                        self.valuesOfBlackPieces += self.valuePiece(self.piecePosCopy[yIter][xIter].pieceType)
                xIter += 1
            xIter = 0
            yIter += 1

    # Determine all moves that are currently possible.
    def movesPossible(self, turn):
        self.allPossibleMoves = []
        xIter = 0
        yIter = 0

        for row in self.piecePosCopy:
            for tile in row:
                # If the tile has a piece...
                if not self.piecePosCopy[yIter][xIter] == "0":
                    # If the piece belongs to the current player...
                    if self.piecePosCopy[yIter][xIter].pieceColor == turn:
                        # If the piece's commander has a command point remaining...
                        if (turn == 0 and
                            self.mainBoard.getWhiteTurnsRemaining()[self.piecePosCopy[yIter][xIter].pieceCommander] == 1) \
                                or (turn == 1 and
                                    self.mainBoard.getBlackTurnsRemaining()[self.piecePosCopy[yIter][xIter].pieceCommander] == 1):
                            if self.piecePosCopy[yIter][xIter].pieceType == "knight":
                                self.checkAppendMoves(-5, 6, xIter, yIter)
                            elif self.piecePosCopy[yIter][xIter].pieceType == "king":
                                self.checkAppendMoves(-3, 4, xIter, yIter)
                            elif self.piecePosCopy[yIter][xIter].pieceType == "queen":
                                self.checkAppendMoves(-3, 4, xIter, yIter)
                            elif self.piecePosCopy[yIter][xIter].pieceType == "bishop":
                                self.checkAppendMoves(-1, 2, xIter, yIter)
                            elif self.piecePosCopy[yIter][xIter].pieceType == "rook":
                                self.checkAppendMoves(-3, 4, xIter, yIter)
                            else:
                                self.checkAppendMoves(-1, 2, xIter, yIter)
                        # If the piece is a knight and has a special move remaining...
                        elif self.piecePosCopy[yIter][xIter].pieceType == "knight" and \
                                self.piecePosCopy[yIter][xIter].knightSpecial:
                            for yCord in range(-1, 2):
                                for xCord in range(-1, 2):
                                    # Make sure we are not out of bounds.
                                    if not (xCord == 0 and yCord == 0) and \
                                            not (xIter + xCord < 0 or xIter + xCord > 7) and \
                                            not (yIter + yCord < 0 or yIter + yCord > 7):
                                        # If there is a piece to attack...
                                        if self.piecePosCopy[yIter][xIter].rules.checkAttackInRange(
                                                self, [xIter, yIter], [xIter + xCord, yIter + yCord],
                                                self.piecePosCopy[yIter][xIter].pieceColor) and not \
                                                self.piecePosCopy[yIter + yCord][xIter + xCord] == "0" and not \
                                                self.piecePosCopy[yIter][xIter].pieceColor == \
                                                self.piecePosCopy[yIter + yCord][xIter + xCord].pieceColor and not \
                                                self.piecePosCopy[yIter + yCord][xIter + xCord].pieceType == "king" \
                                                and not self.piecePosCopy[yIter + yCord][xIter + xCord].pieceType == \
                                                        "queen":
                                            # Append move.
                                            self.allPossibleMoves.append(PieceMoveInfo.PieceMoveInfo(
                                                [xIter, yIter], [xIter + xCord, yIter + yCord]))
                xIter += 1
            xIter = 0
            yIter += 1

    # Check if the move should be added.
    def checkAppendMoves(self, lowerMove, upperMove, xIter, yIter):
        for yCord in range(lowerMove, upperMove):
            for xCord in range(lowerMove, upperMove):
                # Make sure we are not out of bounds.
                if not (xCord == 0 and yCord == 0) and \
                        not (xIter + xCord < 0 or xIter + xCord > 7) and \
                        not (yIter + yCord < 0 or yIter + yCord > 7):
                    # If path is free...
                    if len(self.piecePosCopy[yIter][xIter].rules.isPathFree(
                            self, [xIter, yIter], [xIter + xCord, yIter + yCord],
                            self.piecePosCopy[yIter][xIter].pieceColor, self.piecePosCopy)):
                        # Append move.
                        self.allPossibleMoves.append(PieceMoveInfo.PieceMoveInfo(
                            [xIter, yIter], [xIter + xCord, yIter + yCord]))
                    # If there is a piece to attack...
                    elif self.piecePosCopy[yIter][xIter].rules.checkAttackInRange(
                            self, [xIter, yIter], [xIter + xCord, yIter + yCord],
                            self.piecePosCopy[yIter][xIter].pieceColor) and not \
                            self.piecePosCopy[yIter + yCord][xIter + xCord] == "0" and not \
                            self.piecePosCopy[yIter][xIter].pieceColor == \
                            self.piecePosCopy[yIter + yCord][xIter + xCord].pieceColor:
                        # Append move.
                        self.allPossibleMoves.append(PieceMoveInfo.PieceMoveInfo(
                            [xIter, yIter], [xIter + xCord, yIter + yCord]))

    # Gets the array of all possible moves that exist.
    def getAllPossibleMoves(self, turn):
        # TODO if possible add special move is to end to turn
        self.movesPossible(turn)
        return self.allPossibleMoves

    # Moves a piece.
    def makeMove(self, move):
        if not self.piecePosCopy[move.getToPos()[1]][move.getToPos()[0]] == "0":
            if self.piecePosCopy[move.getToPos()[1]][move.getToPos()[0]].pieceColor == 0:
                self.valuesOfWhitePieces -= \
                    self.valuePiece(self.piecePosCopy[move.getToPos()[1]][move.getToPos()[0]].pieceType)
            else:
                self.valuesOfBlackPieces -= \
                    self.valuePiece(self.piecePosCopy[move.getToPos()[1]][move.getToPos()[0]].pieceType)
        self.deletedElements.append(self.piecePosCopy[move.getToPos()[1]][move.getToPos()[0]])
        self.movesMade.append(move)

        # Copy this piece to destination.
        self.piecePosCopy[move.getToPos()[1]][move.getToPos()[0]] = \
            self.piecePosCopy[move.getFromPos()[1]][move.getFromPos()[0]]

        # Remove it from the previous position.
        self.piecePosCopy[move.getFromPos()[1]][move.getFromPos()[0]] = "0"

        # Remove command point.
        if self.piecePosCopy[move.getToPos()[1]][move.getToPos()[0]].pieceColor == 0:
            self.whiteMovesRemaining[self.piecePosCopy[move.getToPos()[1]][move.getToPos()[0]].pieceCommander] = 0
        else:
            self.blackMovesRemaining[self.piecePosCopy[move.getToPos()[1]][move.getToPos()[0]].pieceCommander] = 0

    # Moves a piece back.
    def undoMove(self):
        move = self.movesMade.pop(len(self.movesMade) - 1)

        # Copy this piece to destination.
        self.piecePosCopy[move.getFromPos()[1]][move.getFromPos()[0]] = \
            self.piecePosCopy[move.getToPos()[1]][move.getToPos()[0]]

        # Remove it from the previous position.
        self.piecePosCopy[move.getToPos()[1]][move.getToPos()[0]] = \
            self.deletedElements.pop(len(self.deletedElements) - 1)

        if not self.piecePosCopy[move.getToPos()[1]][move.getToPos()[0]] == "0":
            if self.piecePosCopy[move.getToPos()[1]][move.getToPos()[0]].pieceColor == 0:
                self.valuesOfWhitePieces += \
                    self.valuePiece(self.piecePosCopy[move.getToPos()[1]][move.getToPos()[0]].pieceType)
            else:
                self.valuesOfBlackPieces += \
                    self.valuePiece(self.piecePosCopy[move.getToPos()[1]][move.getToPos()[0]].pieceType)

        # Remove command point.
        if not self.piecePosCopy[move.getFromPos()[1]][move.getFromPos()[0]].knightSpecial:
            if self.piecePosCopy[move.getFromPos()[1]][move.getFromPos()[0]].pieceColor == 0:
                self.whiteMovesRemaining[self.piecePosCopy[move.getFromPos()[1]][move.getFromPos()[0]].pieceCommander] \
                    = 1
            else:
                self.blackMovesRemaining[self.piecePosCopy[move.getFromPos()[1]][move.getFromPos()[0]].pieceCommander] \
                    = 1

    # Returns the piece position array.
    def updatePiecePosCopy(self, board):
        xIter = 0
        yIter = 0

        for row in board:
            for tile in row:
                self.piecePosCopy[yIter][xIter] = tile
                xIter += 1
            xIter = 0
            yIter += 1

    # Returns how many moves the white has remaining.
    def updateWhiteTurnsRemaining(self):
        self.whiteMovesRemaining = self.mainBoard.getWhiteTurnsRemaining().copy()

    # Returns how many moves the black has remaining.
    def updateBlackTurnsRemaining(self):
        self.blackMovesRemaining = self.mainBoard.getBlackTurnsRemaining().copy()

    # Returns who's turn it is.
    def getTurn(self):
        return self.mainBoard.getTurn()

    # Returns all movements made form the start of the game.
    def getMoveHistory(self):
        return self.mainBoard.getMoveHistory()

    # Get if the game is paused
    def getPaused(self):
        return self.mainBoard.getPaused()
