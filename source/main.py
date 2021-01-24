import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from source import piece
import random


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
        xiter = 0
        yiter = 0

        # Iterate through all tiles in the tile set array and create images for them.
        # The images are stored in another array that can be manipulated.
        for row in sender:
            for tile in row:
                if not tile == "0":
                    # This assigns special properties to each piece type.
                    if tile == "wp" or tile == "bp":
                        if xiter <= 2:
                            label = piece.piece(tile[0], "pawn", 0, parent=self)
                        elif xiter == 3 or xiter == 4:
                            label = piece.piece(tile[0], "pawn", 1, parent=self)
                        elif xiter >= 5:
                            label = piece.piece(tile[0], "pawn", 2, parent=self)
                    elif tile == "wr" or tile == "br":
                        label = piece.piece(tile[0], "rook", 1, parent=self)
                    elif tile == "wk" or tile == "bk":
                        if xiter <= 2:
                            label = piece.piece(tile[0], "knight", 0, parent=self)
                        elif xiter >= 5:
                            label = piece.piece(tile[0], "knight", 2, parent=self)
                    elif tile == "wb" or tile == "bb":
                        if xiter <= 2:
                            label = piece.piece(tile[0], "bishop", 0, parent=self)
                        elif xiter >= 5:
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
                    label.move(xiter * self.tileSize, yiter * self.tileSize)

                    # Move the new label to the label array.
                    destination[yiter][xiter] = label

                xiter += 1
            xiter = 0
            yiter += 1

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

    def movePiece(self, fromPos, toPos, commander):
        if not fromPos == toPos:
            if self.checkValidMove(fromPos, toPos):
                # Move the object through the array to match its movements on the gui.
                if not self.piecePos[toPos[1]][toPos[0]] == "0":
                    if self.rollCapturePiece(toPos):
                        self.capturePiece(toPos)

                        self.moveOverGui(fromPos, toPos, commander)
                    else:
                        # Snap the piece back to its start position when the person releases it.
                        self.piecePos[fromPos[1]][fromPos[0]].move(fromPos[0] * self.tileSize,
                                                                   fromPos[1] * self.tileSize)

                        # Set and check the moves remaining for the current player.
                        self.checkSwitchTurn(commander)
                else:
                    self.moveOverGui(fromPos, toPos, commander)
            else:
                # Snap the piece back to its start position when the person releases it.
                self.piecePos[fromPos[1]][fromPos[0]].move(fromPos[0] * self.tileSize, fromPos[1] * self.tileSize)
        else:
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
        print(pieceList)

    def checkValidMove(self, fromPos, toPos):
        # This needs to be updated with the actual rules!!!!
        moveIsValid = True
        if self.pieceSet[fromPos[1]][fromPos[0]][0] == self.pieceSet[toPos[1]][toPos[0]][0]:
            moveIsValid = False
        # do stuff to check and see if the move is valid
        return moveIsValid

    def rollCapturePiece(self, target):
        # This needs to be updated with the actual capture weights!!!!
        isCaptureSuccessful = False
        if random.randint(0, 1) == 1:
            isCaptureSuccessful = True
        return isCaptureSuccessful

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
