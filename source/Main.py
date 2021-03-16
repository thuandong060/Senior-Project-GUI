import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from ChessRule import Piece
from source import BoardInterface
from time import sleep
from source import AiMove
from source import PieceMoveInfo
import random


class chessBoardWindow(QMainWindow):
    def __init__(self):
        super(chessBoardWindow, self).__init__()



        # Thread storage.
        self.animThread = 0
        self.aiThread = 0

        # AI interface
        self.boardInterface = BoardInterface.BoardInterface(self)

        # Move list
        self.moveHistory = []

        # Used when the game needs to be paused.
        self.pauseGame = False

        # Pause background
        self.pauseBackground = QLabel(self)

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

        # Button so you can reset the game.
        self.resetButton = QPushButton("Reset Board", self)

        # Die roll components
        self.rolledDie = QLabel(self)
        self.neededDie = QLabel(self)
        self.specialDie = QLabel(self)
        self.rolledDieText = QLabel(self)
        self.neededDieText = QLabel(self)
        self.specialDieText = QLabel(self)
        self.captureRollText = QLabel(self)
        self.previousRoll = 0

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
        self.pieceSet = [["br", "bk", "bb", "bq", "bki", "bb", "bk", "br"],
                         ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                         ["0", "0", "0", "0", "0", "0", "0", "0"],
                         ["0", "0", "0", "0", "0", "0", "0", "0"],
                         ["0", "0", "0", "0", "0", "0", "0", "0"],
                         ["0", "0", "0", "0", "0", "0", "0", "0"],
                         ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                         ["wr", "wk", "wb", "wq", "wki", "wb", "wk", "wr"]]

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

    # Getters
    def getTurn(self):
        return self.turn

    def getPlayerTurnsRemaining(self):
        return self.playerTurnsRemaining

    def getPiecePos(self):
        return self.piecePos

    def getMoveHistory(self):
        return self.moveHistory

    # Normal Functions
    def resetBoard(self):
        # Reset the game
        self.pauseGame = False

        self.gameMoveList = []
        self.turn = 0
        self.playerTurnsRemaining = [1, 1, 1]
        self.knightSpecialMovesRemaining = 0
        self.gameOver = False
        self.winner = 0

        # Delete existing pieces
        xIter = 0
        yIter = 0
        for row in self.piecePos:
            for tile in row:
                if not self.piecePos[yIter][xIter] == "0":
                    self.piecePos[yIter][xIter].deleteLater()
                    self.piecePos[yIter][xIter] = "0"
                xIter += 1
            xIter = 0
            yIter += 1

        self.pauseBackground.hide()
        self.gameWinner.hide()
        self.resetButton.hide()

        self.addBoardComponents(self.pieceSet, self.piecePos)

        self.skipButton.clicked.connect(self.skipButtonClicked)
        self.moveIndicator.setText("Turn: White")
        self.remainingMoveIndicator.setText("Remaining Moves:"
                                            "\nLeft Corp: " + str(self.playerTurnsRemaining[0]) +
                                            "\nCenter Corp: " + str(self.playerTurnsRemaining[1]) +
                                            "\nRight Corp: " + str(self.playerTurnsRemaining[2]))
        self.boardInterface.updatePiecePosCopy(self.getPiecePos())

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
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.moveIndicator.height() * 0.8)
        self.moveIndicator.setFont(font)
        self.moveIndicator.move(int(self.boardSize), int(self.boardSize / 2 - 50))

        # Set up remaining move indicator
        self.remainingMoveIndicator.setText("Remaining Moves:"
                                            "\nLeft Corp: " + str(self.playerTurnsRemaining[0]) +
                                            "\nCenter Corp: " + str(self.playerTurnsRemaining[1]) +
                                            "\nRight Corp: " + str(self.playerTurnsRemaining[2]))
        self.remainingMoveIndicator.setAlignment(Qt.AlignCenter)
        self.remainingMoveIndicator.resize(200, 100)
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.remainingMoveIndicator.height() * 0.2)
        self.remainingMoveIndicator.setFont(font)
        self.remainingMoveIndicator.move(int(self.boardSize), int(self.boardSize / 2))

        # Set up the move indicator properties
        self.moveInfoIndicator.setText("")
        self.moveInfoIndicator.setAlignment(Qt.AlignCenter)
        self.moveInfoIndicator.resize(200, 50)
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.moveInfoIndicator.height() * 0.4)
        self.moveInfoIndicator.setFont(font)
        self.moveInfoIndicator.move(int(self.boardSize), int(self.boardSize / 2 + 125))

        # Set up win indicator
        self.pauseBackground.setAlignment(Qt.AlignCenter)
        self.pauseBackground.resize(self.boardSize, self.boardSize)
        self.pauseBackground.setStyleSheet('background-color: rgba(0, 0, 0, 150)')
        self.pauseBackground.move(0, 0)
        self.pauseBackground.hide()

        # Set up win indicator
        self.gameWinner.setAlignment(Qt.AlignCenter)
        self.gameWinner.resize(self.boardSize, self.boardSize)
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.gameWinner.height() * 0.1)
        self.gameWinner.setFont(font)
        self.gameWinner.setStyleSheet('font-weight: bold; color: rgba(0, 255, 255, 255)')
        self.gameWinner.move(0, 0)
        self.gameWinner.hide()

        # Set up skip button
        self.skipButton.clicked.connect(self.skipButtonClicked)
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.skipButton.height() * 0.6)
        self.skipButton.setFont(font)
        self.skipButton.move(int(self.boardSize - ((self.skipButton.width() - self.moveIndicator.width()) / 2)),
                             int(self.boardSize / 2 + 200))

        # Set up reset button
        self.resetButton.clicked.connect(self.resetBoard)
        self.resetButton.resize(150, self.resetButton.height())
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.resetButton.height() * 0.6)
        self.resetButton.setFont(font)
        self.resetButton.move(int((self.boardSize / 2) - (self.resetButton.width() / 2)), int(self.boardSize / 2 + 100))
        self.resetButton.hide()

        # Set up Rolled Die components
        self.rolledDie.resize(75, 75)
        self.rolledDie.setScaledContents(True)
        self.rolledDie.move(int((self.boardSize / 2) - (self.rolledDie.width() / 2)), int((self.boardSize / 2) + 50))
        self.rolledDie.hide()

        # Set up Needed Die components
        self.neededDie.resize(75, 75)
        self.neededDie.setScaledContents(True)
        self.neededDie.move(int((self.boardSize / 2) - (self.neededDie.width() / 2)), int((self.boardSize / 2) - 150))
        self.neededDie.hide()

        # Set up Special Die
        self.specialDie.resize(75, 75)
        self.specialDie.setScaledContents(True)
        self.specialDie.move(int((self.boardSize / 2) - (self.specialDie.width() / 2) + 150),
                             int((self.boardSize / 2) + 50))
        pixmap = QPixmap('../img/die1')
        self.specialDie.setPixmap(pixmap)
        self.specialDie.hide()

        # Set up Rolled Die Text
        self.rolledDieText.setAlignment(Qt.AlignCenter)
        self.rolledDieText.setText("Your Roll:")
        self.rolledDieText.resize(300, 50)
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.rolledDieText.height() * 0.8)
        self.rolledDieText.setFont(font)
        self.rolledDieText.setStyleSheet('font-weight: bold; color: rgba(0, 255, 255, 255)')
        self.rolledDieText.move(int((self.boardSize / 2) - (self.rolledDieText.width() / 2)), int((self.boardSize / 2)))
        self.rolledDieText.hide()

        # Set up Needed Die Text
        self.neededDieText.setAlignment(Qt.AlignCenter)
        self.neededDieText.setText("Roll Needed To\nCapture Piece:")
        self.neededDieText.resize(400, 100)
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.neededDieText.height() * 0.4)
        self.neededDieText.setFont(font)
        self.neededDieText.setStyleSheet('font-weight: bold; color: rgba(0, 255, 255, 255)')
        self.neededDieText.move(int((self.boardSize / 2) - (self.neededDieText.width() / 2)),
                                int((self.boardSize / 2) - 250))
        self.neededDieText.hide()

        # Set up Special Die Text
        self.specialDieText.setAlignment(Qt.AlignCenter)
        self.specialDieText.setText("-")
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.specialDieText.height() * 3)
        self.specialDieText.setFont(font)
        self.specialDieText.setStyleSheet('font-weight: bold; color: rgba(0, 255, 255, 255)')
        self.specialDieText.move(int((self.boardSize / 2) - (self.specialDieText.width() / 2) + 75),
                                 int((self.boardSize / 2) + 65))
        self.specialDieText.hide()

        # Set up Capture Roll Text
        self.captureRollText.setAlignment(Qt.AlignCenter)
        self.captureRollText.setText("")
        self.captureRollText.resize(500, 50)
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.captureRollText.height() * 0.8)
        self.captureRollText.setFont(font)
        self.captureRollText.setStyleSheet('font-weight: bold; color: rgba(0, 255, 255, 255)')
        self.captureRollText.move(int((self.boardSize / 2) - (self.captureRollText.width() / 2)),
                                  int((self.boardSize / 2) + 150))
        self.captureRollText.hide()

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
                            if tile[0] == "w":
                                label = Piece.Piece(tile[0], "pawn", 0, parent=self)
                            else:
                                label = Piece.Piece(tile[0], "pawn", 2, parent=self)
                        elif xIter == 3 or xIter == 4:
                            label = Piece.Piece(tile[0], "pawn", 1, parent=self)
                        elif xIter >= 5:
                            if tile[0] == "w":
                                label = Piece.Piece(tile[0], "pawn", 2, parent=self)
                            else:
                                label = Piece.Piece(tile[0], "pawn", 0, parent=self)
                    elif tile == "wr" or tile == "br":
                        label = Piece.Piece(tile[0], "rook", 1, parent=self)
                    elif tile == "wk" or tile == "bk":
                        if xIter <= 2:
                            if tile[0] == "w":
                                label = Piece.Piece(tile[0], "knight", 0, parent=self)
                            else:
                                label = Piece.Piece(tile[0], "knight", 2, parent=self)
                        elif xIter >= 5:
                            if tile[0] == "w":
                                label = Piece.Piece(tile[0], "knight", 2, parent=self)
                            else:
                                label = Piece.Piece(tile[0], "knight", 0, parent=self)
                    elif tile == "wb" or tile == "bb":
                        if xIter <= 2:
                            if tile[0] == "w":
                                label = Piece.Piece(tile[0], "bishop", 0, parent=self)
                            else:
                                label = Piece.Piece(tile[0], "bishop", 2, parent=self)
                        elif xIter >= 5:
                            if tile[0] == "w":
                                label = Piece.Piece(tile[0], "bishop", 2, parent=self)
                            else:
                                label = Piece.Piece(tile[0], "bishop", 0, parent=self)
                    elif tile == "wq" or tile == "bq":
                        label = Piece.Piece(tile[0], "queen", 1, parent=self)
                    elif tile == "wki" or tile == "bki":
                        label = Piece.Piece(tile[0], "king", 1, parent=self)
                    else:
                        label = QLabel(self)
                    # Set the image based on the array element.
                    label.resize(75, 75)
                    pixmap = QPixmap('../img/' + tile)
                    label.setPixmap(pixmap)
                    label.setScaledContents(True)
                    label.move(int(xIter * self.tileSize), int(yIter * self.tileSize))
                    label.show()

                    # Move the new label to the label array.
                    destination[yIter][xIter] = label

                xIter += 1
            xIter = 0
            yIter += 1

        self.boardInterface.updatePiecePosCopy(self.getPiecePos())

    def skipButtonClicked(self):
        if self.turn == 0:
            self.switchTurn()

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
        elif not self.gameOver and self.turn == 1:
            self.aiMoveThread()

    def switchTurn(self):
        # Switch the turn to the other person and update the UI.
        if not self.pauseGame:
            self.knightSpecialMovesRemaining = 0
            self.playerTurnsRemaining = [0, 0, 0]
            if self.turn == 0:
                self.turn = 1
                self.moveIndicator.setText("Turn: Black")
                if not self.gameOver:
                    self.checkBishopsRemaining(1)
            else:
                self.turn = 0
                self.moveIndicator.setText("Turn: White")
                if not self.gameOver:
                    self.checkBishopsRemaining(0)
            self.remainingMoveIndicator.setText("Remaining Moves:"
                                                "\nLeft Corp: " + str(self.playerTurnsRemaining[0]) +
                                                "\nCenter Corp: " + str(self.playerTurnsRemaining[1]) +
                                                "\nRight Corp: " + str(self.playerTurnsRemaining[2]))
            if not self.gameOver and self.turn == 1:
                self.aiMoveThread()

    def aiMoveThread(self):
        self.aiThread = AiMove.AiMove(self.boardInterface)
        self.aiThread.moveDetermined.connect(self.aiMoveThreadFinish)
        self.aiThread.aiSkipDetermined.connect(self.aiMoveThreadSkip)
        self.aiThread.start()

    def aiMoveThreadFinish(self, move):
        self.movePiece(move.getFromPos(), move.getToPos())

    def aiMoveThreadSkip(self):
        self.switchTurn()

    def checkBishopsRemaining(self, color):
        # Set the command points based on how many bishops the players have left.
        self.playerTurnsRemaining[1] = 1
        xIter = 0
        yIter = 0
        for row in self.piecePos:
            for tile in row:
                if not self.piecePos[yIter][xIter] == "0" and self.piecePos[yIter][xIter].pieceColor == color and \
                        self.piecePos[yIter][xIter].pieceType == "bishop":
                    self.playerTurnsRemaining[self.piecePos[yIter][xIter].pieceCommander] = 1
                if not self.piecePos[yIter][xIter] == "0" and self.piecePos[yIter][xIter].pieceType == "knight":
                    self.piecePos[yIter][xIter].knightSpecial = False
                xIter += 1
            xIter = 0
            yIter += 1

    def movePiece(self, fromPos, toPos):
        if not fromPos == toPos and not self.piecePos[fromPos[1]][fromPos[0]] == "0":
            # Player is trying to move onto a piece
            if not self.piecePos[toPos[1]][toPos[0]] == "0" and not self.piecePos[fromPos[1]][fromPos[0]].knightSpecial:
                # Try to capture a piece
                if not self.playerTurnsRemaining[self.piecePos[fromPos[1]][fromPos[0]].pieceCommander] == 0 and \
                        not self.piecePos[fromPos[1]][fromPos[0]].pieceColor == \
                            self.piecePos[toPos[1]][toPos[0]].pieceColor:
                    if self.checkAttackRange(fromPos, toPos, self.piecePos[fromPos[1]][fromPos[0]].rules):
                        # Run code to do roll for a capture.
                        self.doCaptureAnim(fromPos, toPos, self.piecePos[fromPos[1]][fromPos[0]].pieceCommander,
                                           self.piecePos[fromPos[1]][fromPos[0]].rules)
                    else:
                        # Snap the piece back to its start position when the person releases it.
                        self.piecePos[fromPos[1]][fromPos[0]].move(int(fromPos[0] * self.tileSize),
                                                                   int(fromPos[1] * self.tileSize))
                        self.moveInfoIndicator.setText("Attack Out Of\nRange")
                # Else, the player is trying to give to a bishop
                elif self.piecePos[fromPos[1]][fromPos[0]].pieceCommander == 1 and not \
                        self.piecePos[fromPos[1]][fromPos[0]].pieceType == "king" and \
                        self.piecePos[toPos[1]][toPos[0]].pieceType == "bishop":
                    self.givePieceToBishop(fromPos, toPos)
                    self.moveInfoIndicator.setText("Piece Given To\nBishop")
                else:
                    # Snap the piece back to its start position when the person releases it.
                    self.piecePos[fromPos[1]][fromPos[0]].move(int(fromPos[0] * self.tileSize),
                                                               int(fromPos[1] * self.tileSize))
                    if not self.piecePos[fromPos[1]][fromPos[0]].pieceColor == \
                            self.piecePos[toPos[1]][toPos[0]].pieceColor:
                        self.moveInfoIndicator.setText("No Command Point\nFor This Piece")
                    else:
                        self.moveInfoIndicator.setText("Invalid Move")
            # Else, the player is trying to move to an empty space.
            elif not self.piecePos[fromPos[1]][fromPos[0]].knightSpecial and \
                    not self.playerTurnsRemaining[self.piecePos[fromPos[1]][fromPos[0]].pieceCommander] == 0 and \
                    self.checkValidMove(fromPos, toPos, self.piecePos[fromPos[1]][fromPos[0]].rules):
                if self.piecePos[fromPos[1]][fromPos[0]].pieceType == "knight":
                    if self.checkKnightSpecial(fromPos, toPos, self.piecePos[fromPos[1]][fromPos[0]].rules):
                        self.setKnightSpecial(fromPos, True)
                    else:
                        self.setKnightSpecial(fromPos, False)
                # Move the object through the array to match its movements on the gui.
                self.moveOverGui(fromPos, toPos, self.piecePos[fromPos[1]][fromPos[0]].pieceCommander)
                self.moveInfoIndicator.setText("")
            # Knight is performing a special attack.
            elif not self.piecePos[toPos[1]][toPos[0]] == "0" and \
                    self.piecePos[fromPos[1]][fromPos[0]].pieceType == "knight" and \
                    self.piecePos[fromPos[1]][fromPos[0]].knightSpecial:
                # Try to capture a piece
                if not self.piecePos[fromPos[1]][fromPos[0]].pieceColor == self.piecePos[toPos[1]][toPos[0]].pieceColor:
                    if self.checkAttackRange(fromPos, toPos, self.piecePos[fromPos[1]][fromPos[0]].rules):
                        # Run code to do roll for a knight special capture.
                        self.doSpecialCaptureAnim(fromPos, toPos, self.piecePos[fromPos[1]][fromPos[0]].pieceCommander,
                                                  self.piecePos[fromPos[1]][fromPos[0]].rules)
                    else:
                        # Snap the piece back to its start position when the person releases it.
                        self.piecePos[fromPos[1]][fromPos[0]].move(int(fromPos[0] * self.tileSize),
                                                                   int(fromPos[1] * self.tileSize))
                        self.moveInfoIndicator.setText("Attack Out Of\nRange")
                # Else, the player is trying to give to a bishop
                elif self.piecePos[fromPos[1]][fromPos[0]].pieceCommander == 1 and not \
                        self.piecePos[fromPos[1]][fromPos[0]].pieceType == "king" and \
                        self.piecePos[toPos[1]][toPos[0]].pieceType == "bishop":
                    self.givePieceToBishop(fromPos, toPos)
                    self.moveInfoIndicator.setText("Piece Given To\nBishop")
                else:
                    # Snap the piece back to its start position when the person releases it.
                    self.piecePos[fromPos[1]][fromPos[0]].move(int(fromPos[0] * self.tileSize),
                                                               int(fromPos[1] * self.tileSize))
                    if not self.piecePos[fromPos[1]][fromPos[0]].pieceColor == \
                           self.piecePos[toPos[1]][toPos[0]].pieceColor:
                        self.moveInfoIndicator.setText("No Command Point\nFor This Piece")
                    else:
                        self.moveInfoIndicator.setText("Invalid Move")
            # No command point for this piece
            elif not self.piecePos[fromPos[1]][fromPos[0]].knightSpecial and \
                    self.playerTurnsRemaining[self.piecePos[fromPos[1]][fromPos[0]].pieceCommander] == 0 and \
                    self.checkValidMove(fromPos, toPos, self.piecePos[fromPos[1]][fromPos[0]].rules):
                # Snap the piece back to its start position when the person releases it.
                self.piecePos[fromPos[1]][fromPos[0]].move(int(fromPos[0] * self.tileSize),
                                                           int(fromPos[1] * self.tileSize))
                self.moveInfoIndicator.setText("No Command Point\nFor This Piece")
            else:
                # Snap the piece back to its start position when the person releases it.
                self.piecePos[fromPos[1]][fromPos[0]].move(int(fromPos[0] * self.tileSize),
                                                           int(fromPos[1] * self.tileSize))
                self.moveInfoIndicator.setText("Invalid Move")
        else:
            # Snap the piece back to its start position when the person releases it.
            self.piecePos[fromPos[1]][fromPos[0]].move(int(fromPos[0] * self.tileSize), int(fromPos[1] * self.tileSize))

    def checkKnightSpecial(self, fromPos, toPos, rules):
        # Once a knight has moved, see if the knight has an enemy piece in range.
        return rules.checkKnightSpecialInRange(self, toPos, self.piecePos[fromPos[1]][fromPos[0]].pieceColor, self.piecePos)

    def setKnightSpecial(self, target, setTo):
        if self.piecePos[target[1]][target[0]].pieceType == "knight" and setTo and not \
                self.piecePos[target[1]][target[0]].knightSpecial == True:
            self.piecePos[target[1]][target[0]].knightSpecial = True
            self.knightSpecialMovesRemaining += 1
        elif self.piecePos[target[1]][target[0]].pieceType == "knight" and not setTo and not \
                self.piecePos[target[1]][target[0]].knightSpecial == False:
            self.piecePos[target[1]][target[0]].knightSpecial = False
            if self.knightSpecialMovesRemaining > 0:
                self.knightSpecialMovesRemaining -= 1

    def givePieceToBishop(self, fromPos, toPos):
        # Give the piece command to the Bishop.
        self.piecePos[fromPos[1]][fromPos[0]].pieceCommander = self.piecePos[toPos[1]][toPos[0]].pieceCommander
        # Snap the piece back to its start position when the person releases it.
        self.piecePos[fromPos[1]][fromPos[0]].move(int(fromPos[0] * self.tileSize), int(fromPos[1] * self.tileSize))

    def moveOverGui(self, fromPos, toPos, commander):
        # Snap the piece to the nearest grid point when the person releases it.
        self.piecePos[fromPos[1]][fromPos[0]].move(int(toPos[0] * self.tileSize), int(toPos[1] * self.tileSize))

        self.moveThroughArray(fromPos, toPos, self.piecePos)

        self.moveHistory.append(PieceMoveInfo.PieceMoveInfo(fromPos, toPos))

        print("")
        for move in self.moveHistory:
            if self.turn == 0:
                print("From: " + str(move.getFromPos()) + " To: " + str(move.getToPos()) + "")
            else:
                print("From: " + str(move.getFromPos()) + " To: " + str(move.getToPos()) + "")

        self.boardInterface.updatePiecePosCopy(self.getPiecePos())

        # Set and check the moves remaining for the current player.
        self.checkSwitchTurn(commander)

    def moveThroughArray(self, fromPos, toPos, pieceList):
        # Copy this piece to destination.
        pieceList[toPos[1]][toPos[0]] = pieceList[fromPos[1]][fromPos[0]]

        # Remove it from the previous position.
        pieceList[fromPos[1]][fromPos[0]] = "0"

    def checkValidMove(self, fromPos, toPos, rules):
        # Use the appropriate rule from the rules classes to check the movement of the piece.
        return rules.isPathFree(self, fromPos, toPos, self.piecePos[fromPos[1]][fromPos[0]].pieceColor, self.piecePos)

    def checkAttackRange(self, fromPos, toPos, rules):
        # Use the appropriate rule from the rules classes to check the attack range of the piece.
        return rules.checkAttackInRange(self, fromPos, toPos, self.piecePos[fromPos[1]][fromPos[0]].pieceColor)

    def doCaptureAnim(self, fromPos, toPos, commander, rules):
        rollNeeded = rules.minRollNeeded(self, self.piecePos[toPos[1]][toPos[0]].pieceType)
        rollGot = rules.rollCapture(self)
        self.showAnimComponents(rollNeeded)
        self.rolledDie.raise_()
        self.animThread = AnimationThread(fromPos, toPos, commander, rollNeeded, rollGot, False)
        self.animThread.fallAnimation.connect(self.rolledDieAnimFall)
        self.animThread.updateAnimation.connect(self.rolledDieAnimUpdate)
        self.animThread.captureAnimation.connect(self.rolledDieAnimCapture)
        self.animThread.finishAnimation.connect(self.rolledDieAnimFinish)
        self.animThread.start()

    def doSpecialCaptureAnim(self, fromPos, toPos, commander, rules):
        rollNeeded = rules.minRollNeeded(self, self.piecePos[toPos[1]][toPos[0]].pieceType)
        rollGot = rules.rollCapture(self)
        self.showAnimComponents(rollNeeded)
        self.specialDieText.raise_()
        self.specialDieText.show()
        self.specialDie.raise_()
        self.specialDie.show()
        self.rolledDie.raise_()
        self.animThread = AnimationThread(fromPos, toPos, commander, rollNeeded, rollGot, True)
        self.animThread.fallAnimation.connect(self.rolledDieAnimFall)
        self.animThread.updateAnimation.connect(self.rolledDieAnimUpdate)
        self.animThread.captureAnimation.connect(self.rolledDieAnimCapture)
        self.animThread.finishAnimation.connect(self.rolledDieAnimFinish)
        self.animThread.start()

    def showAnimComponents(self, rollNeeded):
        # Sets up and shows most of the animation components
        self.pauseGame = True
        self.pauseBackground.raise_()
        self.pauseBackground.show()
        self.neededDieText.raise_()
        self.neededDieText.show()
        self.rolledDieText.raise_()
        self.rolledDieText.show()
        self.neededDie.raise_()
        self.neededDie.show()
        pixmap = QPixmap('../img/die' + str(rollNeeded))
        self.neededDie.setPixmap(pixmap)
        self.rolledDie.show()
        number = random.randint(1, 6)
        pixmap = QPixmap('../img/die' + str(number))
        self.rolledDie.setPixmap(pixmap)
        self.rolledDie.resize(self.rolledDie.width() + 255, self.rolledDie.height() + 255)
        self.rolledDie.move(int((self.boardSize / 2) - (self.rolledDie.width() / 2)), int(self.rolledDie.y() - 255))

    def rolledDieAnimFall(self):
        # Animate the opening fall
        self.rolledDie.resize(self.rolledDie.width() - 5, self.rolledDie.height() - 5)
        self.rolledDie.move(int((self.boardSize / 2) - (self.rolledDie.width() / 2)), int(self.rolledDie.y() + 5))

    def rolledDieAnimUpdate(self):
        # Animate the rolling of the die
        number = random.randint(1, 6)
        if self.previousRoll == number:
            if number == 6:
                number -= 1
            else:
                number += 1
        pixmap = QPixmap('../img/die' + str(number))
        self.previousRoll = number
        self.rolledDie.setPixmap(pixmap)

    def rolledDieAnimCapture(self, rollNeeded, rollGot, special):
        # Show the final verdict of the roll
        if special:
            pixmap = QPixmap('../img/die' + str(rollGot + 1))
        else:
            pixmap = QPixmap('../img/die' + str(rollGot))
        self.rolledDie.setPixmap(pixmap)
        if rollGot >= rollNeeded:
            self.captureRollText.setText("Attack Succeeded!")
        else:
            self.captureRollText.setText("Attack Failed!")
        self.captureRollText.raise_()
        self.captureRollText.show()

    def rolledDieAnimFinish(self, fromPos, toPos, commander, rollNeeded, rollGot):
        # Hide all animation components and do clean up work
        self.captureRollText.hide()
        self.pauseBackground.hide()
        self.specialDieText.hide()
        self.neededDieText.hide()
        self.rolledDieText.hide()
        self.specialDie.hide()
        self.neededDie.hide()
        self.rolledDie.hide()

        self.pauseGame = False
        if rollGot >= rollNeeded:
            if self.piecePos[fromPos[1]][fromPos[0]].pieceType == "knight":
                self.setKnightSpecial(fromPos, False)
            # Capture the piece.
            self.capturePiece(toPos)
            # Move the object through the array to match its movements on the gui.
            self.moveOverGui(fromPos, toPos, commander)
            self.moveInfoIndicator.setText("Captured Piece")
        else:
            if self.piecePos[fromPos[1]][fromPos[0]].pieceType == "knight":
                self.setKnightSpecial(fromPos, False)
            # Snap the piece back to its start position when the person releases it.
            self.piecePos[fromPos[1]][fromPos[0]].move(int(fromPos[0] * self.tileSize),
                                                       int(fromPos[1] * self.tileSize))
            # Set and check the moves remaining for the current player.
            self.checkSwitchTurn(commander)
            self.moveInfoIndicator.setText("Capture Failed")

    def capturePiece(self, target):
        # If the target is a bishop, hand its pieces to the king.
        if not self.piecePos[target[1]][target[0]] == "0" and self.piecePos[target[1]][target[0]].pieceType == "bishop":
            xIter = 0
            yIter = 0
            for row in self.piecePos:
                for tile in row:
                    if not self.piecePos[yIter][xIter] == "0" and \
                            not self.piecePos[yIter][xIter].pieceType == "bishop" and \
                            self.piecePos[yIter][xIter].pieceColor == self.piecePos[target[1]][target[0]].pieceColor \
                            and self.piecePos[yIter][xIter].pieceCommander == \
                            self.piecePos[target[1]][target[0]].pieceCommander:
                        self.piecePos[yIter][xIter].pieceCommander = 1
                    xIter += 1
                xIter = 0
                yIter += 1
        # If the target is a king, the capturing player wins.
        if not self.piecePos[target[1]][target[0]] == "0" and self.piecePos[target[1]][target[0]].pieceType == "king":
            self.gameOver = True
            if self.piecePos[target[1]][target[0]].pieceColor == 1:
                self.winner = "White"
            else:
                self.winner = "Black"
            self.skipButton.clicked.disconnect(self.skipButtonClicked)
            self.playerTurnsRemaining = [0, 0, 0]
            self.gameWinner.setText("Game Over!\n"
                                    "The Winner Is " + self.winner)
            self.pauseBackground.show()
            self.pauseBackground.raise_()
            self.gameWinner.show()
            self.gameWinner.raise_()
            self.resetButton.show()
            self.resetButton.raise_()

        # This deletes a piece from the board.
        self.piecePos[target[1]][target[0]].deleteLater()
        self.piecePos[target[1]][target[0]] = "0"


class AnimationThread(QThread):
    fallAnimation = pyqtSignal()
    updateAnimation = pyqtSignal()
    captureAnimation = pyqtSignal(int, int, bool)
    finishAnimation = pyqtSignal(list, list, int, int, int)

    def __init__(self, fromPos, toPos, commander, rollNeeded, rollGot, special):
        super(AnimationThread, self).__init__()

        self.fromPos = fromPos
        self.toPos = toPos
        self.commander = commander
        self.rollNeeded = rollNeeded
        self.rollGot = rollGot
        self.special = special

    def run(self):
        iterator = 0
        # Do the fall animation
        while True:
            self.fallAnimation.emit()
            sleep(0.0001)
            if iterator >= 50:
                break
            iterator += 1

        iterator = 0
        speed = 0.1
        sleep(speed)
        # Do the roll animation
        while True:
            self.updateAnimation.emit()
            if iterator % 10 == 0 or iterator % 15 == 0 or iterator % 17 == 0 or iterator % 18 == 0 or \
                    iterator % 19 == 0:
                speed += 0.1
            if iterator >= 20:
                break
            iterator += 1

            sleep(speed)

        if self.special:
            self.rollGot -= 1

        # Show the actual roll
        self.captureAnimation.emit(self.rollNeeded, self.rollGot, self.special)
        sleep(3)
        # Clean up
        self.finishAnimation.emit(self.fromPos, self.toPos, self.commander, self.rollNeeded, self.rollGot)


def chessBoard():
    app = QApplication(sys.argv)
    window = chessBoardWindow()

    window.show()
    sys.exit(app.exec_())


def main():
    chessBoard()


if __name__ == '__main__':
    main()
