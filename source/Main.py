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
        self.kingInterface = BoardInterface.BoardInterface(self)
        self.bishopInterface1 = BoardInterface.BoardInterface(self)
        self.bishopInterface2 = BoardInterface.BoardInterface(self)

        # Move list
        self.moveHistory = []

        # Used when the game needs to be paused.
        self.pauseGame = False

        # Used so the game doesn't unpause if paused.
        self.pauseButtonWasClicked = False

        # Pause background
        self.pauseBackground = QLabel(self)

        # This block sets up the window properties.
        self.setGeometry(400, 200, 300, 300)
        self.setWindowTitle('Chessboard')

        # Choose side text
        self.chooseSideText = QLabel(self)

        # Side buttons
        self.chooseWhiteSide = QPushButton("White Side", self)
        self.chooseBlackSide = QPushButton("Black Side", self)
        self.chooseSpectate = QPushButton("Spectate", self)

        # 0 for white, 1 for black
        self.turn = 0
        self.player = 0
        self.moveIndicator = QLabel(self)

        # Shows remaining moves.
        self.remainingMoveIndicator = QLabel(self)

        # Shows game info.
        self.moveInfoIndicator = QLabel(self)

        # Shows when the game is won.
        self.gameWinner = QLabel(self)

        # Button so you can skip your turn.
        self.skipButton = QPushButton("End Turn", self)

        # Button so you can pause the game.
        self.pauseButton = QPushButton("Pause", self)

        # Button so you can reset the game after it ends.
        self.resetButton = QPushButton("Reset Board", self)

        # Button so you can reset the game before it ends.
        self.resetButtonPersistent = QPushButton("Reset Board", self)

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

        self.whiteTurnsRemaining = [0, 0, 0]
        self.blackTurnsRemaining = [0, 0, 0]

        self.knightSpecialMovesRemaining = 0
        self.gameOver = False
        self.aiWasRunning = False
        self.dieWasRolling = False
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

        # Holds labels for tiles highlights.
        self.tileHighlightsPos = [["0", "0", "0", "0", "0", "0", "0", "0"],
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

        '''
        self.pieceSet = [["0", "0", "0", "0", "bki", "0", "0", "0"],
                         ["0", "0", "0", "0", "0", "0", "0", "0"],
                         ["0", "0", "0", "0", "0", "0", "0", "0"],
                         ["0", "0", "0", "0", "0", "0", "0", "0"],
                         ["0", "0", "0", "0", "0", "0", "0", "0"],
                         ["0", "0", "0", "0", "0", "0", "0", "0"],
                         ["0", "0", "0", "0", "0", "0", "0", "0"],
                         ["0", "0", "0", "0", "wki", "0", "0", "0"]]
        '''


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

    def getWhiteTurnsRemaining(self):
        return self.whiteTurnsRemaining

    def getBlackTurnsRemaining(self):
        return self.blackTurnsRemaining

    def getPiecePos(self):
        return self.piecePos

    def getMoveHistory(self):
        return self.moveHistory

    def getPaused(self):
        return self.pauseGame

    # Normal Functions
    def resetBoardWithChecks(self):
        if self.pauseGame:
            self.pauseButtonClicked()

        if self.aiWasRunning:
            self.aiThread.stop()
            self.aiWasRunning = False
            self.resetBoard()
        elif self.dieWasRolling:
            self.animThread.stop()
            self.dieWasRolling = False
            self.hideDieAnimComponents()
            self.resetBoard()
        else:
            self.resetBoard()

    def resetBoard(self):
        # Reset the game
        self.pauseGame = False
        self.pauseButtonWasClicked = False
        self.pauseButton.setText("Pause")

        self.moveHistory = []
        self.turn = 0
        self.player = 0
        self.whiteTurnsRemaining = [0, 0, 0]
        self.blackTurnsRemaining = [0, 0, 0]
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

        self.checkBishopsRemaining(0)
        self.checkBishopsRemaining(1)

        # Remove highlights
        self.clearHighlights()

        # Change piece colors
        self.setCommanderColor()

        self.moveIndicator.setText("Turn: White")
        self.remainingMoveIndicator.setText("Remaining Moves:"
                                            "\nLeft Corp: " + str(self.whiteTurnsRemaining[0]) +
                                            "\nCenter Corp: " + str(self.whiteTurnsRemaining[1]) +
                                            "\nRight Corp: " + str(self.whiteTurnsRemaining[2]))

        self.kingInterface.updatePiecePosCopy(self.getPiecePos())
        self.kingInterface.updateWhiteTurnsRemaining()
        self.kingInterface.updateBlackTurnsRemaining()
        self.kingInterface.updateKingPositions()

        self.bishopInterface1.updatePiecePosCopy(self.getPiecePos())
        self.bishopInterface1.updateWhiteTurnsRemaining()
        self.bishopInterface1.updateBlackTurnsRemaining()
        self.bishopInterface1.updateKingPositions()

        self.bishopInterface2.updatePiecePosCopy(self.getPiecePos())
        self.bishopInterface2.updateWhiteTurnsRemaining()
        self.bishopInterface2.updateBlackTurnsRemaining()
        self.bishopInterface2.updateKingPositions()

        self.showSideChoice()

    def showBoard(self):
        # Initialize the board.
        self.setBoard()
        self.showSideChoice()
        self.resize(self.boardSize + self.moveIndicator.width(), self.boardSize)

    def setBoard(self):
        self.tileSize = 75
        self.boardSize = self.tileSize * 8
        self.addBoardComponents(self.tileSet, self.tilePos)
        self.addHighlightBoardComponents()
        self.addBoardComponents(self.pieceSet, self.piecePos)

        self.checkBishopsRemaining(0)
        self.checkBishopsRemaining(1)

        # Change piece colors
        self.setCommanderColor()

        # Set up choose side text properties
        self.chooseSideText.setAlignment(Qt.AlignCenter)
        self.chooseSideText.setText("Choose Your Side")
        self.chooseSideText.resize(500, 100)
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.chooseSideText.height() * 0.4)
        self.chooseSideText.setFont(font)
        self.chooseSideText.setStyleSheet('font-weight: bold; color: rgba(0, 255, 255, 255)')
        self.chooseSideText.move(int((self.boardSize / 2) - (self.chooseSideText.width() / 2)),
                                int((self.boardSize / 2) - 300))
        self.chooseSideText.hide()

        # Set up the choose white side properties
        self.chooseWhiteSide.clicked.connect(self.whiteSideChoosen)
        self.chooseWhiteSide.resize(150, self.chooseWhiteSide.height())
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.chooseWhiteSide.height() * 0.6)
        self.chooseWhiteSide.setFont(font)
        self.chooseWhiteSide.move(int((self.boardSize / 2) - (self.chooseWhiteSide.width() / 2)), int(self.boardSize / 2 + 150))
        self.chooseWhiteSide.hide()

        # Set up the choose black side properties
        self.chooseBlackSide.clicked.connect(self.blackSideChoosen)
        self.chooseBlackSide.resize(150, self.chooseBlackSide.height())
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.chooseBlackSide.height() * 0.6)
        self.chooseBlackSide.setFont(font)
        self.chooseBlackSide.move(int((self.boardSize / 2) - (self.chooseBlackSide.width() / 2)), int(self.boardSize / 2 - 180))
        self.chooseBlackSide.hide()

        # Set up the choose spectate properties
        self.chooseSpectate.clicked.connect(self.spectateChoosen)
        self.chooseSpectate.resize(150, self.chooseSpectate.height())
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.chooseSpectate.height() * 0.6)
        self.chooseSpectate.setFont(font)
        self.chooseSpectate.move(int((self.boardSize / 2) - (self.chooseSpectate.width() / 2)), int(self.boardSize / 2 - 15))
        self.chooseSpectate.hide()

        # Set up the move indicator properties
        self.moveIndicator.setText("Turn: White")
        self.moveIndicator.setAlignment(Qt.AlignCenter)
        self.moveIndicator.resize(200, 25)
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.moveIndicator.height() * 0.8)
        self.moveIndicator.setFont(font)
        self.moveIndicator.move(int(self.boardSize), int(self.boardSize / 2 - 75) - (self.moveIndicator.height() / 2))

        # Set up remaining move indicator
        self.remainingMoveIndicator.setText("Remaining Moves:"
                                            "\nLeft Corp: " + str(self.whiteTurnsRemaining[0]) +
                                            "\nCenter Corp: " + str(self.whiteTurnsRemaining[1]) +
                                            "\nRight Corp: " + str(self.whiteTurnsRemaining[2]))
        self.remainingMoveIndicator.setAlignment(Qt.AlignCenter)
        self.remainingMoveIndicator.resize(200, 100)
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.remainingMoveIndicator.height() * 0.2)
        self.remainingMoveIndicator.setFont(font)
        self.remainingMoveIndicator.move(int(self.boardSize), int(self.boardSize / 2)
                                         - (self.remainingMoveIndicator.height() / 2))

        # Set up the play indicator properties
        self.moveInfoIndicator.setText("")
        self.moveInfoIndicator.setAlignment(Qt.AlignCenter)
        self.moveInfoIndicator.resize(200, 50)
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.moveInfoIndicator.height() * 0.4)
        self.moveInfoIndicator.setFont(font)
        self.moveInfoIndicator.move(int(self.boardSize), int(self.boardSize / 2 + 75)
                                    - (self.moveIndicator.height() / 2))

        # Set up pause overlay
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
                             int(self.boardSize / 2 + 250) - (self.skipButton.height() / 2))

        # Set up pause button
        self.pauseButton.clicked.connect(self.pauseButtonClicked)
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.pauseButton.height() * 0.6)
        self.pauseButton.setFont(font)
        self.pauseButton.move(int(self.boardSize - ((self.pauseButton.width() - self.moveIndicator.width()) / 2)),
                             int(self.boardSize / 2 + 200) - (self.pauseButton.height() / 2))

        # Set up reset button
        self.resetButton.clicked.connect(self.resetBoard)
        self.resetButton.resize(150, self.resetButton.height())
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.resetButton.height() * 0.6)
        self.resetButton.setFont(font)
        self.resetButton.move(int((self.boardSize / 2) - (self.resetButton.width() / 2)), int(self.boardSize / 2 + 100))
        self.resetButton.hide()

        # Set up reset button persistent
        self.resetButtonPersistent.clicked.connect(self.resetBoardWithChecks)
        self.resetButtonPersistent.resize(150, self.resetButtonPersistent.height())
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.resetButtonPersistent.height() * 0.6)
        self.resetButtonPersistent.setFont(font)
        self.resetButtonPersistent.move(int(self.boardSize - ((self.resetButtonPersistent.width() -
                                                               self.moveIndicator.width()) / 2)),
                                        int(self.boardSize / 2 - 250) - (self.resetButton.height() / 2))

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
        self.rolledDieText.setText("White's Roll:")
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
        self.neededDieText.setText("Roll Needed For\nWhite To Capture Piece:")
        self.neededDieText.resize(500, 100)
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

        self.kingInterface.updatePiecePosCopy(self.getPiecePos())
        self.kingInterface.updateWhiteTurnsRemaining()
        self.kingInterface.updateBlackTurnsRemaining()
        self.kingInterface.updateKingPositions()

        self.bishopInterface1.updatePiecePosCopy(self.getPiecePos())
        self.bishopInterface1.updateWhiteTurnsRemaining()
        self.bishopInterface1.updateBlackTurnsRemaining()
        self.bishopInterface1.updateKingPositions()

        self.bishopInterface2.updatePiecePosCopy(self.getPiecePos())
        self.bishopInterface2.updateWhiteTurnsRemaining()
        self.bishopInterface2.updateBlackTurnsRemaining()
        self.bishopInterface2.updateKingPositions()

    def showSideChoice(self):
        self.skipButton.clicked.disconnect(self.skipButtonClicked)
        self.pauseButton.clicked.disconnect(self.pauseButtonClicked)
        self.resetButtonPersistent.clicked.disconnect(self.resetBoardWithChecks)
        self.pauseBackground.show()
        self.pauseBackground.raise_()
        self.chooseSideText.show()
        self.chooseSideText.raise_()
        self.chooseWhiteSide.show()
        self.chooseWhiteSide.raise_()
        self.chooseBlackSide.show()
        self.chooseBlackSide.raise_()
        self.chooseSpectate.show()
        self.chooseSpectate.raise_()

    def hideSideChoice(self):
        self.skipButton.clicked.connect(self.skipButtonClicked)
        self.pauseButton.clicked.connect(self.pauseButtonClicked)
        self.resetButtonPersistent.clicked.connect(self.resetBoardWithChecks)
        self.pauseBackground.hide()
        self.chooseSideText.hide()
        self.chooseWhiteSide.hide()
        self.chooseBlackSide.hide()
        self.chooseSpectate.hide()

    def whiteSideChoosen(self):
        self.player = 0
        self.hideSideChoice()

    def blackSideChoosen(self):
        self.player = 1
        self.aiWasRunning = True
        self.aiMoveThread(self.whiteTurnsRemaining, 0)
        self.hideSideChoice()

    def spectateChoosen(self):
        self.player = -1
        self.aiWasRunning = True
        self.aiMoveThread(self.whiteTurnsRemaining, 0)
        self.hideSideChoice()

    def setCommanderColor(self):
        for row in self.piecePos:
            for tile in row:
                if not tile == "0" :
                    outline = ""
                    color = "w"
                    type = "p"

                    if self.turn == 0:
                        if tile.knightSpecial:
                            outline = "pr"
                        elif tile.pieceCommander == 1 and tile.pieceColor == self.turn and \
                                self.whiteTurnsRemaining[1] == 1:
                            outline = "bl"
                        elif tile.pieceCommander == 0 and tile.pieceColor == self.turn and \
                                self.whiteTurnsRemaining[0] == 1:
                            outline = "gr"
                        elif tile.pieceCommander == 2 and tile.pieceColor == self.turn and \
                                self.whiteTurnsRemaining[2] == 1:
                            outline = "rd"
                    else:
                        if tile.knightSpecial:
                            outline = "pr"
                        elif tile.pieceCommander == 1 and tile.pieceColor == self.turn and \
                                self.blackTurnsRemaining[1] == 1:
                            outline = "bl"
                        elif tile.pieceCommander == 0 and tile.pieceColor == self.turn and \
                                self.blackTurnsRemaining[0] == 1:
                            outline = "gr"
                        elif tile.pieceCommander == 2 and tile.pieceColor == self.turn and \
                                self.blackTurnsRemaining[2] == 1:
                            outline = "rd"

                    if tile.pieceColor == 1:
                        color = "b"

                    if tile.pieceType == "knight":
                        type = "k"
                    elif tile.pieceType == "king":
                        type = "ki"
                    elif tile.pieceType == "queen":
                        type = "q"
                    elif tile.pieceType == "rook":
                        type = "r"
                    elif tile.pieceType == "bishop":
                        type = "b"

                    pixmap = QPixmap('../img/' + color + type + outline)
                    tile.setPixmap(pixmap)

    def addHighlightBoardComponents(self):
        # These are used as iterators to move through the arrays.
        xIter = 0
        yIter = 0

        # Iterate through all tiles in the tile set array and create images for them.
        # The images are stored in another array that can be manipulated.
        for row in self.tileHighlightsPos:
            for tile in row:
                # Add the highlight image
                label = QLabel(self)
                label.resize(75, 75)
                pixmap = QPixmap('../img/yt')
                label.setPixmap(pixmap)
                label.setScaledContents(True)
                label.move(int(xIter * self.tileSize), int(yIter * self.tileSize))
                label.hide()

                # Move the new label to the label array.
                self.tileHighlightsPos[yIter][xIter] = label

                xIter += 1
            xIter = 0
            yIter += 1

    def skipButtonClicked(self):
        if not self.gameOver and self.turn == self.player:
            self.switchTurn()

    def pauseButtonClicked(self):
        if self.pauseButtonWasClicked == False:
            self.pauseGame = True
            self.pauseButtonWasClicked = True
            self.pauseButton.setText("Resume")
        else:
            self.pauseGame = False
            self.pauseButtonWasClicked = False
            self.pauseButton.setText("Pause")

            if self.turn == 0:
                if self.whiteTurnsRemaining[0] + self.whiteTurnsRemaining[1] + self.whiteTurnsRemaining[2] == 0 and \
                        self.knightSpecialMovesRemaining == 0:
                    self.switchTurn()
            else:
                if self.blackTurnsRemaining[0] + self.blackTurnsRemaining[1] + self.blackTurnsRemaining[2] == 0 and \
                        self.knightSpecialMovesRemaining == 0:
                    self.switchTurn()

    def checkSwitchTurn(self, commander):
        # Remove the move authority from the current commander and check to see if all command authority is removed.
        if self.turn == 0:
            self.whiteTurnsRemaining[commander] = 0
            self.remainingMoveIndicator.setText("Remaining Moves:"
                                                "\nLeft Corp: " + str(self.whiteTurnsRemaining[0]) +
                                                "\nCenter Corp: " + str(self.whiteTurnsRemaining[1]) +
                                                "\nRight Corp: " + str(self.whiteTurnsRemaining[2]))
        else:
            self.blackTurnsRemaining[commander] = 0
            self.remainingMoveIndicator.setText("Remaining Moves:"
                                                "\nLeft Corp: " + str(self.blackTurnsRemaining[0]) +
                                                "\nCenter Corp: " + str(self.blackTurnsRemaining[1]) +
                                                "\nRight Corp: " + str(self.blackTurnsRemaining[2]))

        # Change piece colors
        self.setCommanderColor()

        if self.turn == 0:
            if self.whiteTurnsRemaining[0] + self.whiteTurnsRemaining[1] + self.whiteTurnsRemaining[2] == 0 and \
                    self.knightSpecialMovesRemaining == 0:
                self.switchTurn()
            elif not self.gameOver and not self.player == 0:
                self.aiWasRunning = True
                self.aiMoveThread(self.whiteTurnsRemaining, 0)
        else:
            if self.blackTurnsRemaining[0] + self.blackTurnsRemaining[1] + self.blackTurnsRemaining[2] == 0 and \
                    self.knightSpecialMovesRemaining == 0:
                self.switchTurn()
            elif not self.gameOver and not self.player == 1:
                self.aiWasRunning = True
                self.aiMoveThread(self.blackTurnsRemaining, 1)

    def switchTurn(self):
        # Switch the turn to the other person and update the UI.
        if not self.pauseGame:
            self.knightSpecialMovesRemaining = 0

            self.whiteTurnsRemaining = [0, 0, 0]
            self.blackTurnsRemaining = [0, 0, 0]

            if not self.gameOver:
                self.checkBishopsRemaining(0)
                self.checkBishopsRemaining(1)

                self.kingInterface.updateWhiteTurnsRemaining()
                self.kingInterface.updateBlackTurnsRemaining()

                self.bishopInterface1.updateWhiteTurnsRemaining()
                self.bishopInterface1.updateBlackTurnsRemaining()

                self.bishopInterface2.updateWhiteTurnsRemaining()
                self.bishopInterface2.updateBlackTurnsRemaining()

            if self.turn == 0:
                self.turn = 1
                self.moveIndicator.setText("Turn: Black")
                self.remainingMoveIndicator.setText("Remaining Moves:"
                                                    "\nLeft Corp: " + str(self.blackTurnsRemaining[0]) +
                                                    "\nCenter Corp: " + str(self.blackTurnsRemaining[1]) +
                                                    "\nRight Corp: " + str(self.blackTurnsRemaining[2]))
            else:
                self.turn = 0
                self.moveIndicator.setText("Turn: White")
                self.remainingMoveIndicator.setText("Remaining Moves:"
                                                    "\nLeft Corp: " + str(self.whiteTurnsRemaining[0]) +
                                                    "\nCenter Corp: " + str(self.whiteTurnsRemaining[1]) +
                                                    "\nRight Corp: " + str(self.whiteTurnsRemaining[2]))

            # Change piece colors
            self.setCommanderColor()

            if not self.gameOver and self.turn == 0 and not self.player == 0:
                self.aiWasRunning = True
                self.aiMoveThread(self.whiteTurnsRemaining, 0)
            elif not self.gameOver and self.turn == 1 and not self.player == 1:
                self.aiWasRunning = True
                self.aiMoveThread(self.blackTurnsRemaining, 1)

    def aiMoveThread(self, movesRemaining, color):
        self.aiThread = AiMove.AiMove(self.kingInterface, self.bishopInterface1, self.bishopInterface2,
                                      movesRemaining, color)
        self.aiThread.moveDetermined.connect(self.aiMoveThreadFinish)
        self.aiThread.moveToBishop.connect(self.aiMoveThreadBishop)
        self.aiThread.aiSkipDetermined.connect(self.aiMoveThreadSkip)
        self.aiThread.start()

    def aiMoveThreadFinish(self, move):
        self.aiWasRunning = False
        self.movePiece(move.getFromPos(), move.getToPos())

    def aiMoveThreadBishop(self, move):
        self.movePiece(move.getFromPos(), move.getToPos())

    def aiMoveThreadSkip(self):
        self.aiWasRunning = False
        self.switchTurn()

    def checkBishopsRemaining(self, color):
        # Set the command points based on how many bishops the players have left.
        if color == 0:
            self.whiteTurnsRemaining[1] = 1
        else:
            self.blackTurnsRemaining[1] = 1

        xIter = 0
        yIter = 0
        for row in self.piecePos:
            for tile in row:
                if not self.piecePos[yIter][xIter] == "0" and self.piecePos[yIter][xIter].pieceColor == color and \
                        self.piecePos[yIter][xIter].pieceType == "bishop":
                    if color == 0:
                        self.whiteTurnsRemaining[self.piecePos[yIter][xIter].pieceCommander] = 1
                    else:
                        self.blackTurnsRemaining[self.piecePos[yIter][xIter].pieceCommander] = 1
                if not self.piecePos[yIter][xIter] == "0" and self.piecePos[yIter][xIter].pieceType == "knight":
                    self.piecePos[yIter][xIter].knightSpecial = False
                xIter += 1
            xIter = 0
            yIter += 1

    def movePiece(self, fromPos, toPos):
        if self.turn == 0:
            turnsRemaining = self.whiteTurnsRemaining
        else:
            turnsRemaining = self.blackTurnsRemaining

        if not fromPos == toPos and not self.piecePos[fromPos[1]][fromPos[0]] == "0":
            path = self.checkValidMove(fromPos, toPos, self.piecePos[fromPos[1]][fromPos[0]].rules)
            # Player is trying to move onto a piece
            if not self.piecePos[toPos[1]][toPos[0]] == "0" and not self.piecePos[fromPos[1]][fromPos[0]].knightSpecial:
                # Try to capture a piece
                if not turnsRemaining[self.piecePos[fromPos[1]][fromPos[0]].pieceCommander] == 0 and \
                        not self.piecePos[fromPos[1]][fromPos[0]].pieceColor == \
                            self.piecePos[toPos[1]][toPos[0]].pieceColor:
                    if self.checkAttackRange(fromPos, toPos, self.piecePos[fromPos[1]][fromPos[0]].rules):
                        # Snap the piece back to its start position when the person releases it.
                        self.piecePos[fromPos[1]][fromPos[0]].move(int(fromPos[0] * self.tileSize),
                                                                   int(fromPos[1] * self.tileSize))
                        self.dieWasRolling = True

                        # Highlight Attacking Pieces
                        self.clearHighlights()
                        self.highlightPathway([fromPos, toPos], True)

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
                        print("BAD MOVE" + str(fromPos) + str(toPos))
            # Else, the player is trying to move to an empty space.
            elif not self.piecePos[fromPos[1]][fromPos[0]].knightSpecial and \
                    not turnsRemaining[self.piecePos[fromPos[1]][fromPos[0]].pieceCommander] == 0 and \
                    len(path) > 0:
                if self.piecePos[fromPos[1]][fromPos[0]].pieceType == "knight":
                    if self.checkKnightSpecial(fromPos, toPos, self.piecePos[fromPos[1]][fromPos[0]].rules):
                        self.setKnightSpecial(fromPos, True)
                    else:
                        self.setKnightSpecial(fromPos, False)
                # Clear Highlights
                self.clearHighlights()

                # Move the object through the array to match its movements on the gui.
                self.moveOverGui(fromPos, toPos, self.piecePos[fromPos[1]][fromPos[0]].pieceCommander)
                self.moveInfoIndicator.setText("")

                # Highlight the path of the piece
                self.highlightPathway(path, False)
            # Knight is performing a special attack.
            elif not self.piecePos[toPos[1]][toPos[0]] == "0" and \
                    self.piecePos[fromPos[1]][fromPos[0]].pieceType == "knight" and \
                    self.piecePos[fromPos[1]][fromPos[0]].knightSpecial:
                # Try to capture a piece
                if not self.piecePos[fromPos[1]][fromPos[0]].pieceColor == self.piecePos[toPos[1]][toPos[0]].pieceColor:
                    if self.checkAttackRange(fromPos, toPos, self.piecePos[fromPos[1]][fromPos[0]].rules):
                        # Snap the piece back to its start position when the person releases it.
                        self.piecePos[fromPos[1]][fromPos[0]].move(int(fromPos[0] * self.tileSize),
                                                                   int(fromPos[1] * self.tileSize))
                        self.dieWasRolling = True

                        # Highlight Attacking Pieces
                        self.clearHighlights()
                        self.highlightPathway([fromPos, toPos], True)

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
                        print("BAD MOVE" + str(fromPos) + str(toPos))
            # No command point for this piece
            elif not self.piecePos[fromPos[1]][fromPos[0]].knightSpecial and \
                    turnsRemaining[self.piecePos[fromPos[1]][fromPos[0]].pieceCommander] == 0 and \
                    len(path) > 0:
                # Snap the piece back to its start position when the person releases it.
                self.piecePos[fromPos[1]][fromPos[0]].move(int(fromPos[0] * self.tileSize),
                                                           int(fromPos[1] * self.tileSize))
                self.moveInfoIndicator.setText("No Command Point\nFor This Piece")
            else:
                # Snap the piece back to its start position when the person releases it.
                self.piecePos[fromPos[1]][fromPos[0]].move(int(fromPos[0] * self.tileSize),
                                                           int(fromPos[1] * self.tileSize))
                self.moveInfoIndicator.setText("Invalid Move")
                print("BAD MOVE" + str(fromPos) + str(toPos))
        elif not self.piecePos[fromPos[1]][fromPos[0]] == "0":
            # Snap the piece back to its start position when the person releases it.
            self.piecePos[fromPos[1]][fromPos[0]].move(int(fromPos[0] * self.tileSize), int(fromPos[1] * self.tileSize))

    def highlightPathway(self, path, invert):
        for tile in path:
            if invert:
                self.tileHighlightsPos[tile[1]][tile[0]].show()
            else:
                self.tileHighlightsPos[tile[0]][tile[1]].show()

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
        # Check if the piece is a Knight with a special move remaining.
        self.setKnightSpecial(fromPos, False)
        # Change piece colors
        self.setCommanderColor()

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

        self.kingInterface.updatePiecePosCopy(self.getPiecePos())
        self.kingInterface.updateWhiteTurnsRemaining()
        self.kingInterface.updateBlackTurnsRemaining()
        self.kingInterface.updateKingPositions()

        self.bishopInterface1.updatePiecePosCopy(self.getPiecePos())
        self.bishopInterface1.updateWhiteTurnsRemaining()
        self.bishopInterface1.updateBlackTurnsRemaining()
        self.bishopInterface1.updateKingPositions()

        self.bishopInterface2.updatePiecePosCopy(self.getPiecePos())
        self.bishopInterface2.updateWhiteTurnsRemaining()
        self.bishopInterface2.updateBlackTurnsRemaining()
        self.bishopInterface2.updateKingPositions()

        # Set and check the moves remaining for the current player.
        self.checkSwitchTurn(commander)

    def clearHighlights(self):
        xIter = 0
        yIter = 0

        for row in self.tileHighlightsPos:
            for tile in row:
                self.tileHighlightsPos[yIter][xIter].hide()

                xIter += 1
            xIter = 0
            yIter += 1

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
        self.pauseGame = True
        rollNeeded = rules.minRollNeeded(self, self.piecePos[toPos[1]][toPos[0]].pieceType)
        rollGot = rules.rollCapture(self)
        self.animThread = AnimationThread(fromPos, toPos, commander, rollNeeded, rollGot, False)
        self.animThread.setupAnimation.connect(self.showAnimComponents)
        self.animThread.fallAnimation.connect(self.rolledDieAnimFall)
        self.animThread.updateAnimation.connect(self.rolledDieAnimUpdate)
        self.animThread.captureAnimation.connect(self.rolledDieAnimCapture)
        self.animThread.finishAnimation.connect(self.rolledDieAnimFinish)
        self.animThread.start()

    def doSpecialCaptureAnim(self, fromPos, toPos, commander, rules):
        self.pauseGame = True
        rollNeeded = rules.minRollNeeded(self, self.piecePos[toPos[1]][toPos[0]].pieceType)
        rollGot = rules.rollCapture(self)
        self.animThread = AnimationThread(fromPos, toPos, commander, rollNeeded, rollGot, True)
        self.animThread.setupAnimation.connect(self.showAnimComponents)
        self.animThread.setupSpecialAnimation.connect(self.showAnimComponentsSpecial)
        self.animThread.fallAnimation.connect(self.rolledDieAnimFall)
        self.animThread.updateAnimation.connect(self.rolledDieAnimUpdate)
        self.animThread.captureAnimation.connect(self.rolledDieAnimCapture)
        self.animThread.finishAnimation.connect(self.rolledDieAnimFinish)
        self.animThread.start()

    def showAnimComponents(self, rollNeeded):
        # Sets up and shows most of the animation components
        self.pauseBackground.raise_()
        self.pauseBackground.show()
        if self.turn == 0:
            self.neededDieText.setText("Roll Needed For\nWhite To Capture Piece:")
            self.rolledDieText.setText("White's Roll:")
        else:
            self.neededDieText.setText("Roll Needed For\nBlack To Capture Piece:")
            self.rolledDieText.setText("Black's Roll:")
        self.neededDieText.raise_()
        self.neededDieText.show()
        self.rolledDieText.raise_()
        self.rolledDieText.show()
        self.neededDie.raise_()
        self.neededDie.show()
        pixmap = QPixmap('../img/die' + str(rollNeeded))
        self.neededDie.setPixmap(pixmap)
        self.rolledDie.raise_()
        self.rolledDie.show()
        number = random.randint(1, 6)
        pixmap = QPixmap('../img/die' + str(number))
        self.rolledDie.setPixmap(pixmap)
        self.rolledDie.resize(self.rolledDie.width() + 255, self.rolledDie.height() + 255)
        self.rolledDie.move(int((self.boardSize / 2) - (self.rolledDie.width() / 2)), int(self.rolledDie.y() - 255))

    def showAnimComponentsSpecial(self):
        # Sets up and shows the animation components for the special Animation
        self.specialDieText.raise_()
        self.specialDieText.show()
        self.specialDie.raise_()
        self.specialDie.show()
        self.rolledDie.raise_()

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
        self.hideDieAnimComponents()
        if self.pauseButtonWasClicked == False:
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

    def hideDieAnimComponents(self):
        # Hide all animation components and do clean up work
        self.captureRollText.hide()
        self.pauseBackground.hide()
        self.specialDieText.hide()
        self.neededDieText.hide()
        self.rolledDieText.hide()
        self.specialDie.hide()
        self.neededDie.hide()
        self.rolledDie.hide()

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
            self.whiteTurnsRemaining = [0, 0, 0]
            self.blackTurnsRemaining = [0, 0, 0]
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
    setupAnimation = pyqtSignal(int)
    setupSpecialAnimation = pyqtSignal()
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
        self.running = True

    def stop(self):
        self.running = False

    def run(self):
        if self.running:
            sleep(2)

        if self.running:
            self.setupAnimation.emit(self.rollNeeded)

            if self.special:
                self.setupSpecialAnimation.emit()

            iterator = 0

        # Do the fall animation
        while self.running:
            self.fallAnimation.emit()
            sleep(0.0001)
            if iterator >= 50:
                break
            iterator += 1

        if self.running:
            iterator = 0
            speed = 0.1
            sleep(speed)

        # Do the roll animation
        while self.running:
            self.updateAnimation.emit()
            if iterator % 10 == 0 or iterator % 15 == 0 or iterator % 17 == 0 or iterator % 18 == 0 or \
                    iterator % 19 == 0:
                speed += 0.1
            if iterator >= 20:
                break
            iterator += 1

            sleep(speed)

        if self.running:
            if self.special:
                self.rollGot -= 1

            # Show the actual roll
            self.captureAnimation.emit(self.rollNeeded, self.rollGot, self.special)
            sleep(3)

        if self.running:
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
