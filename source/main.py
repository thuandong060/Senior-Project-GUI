import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtCore import Qt
from ChessRule import piece


class chessBoardWindow(QMainWindow):
    def __init__(self):
        super(chessBoardWindow, self).__init__()
        # This block sets up the window properties.
        self.setGeometry(400, 200, 300, 300)
        self.setWindowTitle('Chessboard')

        # 0 for white, 1 for black
        self.turn = 0
        self.moveIndicator = QLabel(self)

        # Shows remaining moves.
        self.remainingMoveIndicator = QLabel(self)

        # Shows game info.
        self.moveInfoIndicator = QLabel(self)

        # Shows when the game is won.
        self.gameWinner = QLabel(self)

        # Button so you can skip your turn.
        self.skipButton = QPushButton("End Turn", self)

        # The basic unit of measurement for the board.
        self.tileSize = 0
        self.boardSize = 0

        self.playerTurnsRemaining = [1, 1, 1]
        self.knightSpecialMovesRemaining = 0
        self.gameOver = False
        self.winner = 0

        # Holds initial setup commands for the board.
        self.tileSet = [["wt", "bt", "wt", "bt", "wt", "bt", "wt", "bt"],
                        ["bt", "wt", "bt", "wt", "bt", "wt", "bt", "wt"],
                        ["wt", "bt", "wt", "bt", "wt", "bt", "wt", "bt"],
                        ["bt", "wt", "bt", "wt", "bt", "wt", "bt", "wt"],
                        ["wt", "bt", "wt", "bt", "wt", "bt", "wt", "bt"],
                        ["bt", "wt", "bt", "wt", "bt", "wt", "bt", "wt"],
                        ["wt", "bt", "wt", "bt", "wt", "bt", "wt", "bt"],
                        ["bt", "wt", "bt", "wt", "bt", "wt", "bt", "wt"]]

        # Holds labels for the tiles on the board.
        self.tilePos = [["0", "0", "0", "0", "0", "0", "0", "0"],
                        ["0", "0", "0", "0", "0", "0", "0", "0"],
                        ["0", "0", "0", "0", "0", "0", "0", "0"],
                        ["0", "0", "0", "0", "0", "0", "0", "0"],
                        ["0", "0", "0", "0", "0", "0", "0", "0"],
                        ["0", "0", "0", "0", "0", "0", "0", "0"],
                        ["0", "0", "0", "0", "0", "0", "0", "0"],
                        ["0", "0", "0", "0", "0", "0", "0", "0"]]

        # Holds initial setup commands for the pieces.
        self.pieceSet = [["br", "bk", "bb", "bki", "bq", "bb", "bk", "br"],
                         ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                         ["0", "0", "0", "0", "0", "0", "0", "0"],
                         ["0", "0", "0", "0", "0", "0", "0", "0"],
                         ["0", "0", "0", "0", "0", "0", "0", "0"],
                         ["0", "0", "0", "0", "0", "0", "0", "0"],
                         ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                         ["wr", "wk", "wb", "wki", "wq", "wb", "wk", "wr"]]

        # Holds labels for the pieces on the board.
        self.piecePos = [["0", "0", "0", "0", "0", "0", "0", "0"],
                         ["0", "0", "0", "0", "0", "0", "0", "0"],
                         ["0", "0", "0", "0", "0", "0", "0", "0"],
                         ["0", "0", "0", "0", "0", "0", "0", "0"],
                         ["0", "0", "0", "0", "0", "0", "0", "0"],
                         ["0", "0", "0", "0", "0", "0", "0", "0"],
                         ["0", "0", "0", "0", "0", "0", "0", "0"],
                         ["0", "0", "0", "0", "0", "0", "0", "0"]]

        # Holds pathfinding info. [Evaluated, cost from current, cost to end, total value]
        self.nodeArr = [[[0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize],
                        [0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize],
                        [0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize]],
                        [[0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize],
                        [0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize],
                        [0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize]],
                        [[0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize],
                        [0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize],
                        [0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize]],
                        [[0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize],
                        [0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize],
                        [0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize]],
                        [[0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize],
                        [0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize],
                        [0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize]],
                        [[0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize],
                        [0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize],
                        [0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize]],
                        [[0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize],
                        [0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize],
                        [0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize]],
                        [[0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize],
                        [0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize],
                        [0, 0, 0, sys.maxsize], [0, 0, 0, sys.maxsize]]]

        self.showBoard()

    def showBoard(self):
        # Initialize the board.
        self.setBoard()
        self.resize(self.boardSize + self.moveIndicator.width(), self.boardSize)

    def setBoard(self):
        self.tileSize = 75
        self.boardSize = self.tileSize * 8
        self.addBoardComponents(self.tileSet, self.tilePos)
        self.addBoardComponents(self.pieceSet, self.piecePos)

        # Set up the move indicator properties
        self.moveIndicator.setText("Turn: White")
        self.moveIndicator.setAlignment(Qt.AlignCenter)
        self.moveIndicator.resize(200, 25)
        self.moveIndicator.setFont(QFont('Arial', 16))
        self.moveIndicator.move(self.boardSize, self.boardSize / 2 - 50)

        # Set up remaining move indicator
        self.remainingMoveIndicator.setText("Remaining Moves:"
                                            "\nLeft Corp: " + str(self.playerTurnsRemaining[0]) +
                                            "\nCenter Corp: " + str(self.playerTurnsRemaining[1]) +
                                            "\nRight Corp: " + str(self.playerTurnsRemaining[2]))
        self.remainingMoveIndicator.setAlignment(Qt.AlignCenter)
        self.remainingMoveIndicator.resize(200, 100)
        self.remainingMoveIndicator.setFont(QFont('Arial', 16))
        self.remainingMoveIndicator.move(self.boardSize, self.boardSize / 2)

        # Set up the move indicator properties
        self.moveInfoIndicator.setText("")
        self.moveInfoIndicator.setAlignment(Qt.AlignCenter)
        self.moveInfoIndicator.resize(200, 50)
        self.moveInfoIndicator.setFont(QFont('Arial', 16))
        self.moveInfoIndicator.move(self.boardSize, self.boardSize / 2 + 125)

        # Set up remaining move indicator
        self.gameWinner.setAlignment(Qt.AlignCenter)
        self.gameWinner.resize(self.boardSize, self.boardSize)
        self.gameWinner.setFont(QFont('Arial', 36))
        self.gameWinner.setStyleSheet('font-weight: bold; color: red')
        dropShadow = QGraphicsDropShadowEffect()
        dropShadow.setColor(QColor(0, 0, 0))
        dropShadow.setXOffset(0)
        dropShadow.setYOffset(0)
        dropShadow.setBlurRadius(50)
        self.gameWinner.setGraphicsEffect(dropShadow)
        self.gameWinner.move(0, 0)
        self.gameWinner.hide()

        # Set up skip button
        self.skipButton.clicked.connect(self.switchTurn)
        self.skipButton.setFont(QFont('Arial', 16))
        self.skipButton.move(self.boardSize - ((self.skipButton.width() - self.moveIndicator.width()) / 2),
                             self.boardSize / 2 + 200)

    def addBoardComponents(self, sender, destination):
        # These are used as iterators to move through the arrays.
        xIter = 0
        yIter = 0

        # Iterate through all tiles in the tile set array and create images for them.
        # The images are stored in another array that can be manipulated.
        for row in sender:
            for tile in row:
                if not tile == "0":
                    # This assigns special properties to each piece type.
                    if tile == "wp" or tile == "bp":
                        if xIter <= 2:
                            label = piece.piece(tile[0], "pawn", 0, parent=self)
                        elif xIter == 3 or xIter == 4:
                            label = piece.piece(tile[0], "pawn", 1, parent=self)
                        elif xIter >= 5:
                            label = piece.piece(tile[0], "pawn", 2, parent=self)
                    elif tile == "wr" or tile == "br":
                        label = piece.piece(tile[0], "rook", 1, parent=self)
                    elif tile == "wk" or tile == "bk":
                        if xIter <= 2:
                            label = piece.piece(tile[0], "knight", 0, parent=self)
                        elif xIter >= 5:
                            label = piece.piece(tile[0], "knight", 2, parent=self)
                    elif tile == "wb" or tile == "bb":
                        if xIter <= 2:
                            label = piece.piece(tile[0], "bishop", 0, parent=self)
                        elif xIter >= 5:
                            label = piece.piece(tile[0], "bishop", 2, parent=self)
                    elif tile == "wq" or tile == "bq":
                        label = piece.piece(tile[0], "queen", 1, parent=self)
                    elif tile == "wki" or tile == "bki":
                        label = piece.piece(tile[0], "king", 1, parent=self)
                    else:
                        label = QLabel(self)
                    # Set the image based on the array element.
                    label.resize(75, 75)
                    pixmap = QPixmap('../img/' + tile)
                    label.setPixmap(pixmap)
                    label.setScaledContents(True)
                    label.move(xIter * self.tileSize, yIter * self.tileSize)

                    # Move the new label to the label array.
                    destination[yIter][xIter] = label

                xIter += 1
            xIter = 0
            yIter += 1

    def checkSwitchTurn(self, commander):
        # Remove the move authority from the current commander and check to see if all command authority is removed.
        self.playerTurnsRemaining[commander] = 0
        self.remainingMoveIndicator.setText("Remaining Moves:"
                                            "\nLeft Corp: " + str(self.playerTurnsRemaining[0]) +
                                            "\nCenter Corp: " + str(self.playerTurnsRemaining[1]) +
                                            "\nRight Corp: " + str(self.playerTurnsRemaining[2]))
        if self.playerTurnsRemaining[0] + self.playerTurnsRemaining[1] + self.playerTurnsRemaining[2] == 0 and \
                self.knightSpecialMovesRemaining == 0:
            self.switchTurn()

    def switchTurn(self):
        # Switch the turn to the other person and update the UI.
        self.knightSpecialMovesRemaining = 0
        self.playerTurnsRemaining = [0, 0, 0]
        if self.turn == 0:
            self.turn = 1
            self.moveIndicator.setText("Turn: Black")
            if not self.gameOver:
                self.checkBishopsRemaining("b")
        else:
            self.turn = 0
            self.moveIndicator.setText("Turn: White")
            if not self.gameOver:
                self.checkBishopsRemaining("w")
        self.remainingMoveIndicator.setText("Remaining Moves:"
                                            "\nLeft Corp: " + str(self.playerTurnsRemaining[0]) +
                                            "\nCenter Corp: " + str(self.playerTurnsRemaining[1]) +
                                            "\nRight Corp: " + str(self.playerTurnsRemaining[2]))

    def checkBishopsRemaining(self, color):
        self.playerTurnsRemaining[1] = 1
        xIter = 0
        yIter = 0
        for row in self.pieceSet:
            for tile in row:
                if self.pieceSet[yIter][xIter] == color + "b":
                    self.playerTurnsRemaining[self.piecePos[yIter][xIter].pieceCommander] = 1
                if self.pieceSet[yIter][xIter][1:] == "k":
                    self.piecePos[yIter][xIter].knightSpecial = False
                xIter += 1
            xIter = 0
            yIter += 1

    def movePiece(self, fromPos, toPos, commander, rules):
        if not fromPos == toPos:
            # Player is trying to move onto a piece
            if not self.piecePos[fromPos[1]][fromPos[0]].knightSpecial and not self.piecePos[toPos[1]][toPos[0]] == "0":
                # Try to capture a piece
                if not self.playerTurnsRemaining[commander] == 0 and \
                        not self.piecePos[fromPos[1]][fromPos[0]].pieceColor == \
                            self.piecePos[toPos[1]][toPos[0]].pieceColor:
                    if self.checkAttackRange(fromPos, toPos, rules):
                        if self.checkCapturePiece(toPos, rules):
                            if self.piecePos[fromPos[1]][fromPos[0]].pieceType == "knight":
                                self.setKnightSpecial(fromPos, False)
                            # Capture the piece.
                            self.capturePiece(toPos)
                            # Move the object through the array to match its movements on the gui.
                            self.moveOverGui(fromPos, toPos, commander)
                            print("Captured")
                            self.moveInfoIndicator.setText("Captured Piece")
                        else:
                            if self.piecePos[fromPos[1]][fromPos[0]].pieceType == "knight":
                                self.setKnightSpecial(fromPos, False)
                            # Snap the piece back to its start position when the person releases it.
                            self.piecePos[fromPos[1]][fromPos[0]].move(fromPos[0] * self.tileSize,
                                                                       fromPos[1] * self.tileSize)
                            # Set and check the moves remaining for the current player.
                            self.checkSwitchTurn(commander)
                            print("Failed To Capture")
                            self.moveInfoIndicator.setText("Capture Failed")
                    else:
                        # Snap the piece back to its start position when the person releases it.
                        self.piecePos[fromPos[1]][fromPos[0]].move(fromPos[0] * self.tileSize,
                                                                   fromPos[1] * self.tileSize)
                        print("Attack Out Of Range")
                        self.moveInfoIndicator.setText("Attack Out Of\nRange")
                # Else, the player is trying to give to a bishop
                elif commander == 1 and not self.piecePos[fromPos[1]][fromPos[0]].pieceType == "king" and \
                        self.piecePos[toPos[1]][toPos[0]].pieceType == "bishop":
                    self.givePieceToBishop(fromPos, toPos)
                    print("Give To Bishop")
                    self.moveInfoIndicator.setText("Piece Given To\nBishop")
                else:
                    # Snap the piece back to its start position when the person releases it.
                    self.piecePos[fromPos[1]][fromPos[0]].move(fromPos[0] * self.tileSize, fromPos[1] * self.tileSize)
                    print("No In-Fighting")
                    if not self.piecePos[fromPos[1]][fromPos[0]].pieceColor == \
                            self.piecePos[toPos[1]][toPos[0]].pieceColor:
                        self.moveInfoIndicator.setText("No Command Point\nFor This Piece")
                    else:
                        self.moveInfoIndicator.setText("Invalid Move")
            # Else, the player is trying to move to an empty space.
            elif not self.piecePos[fromPos[1]][fromPos[0]].knightSpecial and \
                    not self.playerTurnsRemaining[commander] == 0 and self.checkValidMove(fromPos, toPos, rules):
                if self.piecePos[fromPos[1]][fromPos[0]].pieceType == "knight":
                    self.setKnightSpecial(fromPos, True)
                # Move the object through the array to match its movements on the gui.
                self.moveOverGui(fromPos, toPos, commander)
                print("Moved To Empty")
                self.moveInfoIndicator.setText("")
            # Knight is performing a special attack.
            elif self.piecePos[fromPos[1]][fromPos[0]].pieceType == "knight" and \
                    self.piecePos[fromPos[1]][fromPos[0]].knightSpecial and \
                    not self.piecePos[toPos[1]][toPos[0]] == "0":
                # Try to capture a piece
                if not self.piecePos[fromPos[1]][fromPos[0]].pieceColor == self.piecePos[toPos[1]][toPos[0]].pieceColor:
                    if self.checkAttackRange(fromPos, toPos, rules):
                        if self.checkCapturePieceSpecial(toPos, rules):
                            if self.piecePos[fromPos[1]][fromPos[0]].pieceType == "knight":
                                self.setKnightSpecial(fromPos, False)
                            # Capture the piece.
                            self.capturePiece(toPos)
                            # Move the object through the array to match its movements on the gui.
                            self.moveOverGui(fromPos, toPos, commander)
                            print("Captured")
                            self.moveInfoIndicator.setText("Captured Piece")
                        else:
                            if self.piecePos[fromPos[1]][fromPos[0]].pieceType == "knight":
                                self.setKnightSpecial(fromPos, False)
                            # Snap the piece back to its start position when the person releases it.
                            self.piecePos[fromPos[1]][fromPos[0]].move(fromPos[0] * self.tileSize,
                                                                       fromPos[1] * self.tileSize)
                            # Set and check the moves remaining for the current player.
                            self.checkSwitchTurn(commander)
                            print("Failed To Capture")
                            self.moveInfoIndicator.setText("Capture Failed")
                    else:
                        # Snap the piece back to its start position when the person releases it.
                        self.piecePos[fromPos[1]][fromPos[0]].move(fromPos[0] * self.tileSize,
                                                                   fromPos[1] * self.tileSize)
                        print("Attack Out Of Range")
                        self.moveInfoIndicator.setText("Attack Out Of\nRange")
                # Else, the player is trying to give to a bishop
                elif commander == 1 and not self.piecePos[fromPos[1]][fromPos[0]].pieceType == "king" and \
                        self.piecePos[toPos[1]][toPos[0]].pieceType == "bishop":
                    self.givePieceToBishop(fromPos, toPos)
                    print("Give To Bishop")
                    self.moveInfoIndicator.setText("Piece Given To\nBishop")
                else:
                    # Snap the piece back to its start position when the person releases it.
                    self.piecePos[fromPos[1]][fromPos[0]].move(fromPos[0] * self.tileSize, fromPos[1] * self.tileSize)
                    print("No In-Fighting")
                    if not self.piecePos[fromPos[1]][fromPos[0]].pieceColor == \
                           self.piecePos[toPos[1]][toPos[0]].pieceColor:
                        self.moveInfoIndicator.setText("No Command Point\nFor This Piece")
                    else:
                        self.moveInfoIndicator.setText("Invalid Move")
            # No command point for this piece
            elif not self.piecePos[fromPos[1]][fromPos[0]].knightSpecial and \
                    self.playerTurnsRemaining[commander] == 0 and self.checkValidMove(fromPos, toPos, rules):
                # Snap the piece back to its start position when the person releases it.
                self.piecePos[fromPos[1]][fromPos[0]].move(fromPos[0] * self.tileSize, fromPos[1] * self.tileSize)
                print("No Command Point")
                self.moveInfoIndicator.setText("No Command Point\nFor This Piece")
            else:
                # Snap the piece back to its start position when the person releases it.
                self.piecePos[fromPos[1]][fromPos[0]].move(fromPos[0] * self.tileSize, fromPos[1] * self.tileSize)
                print("No Valid Movement")
                self.moveInfoIndicator.setText("Invalid Move")
        else:
            # Snap the piece back to its start position when the person releases it.
            self.piecePos[fromPos[1]][fromPos[0]].move(fromPos[0] * self.tileSize, fromPos[1] * self.tileSize)
            print("Same Square")

    def setKnightSpecial(self, target, setTo):
        if self.piecePos[target[1]][target[0]].pieceType == "knight" and setTo:
            self.piecePos[target[1]][target[0]].knightSpecial = True
            self.knightSpecialMovesRemaining += 1
        elif self.piecePos[target[1]][target[0]].pieceType == "knight" and not setTo:
            self.piecePos[target[1]][target[0]].knightSpecial = False
            self.knightSpecialMovesRemaining -= 1

    def givePieceToBishop(self, fromPos, toPos):
        # Give the piece command to the Bishop.
        self.piecePos[fromPos[1]][fromPos[0]].pieceCommander = self.piecePos[toPos[1]][toPos[0]].pieceCommander
        # Snap the piece back to its start position when the person releases it.
        self.piecePos[fromPos[1]][fromPos[0]].move(fromPos[0] * self.tileSize, fromPos[1] * self.tileSize)

    def moveOverGui(self, fromPos, toPos, commander):
        # Snap the piece to the nearest grid point when the person releases it.
        self.piecePos[fromPos[1]][fromPos[0]].move(toPos[0] * self.tileSize, toPos[1] * self.tileSize)

        self.moveThroughArray(fromPos, toPos, self.pieceSet)
        self.moveThroughArray(fromPos, toPos, self.piecePos)

        # Set and check the moves remaining for the current player.
        self.checkSwitchTurn(commander)

    def moveThroughArray(self, fromPos, toPos, pieceList):
        # Copy this piece to destination.
        pieceList[toPos[1]][toPos[0]] = pieceList[fromPos[1]][fromPos[0]]

        # Remove it from the previous position.
        pieceList[fromPos[1]][fromPos[0]] = "0"

    def checkValidMove(self, fromPos, toPos, rules):
        # Use the appropriate rule from the rules classes to check the movement of the piece.
        return rules.isPathFree(self, fromPos, toPos, self.piecePos[fromPos[1]][fromPos[0]].pieceColor,
                                self.piecePos, self.nodeArr)

    def checkAttackRange(self, fromPos, toPos, rules):
        # Use the appropriate rule from the rules classes to check the attack range of the piece.
        return rules.checkAttackInRange(self, fromPos, toPos, self.piecePos[fromPos[1]][fromPos[0]].pieceColor)

    def checkCapturePiece(self, toPos, rules):
        # Use the appropriate rule from the rules classes to check the capture roll of the piece.
        return rules.rollCapture(self, toPos, self.piecePos)

    def checkCapturePieceSpecial(self, toPos, rules):
        # Use the appropriate rule from the rules classes to check the special capture roll of the piece.
        return rules.rollCaptureSpecial(self, toPos, self.piecePos)

    def capturePiece(self, target):
        # If the target is a bishop, hand its pieces to the king.
        if self.pieceSet[target[1]][target[0]][1:] == "b":
            xIter = 0
            yIter = 0
            for row in self.pieceSet:
                for tile in row:
                    if not self.pieceSet[yIter][xIter] == "0" and not self.pieceSet[yIter][xIter][1:] == "b" and \
                            self.piecePos[yIter][xIter].pieceColor == self.piecePos[target[1]][target[0]].pieceColor \
                            and self.piecePos[yIter][xIter].pieceCommander == \
                            self.piecePos[target[1]][target[0]].pieceCommander:
                        self.piecePos[yIter][xIter].pieceCommander = 1
                    xIter += 1
                xIter = 0
                yIter += 1
        # If the target is a king, the capturing player wins.
        if self.pieceSet[target[1]][target[0]][1:] == "ki":
            self.gameOver = True
            if self.pieceSet[target[1]][target[0]][0] == "b":
                self.winner = "White"
            else:
                self.winner = "Black"
            self.skipButton.clicked.disconnect(self.switchTurn)
            self.playerTurnsRemaining = [0, 0, 0]
            self.gameWinner.setText("Game Over!\n"
                                    "The Winner Is " + self.winner)
            self.gameWinner.show()
            self.gameWinner.raise_()

        # This deletes a piece from the board.
        self.piecePos[target[1]][target[0]].deleteLater()
        self.piecePos[target[1]][target[0]] = "0"


def chessBoard():
    app = QApplication(sys.argv)
    window = chessBoardWindow()

    window.show()
    sys.exit(app.exec_())


def main():
    chessBoard()


if __name__ == '__main__':
    main()
