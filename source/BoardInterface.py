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

    # TODO return 0 if not game over and 1 is black win and 2 white win and 3 is tie
    def isGameOver(self):
        return 0

    # Determine all moves that are currently possible.
    def movesPossible(self):
        self.allPossibleMoves = []
        xIter = 0
        yIter = 0

        for row in self.piecePosCopy:
            for tile in row:
                # If the tile has a piece...
                if not self.piecePosCopy[yIter][xIter] == "0":
                    # If the piece belongs to the current player...
                    if self.piecePosCopy[yIter][xIter].pieceColor == self.getTurn():
                        # If the piece's commander has a command point remaining...
                        if self.getMovesRemaining()[self.piecePosCopy[yIter][xIter].pieceCommander] == 1:
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
                    if self.piecePosCopy[yIter][xIter].rules.isPathFree(
                            self, [xIter, yIter], [xIter + xCord, yIter + yCord],
                            self.piecePosCopy[yIter][xIter].pieceColor, self.piecePosCopy):
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
    def getAllPossibleMoves(self):
        # TODO if possible add special move is to end to turn
        self.movesPossible()
        return self.allPossibleMoves

    # Calls the movePiece function of the board.
    def makeMove(self, move):
        # Copy this piece to destination.
        self.piecePosCopy[move.getToPos()[1]][move.getToPos()[0]] = \
            self.piecePosCopy[move.getFromPos()[1]][move.getFromPos()[0]]

        # Remove it from the previous position.
        self.piecePosCopy[move.getFromPos()[1]][move.getFromPos()[0]] = "0"

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

    # Returns how many moves the player has remaining.
    def getMovesRemaining(self):
        return self.mainBoard.getPlayerTurnsRemaining()

    # Returns who's turn it is.
    def getTurn(self):
        return self.mainBoard.getTurn()

    # Returns all movements made form the start of the game.
    def getMoveHistory(self):
        return self.mainBoard.getMoveHistory()
