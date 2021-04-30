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

        self.whiteKingPieceCount = 0
        self.whiteBishop1PieceCount = 0
        self.whiteBishop2PieceCount = 0

        self.blackKingPieceCount = 0
        self.blackBishop1PieceCount = 0
        self.blackBishop2PieceCount = 0

        self.turnCount = 0

        # TODO return 0 if not game over and 1 is black win and 2 white win and 3 is tie
    def isGameOver(self):
        return 0

    def valuePiece(self, modifier, pieceType):
        # Return a value based on the piece and the given modifier.
        if pieceType == "knight":
            return 300 * modifier
        elif pieceType == "king":
            return 1200 * modifier
        elif pieceType == "queen":
            return 900 * modifier
        elif pieceType == "bishop":
            return 1200 * modifier
        elif pieceType == "rook":
            return 500 * modifier
        else:
            return 100 * modifier

    def valuePieceDefendAndAttack(self, pieceTypeAttack, pieceTypeDefend):
        # Used to find the value of a piece based on what piece is attacking what.
        if pieceTypeAttack == "knight":
            if pieceTypeDefend == "king" or pieceTypeDefend == "queen":
                return self.valuePiece(1 / 6, pieceTypeDefend)
            elif pieceTypeDefend == "rook":
                return self.valuePiece(2 / 6, pieceTypeDefend)
            elif pieceTypeDefend == "knight" or pieceTypeDefend == "bishop":
                return self.valuePiece(3 / 6, pieceTypeDefend)
            else:
                return self.valuePiece(5 / 6, pieceTypeDefend)
        elif pieceTypeAttack == "king":
            if pieceTypeDefend == "king" or pieceTypeDefend == "queen" or pieceTypeDefend == "knight" or \
                    pieceTypeDefend == "bishop":
                return self.valuePiece(3 / 6, pieceTypeDefend)
            elif pieceTypeDefend == "rook":
                return self.valuePiece(2 / 6, pieceTypeDefend)
            else:
                return self.valuePiece(6 / 6, pieceTypeDefend)
        elif pieceTypeAttack == "queen":
            if pieceTypeDefend == "king" or pieceTypeDefend == "queen" or pieceTypeDefend == "knight" or \
                    pieceTypeDefend == "bishop":
                return self.valuePiece(3 / 6, pieceTypeDefend)
            elif pieceTypeDefend == "rook":
                return self.valuePiece(2 / 6, pieceTypeDefend)
            else:
                return self.valuePiece(5 / 6, pieceTypeDefend)
        elif pieceTypeAttack == "bishop":
            if pieceTypeDefend == "king" or pieceTypeDefend == "queen" or pieceTypeDefend == "knight" or \
                    pieceTypeDefend == "rook":
                return self.valuePiece(2 / 6, pieceTypeDefend)
            elif pieceTypeDefend == "bishop":
                return self.valuePiece(3 / 6, pieceTypeDefend)
            else:
                return self.valuePiece(4 / 6, pieceTypeDefend)
        elif pieceTypeAttack == "rook":
            if pieceTypeDefend == "king" or pieceTypeDefend == "queen":
                return self.valuePiece(3 / 6, pieceTypeDefend)
            elif pieceTypeDefend == "rook":
                return self.valuePiece(1 / 6, pieceTypeDefend)
            else:
                return self.valuePiece(2 / 6, pieceTypeDefend)
        else:
            if pieceTypeDefend == "king" or pieceTypeDefend == "queen" or pieceTypeDefend == "knight" or \
                    pieceTypeDefend == "rook":
                return self.valuePiece(1 / 6, pieceTypeDefend)
            elif pieceTypeDefend == "bishop":
                return self.valuePiece(2 / 6, pieceTypeDefend)
            else:
                return self.valuePiece(3 / 6, pieceTypeDefend)

    def updateKingPositions(self):
        # Reset all position and piece counts
        self.whiteKingPosition = 0
        self.whiteBishop1Position = 0
        self.whiteBishop2Position = 0

        self.blackKingPosition = 0
        self.blackBishop1Position = 0
        self.blackBishop2Position = 0

        self.whiteKingPieceCount = 0
        self.whiteBishop1PieceCount = 0
        self.whiteBishop2PieceCount = 0

        self.blackKingPieceCount = 0
        self.blackBishop1PieceCount = 0
        self.blackBishop2PieceCount = 0

        xIter = 0
        yIter = 0

        # For all tiles...
        for row in self.piecePosCopy:
            for tile in row:
                piece = self.piecePosCopy[yIter][xIter]
                # If the tile is a piece...
                if not piece == "0":
                    # If they are a king, update their position
                    if piece.pieceType == "king":
                        if piece.pieceColor == 0:
                            self.whiteKingPosition = [xIter, yIter]
                        else:
                            self.blackKingPosition = [xIter, yIter]
                    # If they are a bishop, update their position
                    elif piece.pieceType == "bishop":
                        if piece.pieceColor == 0:
                            if piece.pieceCommander == 0:
                                self.whiteBishop1Position = [xIter, yIter]
                            else:
                                self.whiteBishop2Position = [xIter, yIter]
                        else:
                            if piece.pieceCommander == 0:
                                self.blackBishop1Position = [xIter, yIter]
                            else:
                                self.blackBishop2Position = [xIter, yIter]

                    # If the piece is white, add it to the appropriate piece count.
                    if piece.pieceColor == 0:
                        if piece.pieceCommander == 0:
                            self.whiteBishop1PieceCount += 1
                        elif piece.pieceCommander == 1:
                            self.whiteKingPieceCount += 1
                        else:
                            self.whiteBishop2PieceCount += 1
                    # If the piece is black, add it to the appropriate piece count.
                    else:
                        if piece.pieceCommander == 0:
                            self.blackBishop1PieceCount += 1
                        elif piece.pieceCommander == 1:
                            self.blackKingPieceCount += 1
                        else:
                            self.blackBishop2PieceCount += 1
                xIter += 1
            xIter = 0
            yIter += 1

    def getValuesOfPieces(self):
        # Reset the vales for the white and black sides.
        self.valuesOfWhitePieces = 0
        self.valuesOfBlackPieces = 0
        xIter = 0
        yIter = 0

        # For the tiles on the board...
        for row in self.piecePosCopy:
            for tile in row:
                piece = self.piecePosCopy[yIter][xIter]
                # If they are a piece...
                if not piece == "0":
                    # If they are a white piece, add its value to white's side.
                    if not piece.pieceColor == 0:
                        self.valuesOfWhitePieces += self.valuePiece(1, piece.pieceType)
                    # If they are a white piece, add its value to black's side.
                    else:
                        self.valuesOfBlackPieces += self.valuePiece(1, piece.pieceType)
                xIter += 1
            xIter = 0
            yIter += 1

    # Determine all moves that are currently possible.
    def movesPossible(self, turn, callingCommander):
        self.allPossibleMoves = []
        xIter = 0
        yIter = 0

        for row in self.piecePosCopy:
            for tile in row:
                piece = self.piecePosCopy[yIter][xIter]
                # If the tile has a piece...
                if not piece == "0":
                    # If the piece belongs to the current player...
                    if piece.pieceColor == turn and \
                            (piece.pieceCommander == callingCommander or callingCommander == -1):
                        # If the piece's commander has a command point remaining...
                        if (turn == 0 and
                            self.mainBoard.getWhiteTurnsRemaining()[piece.pieceCommander] == 1) \
                                or (turn == 1 and
                                    self.mainBoard.getBlackTurnsRemaining()[piece.pieceCommander] == 1) \
                                or (callingCommander == 1 and not piece.pieceType == "king"):
                            if piece.pieceType == "knight":
                                self.checkAppendMoves(-5, 6, xIter, yIter, piece)
                            elif piece.pieceType == "king":
                                self.checkAppendMoves(-3, 4, xIter, yIter, piece)
                            elif piece.pieceType == "queen":
                                self.checkAppendMoves(-3, 4, xIter, yIter, piece)
                            elif piece.pieceType == "bishop":
                                self.checkAppendMoves(-1, 2, xIter, yIter, piece)
                            elif piece.pieceType == "rook":
                                self.checkAppendMoves(-3, 4, xIter, yIter, piece)
                            else:
                                self.checkAppendMoves(-1, 2, xIter, yIter, piece)
                        # If the piece is a knight and has a special move remaining...
                        elif piece.pieceType == "knight" and piece.knightSpecial:
                            for yCord in range(-1, 2):
                                for xCord in range(-1, 2):
                                    # Make sure we are not out of bounds.
                                    if not (xCord == 0 and yCord == 0) and \
                                            not (xIter + xCord < 0 or xIter + xCord > 7) and \
                                            not (yIter + yCord < 0 or yIter + yCord > 7):
                                        # If there is a piece to attack...
                                        if piece.rules.checkAttackInRange(self, [xIter, yIter],
                                                                          [xIter + xCord, yIter + yCord],
                                                                          piece.pieceColor) and \
                                                not self.piecePosCopy[yIter + yCord][xIter + xCord] == "0" and \
                                                not piece.pieceColor == \
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
    def checkAppendMoves(self, lowerMove, upperMove, xIter, yIter, piece):
        for yCord in range(lowerMove, upperMove):
            for xCord in range(lowerMove, upperMove):
                # Make sure we are not out of bounds.
                if not (xCord == 0 and yCord == 0) and \
                        not (xIter + xCord < 0 or xIter + xCord > 7) and \
                        not (yIter + yCord < 0 or yIter + yCord > 7):
                    # If path is free...
                    if len(piece.rules.isPathFree(self, [xIter, yIter], [xIter + xCord, yIter + yCord],
                            piece.pieceColor, self.piecePosCopy)):
                        # Append move.
                        self.allPossibleMoves.append(PieceMoveInfo.PieceMoveInfo(
                            [xIter, yIter], [xIter + xCord, yIter + yCord]))
                    # If there is a piece to attack...
                    elif piece.rules.checkAttackInRange(self, [xIter, yIter], [xIter + xCord, yIter + yCord],
                                                        piece.pieceColor) and \
                            not self.piecePosCopy[yIter + yCord][xIter + xCord] == "0" and \
                            not piece.pieceColor == self.piecePosCopy[yIter + yCord][xIter + xCord].pieceColor:
                        # Append move.
                        self.allPossibleMoves.append(PieceMoveInfo.PieceMoveInfo(
                            [xIter, yIter], [xIter + xCord, yIter + yCord]))

    # Gets the array of all possible moves that exist.
    def getAllPossibleMoves(self, turn, callingCommander):
        # TODO if possible add special move is to end to turn
        self.movesPossible(turn, callingCommander)
        return self.allPossibleMoves

    # Moves a piece.
    def makeMove(self, move):
        if not self.piecePosCopy[move.getFromPos()[1]][move.getFromPos()[0]] == "0":
            # Remove points as the pieces are removed.
            if not self.piecePosCopy[move.getToPos()[1]][move.getToPos()[0]] == "0":
                if self.piecePosCopy[move.getToPos()[1]][move.getToPos()[0]].pieceColor == 0:
                    self.valuesOfWhitePieces -= self.valuePieceDefendAndAttack(
                        self.piecePosCopy[move.getFromPos()[1]][move.getFromPos()[0]].pieceType,
                        self.piecePosCopy[move.getToPos()[1]][move.getToPos()[0]].pieceType)
                else:
                    self.valuesOfBlackPieces -= self.valuePieceDefendAndAttack(
                        self.piecePosCopy[move.getFromPos()[1]][move.getFromPos()[0]].pieceType,
                        self.piecePosCopy[move.getToPos()[1]][move.getToPos()[0]].pieceType)
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
        if not self.piecePosCopy[move.getToPos()[1]][move.getToPos()[0]] == "0":

            # Copy this piece to destination.
            self.piecePosCopy[move.getFromPos()[1]][move.getFromPos()[0]] = \
                self.piecePosCopy[move.getToPos()[1]][move.getToPos()[0]]

            # Remove it from the previous position.
            self.piecePosCopy[move.getToPos()[1]][move.getToPos()[0]] = \
                self.deletedElements.pop(len(self.deletedElements) - 1)

            # Add points as the pieces are added back.
            if not self.piecePosCopy[move.getToPos()[1]][move.getToPos()[0]] == "0":
                if self.piecePosCopy[move.getToPos()[1]][move.getToPos()[0]].pieceColor == 0:
                    self.valuesOfWhitePieces += self.valuePieceDefendAndAttack(
                        self.piecePosCopy[move.getFromPos()[1]][move.getFromPos()[0]].pieceType,
                        self.piecePosCopy[move.getToPos()[1]][move.getToPos()[0]].pieceType)
                else:
                    self.valuesOfBlackPieces += self.valuePieceDefendAndAttack(
                        self.piecePosCopy[move.getFromPos()[1]][move.getFromPos()[0]].pieceType,
                        self.piecePosCopy[move.getToPos()[1]][move.getToPos()[0]].pieceType)

            # Remove command point.
            if not self.piecePosCopy[move.getFromPos()[1]][move.getFromPos()[0]].knightSpecial:
                if self.piecePosCopy[move.getFromPos()[1]][move.getFromPos()[0]].pieceColor == 0:
                    self.whiteMovesRemaining[
                        self.piecePosCopy[move.getFromPos()[1]][move.getFromPos()[0]].pieceCommander] = 1
                else:
                    self.blackMovesRemaining[
                        self.piecePosCopy[move.getFromPos()[1]][move.getFromPos()[0]].pieceCommander] = 1

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

    # Updates how many moves the white has remaining.
    def updateWhiteTurnsRemaining(self):
        self.whiteMovesRemaining = self.mainBoard.getWhiteTurnsRemaining().copy()

    # Updates how many moves the black has remaining.
    def updateBlackTurnsRemaining(self):
        self.blackMovesRemaining = self.mainBoard.getBlackTurnsRemaining().copy()

    # Updates the number of turns that have elapsed in the game.
    def updateTurnCount(self):
        self.turnCount += 1

    # Returns who's turn it is.
    def getTurn(self):
        return self.mainBoard.getTurn()

    # Returns all movements made form the start of the game.
    def getMoveHistory(self):
        return self.mainBoard.getMoveHistory()

    # Get if the game is paused
    def getPaused(self):
        return self.mainBoard.getPaused()
