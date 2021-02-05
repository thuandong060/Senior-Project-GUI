import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QFont
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

        # Button so you can skip your turn.
        self.skipButton = QPushButton("End Turn", self)

        # The basic unit of measurement for the board.
        self.tileSize = 0
        self.boardSize = 0

        self.playerTurnsRemaining = [1, 1, 1]

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
        self.setFont(QFont('Arial', 16))
        self.moveIndicator.move(self.boardSize, self.boardSize / 2 - 50)

        # Set up remaining move indicator
        self.remainingMoveIndicator.setText("Remaining Moves:"
                                            "\nLeft Corp: " + str(self.playerTurnsRemaining[0]) +
                                            "\nCenter Corp: " + str(self.playerTurnsRemaining[1]) +
                                            "\nRight Corp: " + str(self.playerTurnsRemaining[2]))
        self.remainingMoveIndicator.setAlignment(Qt.AlignCenter)
        self.remainingMoveIndicator.resize(200, 100)
        self.setFont(QFont('Arial', 16))
        self.remainingMoveIndicator.move(self.boardSize, self.boardSize / 2)

        # Set up skip button
        self.skipButton.clicked.connect(self.switchTurn)
        self.skipButton.move(self.boardSize - ((self.skipButton.width() - self.moveIndicator.width()) / 2),
                             self.boardSize / 2 + 130)

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
        if self.playerTurnsRemaining[0] + self.playerTurnsRemaining[1] + self.playerTurnsRemaining[2] == 0:
            self.switchTurn()

    def switchTurn(self):
        # Switch the turn to the other person and update the UI.
        if self.turn == 0:
            self.turn = 1
            self.moveIndicator.setText("Turn: Black")
            # Remove this later
            self.playerTurnsRemaining = [1, 1, 1]
        else:
            self.turn = 0
            self.moveIndicator.setText("Turn: White")
            self.playerTurnsRemaining = [1, 1, 1]
        self.remainingMoveIndicator.setText("Remaining Moves:"
                                            "\nLeft Corp: " + str(self.playerTurnsRemaining[0]) +
                                            "\nCenter Corp: " + str(self.playerTurnsRemaining[1]) +
                                            "\nRight Corp: " + str(self.playerTurnsRemaining[2]))

    def movePiece(self, fromPos, toPos, commander, rules):
        if not fromPos == toPos:
            # Player is trying to move onto a piece
            if not self.piecePos[toPos[1]][toPos[0]] == "0":
                # Try to capture a piece
                if not self.piecePos[fromPos[1]][fromPos[0]].pieceColor == self.piecePos[toPos[1]][toPos[0]].pieceColor:
                    if self.checkAttackRange(fromPos, toPos, rules):
                        if self.checkCapturePiece(toPos, rules):
                            # Capture the piece.
                            self.capturePiece(toPos)
                            # Move the object through the array to match its movements on the gui.
                            self.moveOverGui(fromPos, toPos, commander)
                            print("Captured")
                        else:
                            # Snap the piece back to its start position when the person releases it.
                            self.piecePos[fromPos[1]][fromPos[0]].move(fromPos[0] * self.tileSize,
                                                                       fromPos[1] * self.tileSize)
                            # Set and check the moves remaining for the current player.
                            self.checkSwitchTurn(commander)
                            print("Failed To Capture")
                    else:
                        # Snap the piece back to its start position when the person releases it.
                        self.piecePos[fromPos[1]][fromPos[0]].move(fromPos[0] * self.tileSize,
                                                                   fromPos[1] * self.tileSize)
                        print("Attack Out Of Range")
                # Else, the player is trying to give to a bishop
                elif commander == 1 and not self.piecePos[fromPos[1]][fromPos[0]].pieceType == "king" and \
                        self.piecePos[toPos[1]][toPos[0]].pieceType == "bishop":
                    # Snap the piece back to its start position when the person releases it.
                    self.piecePos[fromPos[1]][fromPos[0]].move(fromPos[0] * self.tileSize, fromPos[1] * self.tileSize)
                    print("Give To Bishop")
                else:
                    # Snap the piece back to its start position when the person releases it.
                    self.piecePos[fromPos[1]][fromPos[0]].move(fromPos[0] * self.tileSize, fromPos[1] * self.tileSize)
                    print("No In-Fighting")
            # Else, the player is trying to move to an empty space.
            elif self.checkValidMove(fromPos, toPos, rules):
                # Move the object through the array to match its movements on the gui.
                self.moveOverGui(fromPos, toPos, commander)
                print("Moved To Empty")
            else:
                # Snap the piece back to its start position when the person releases it.
                self.piecePos[fromPos[1]][fromPos[0]].move(fromPos[0] * self.tileSize, fromPos[1] * self.tileSize)
                print("No Valid Movement")
        else:
            # Snap the piece back to its start position when the person releases it.
            self.piecePos[fromPos[1]][fromPos[0]].move(fromPos[0] * self.tileSize, fromPos[1] * self.tileSize)
            print("Same Square")

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
        # Use the appropriate rule from the rules classes to chek the capture roll of the piece.
        return rules.rollCapture(self, toPos, self.piecePos)

    def capturePiece(self, target):
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
