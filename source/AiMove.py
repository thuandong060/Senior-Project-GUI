from PyQt5.QtCore import QThread, pyqtSignal
from source import PieceMoveInfo
from time import sleep
from datetime import datetime
from source import AiBrain
import random


class AiMove(QThread):
    moveDetermined = pyqtSignal(PieceMoveInfo.PieceMoveInfo)
    moveToBishop = pyqtSignal(PieceMoveInfo.PieceMoveInfo)
    aiSkipDetermined = pyqtSignal()

    def __init__(self, kingBoardInterface, bishop1BoardInterface, bishop2BoardInterface, movesRemaining, color):
        super(AiMove, self).__init__()
        self.overallBestMove = 0
        self.bishopMove = 0
        self.kingAi = 0
        self.bishopAi1 = 0
        self.bishopAi2 = 0
        self.kingMove = 0
        self.bishopMove1 = 0
        self.bishopMove2 = 0
        self.kingAiComplete = False
        self.bishopAi1Complete = False
        self.bishopAi2Complete = False
        self.kingBoardInterface = kingBoardInterface
        self.bishop1BoardInterface = bishop1BoardInterface
        self.bishop2BoardInterface = bishop2BoardInterface
        self.movesRemaining = movesRemaining
        self.color = color
        self.sendToBishop = False
        self.isRunning = True
        self.callsDebug = 0
        self.startTime = 0

    def stop(self):
        self.isRunning = False
        if not self.kingAi == 0:
            self.kingAi.stop()
        if not self.bishopAi1 == 0:
            self.bishopAi1.stop()
        if not self.bishopAi2 == 0:
            self.bishopAi2.stop()

    def run(self):
        self.nextMove()

    def kingAiFinished(self, move):
        self.kingAiComplete = True
        self.kingMove = move

    def bishopAi1Finished(self, move):
        self.bishopAi1Complete = True
        self.bishopMove1 = move

    def bishopAi2Finished(self, move):
        self.bishopAi2Complete = True
        self.bishopMove2 = move

    def kingAiNoMove(self):
        self.kingAiComplete = True

    def bishopAi1NoMove(self):
        self.bishopAi1Complete = True

    def bishopAi2NoMove(self):
        self.bishopAi2Complete = True

    def nextMove(self):
        if self.isRunning:
            self.startTime = datetime.now()
            sleep(1)


        if self.isRunning:
            print("White: " + str(self.kingBoardInterface.whiteKingPosition) + " " + str(self.kingBoardInterface.whiteBishop1Position) + " " + str(self.kingBoardInterface.whiteBishop2Position) +
                  "\n Black: "  + str(self.kingBoardInterface.blackKingPosition) + " " + str(self.kingBoardInterface.blackBishop1Position) + " " + str(self.kingBoardInterface.blackBishop2Position))

            # Setup the threads for the three AI parts.
            self.kingAi = AiBrain.AiBrain(self.kingBoardInterface, self.color, 1)
            self.kingAi.foundBestMove.connect(self.kingAiFinished)
            self.kingAi.noMove.connect(self.kingAiNoMove)
            self.kingAi.start()

            self.bishopAi1 = AiBrain.AiBrain(self.bishop1BoardInterface, self.color, 0)
            self.bishopAi1.foundBestMove.connect(self.bishopAi1Finished)
            self.bishopAi1.noMove.connect(self.bishopAi1NoMove)
            self.bishopAi1.start()

            self.bishopAi2 = AiBrain.AiBrain(self.bishop2BoardInterface, self.color, 2)
            self.bishopAi2.foundBestMove.connect(self.bishopAi2Finished)
            self.bishopAi2.noMove.connect(self.bishopAi2NoMove)
            self.bishopAi2.start()

        # Wait for all threads to finish.
        while self.isRunning and not (self.kingAiComplete and self.bishopAi1Complete and self.bishopAi2Complete):
            sleep(0.5)

        if self.isRunning:
            elapsedTime = datetime.now() - self.startTime

            # If 2.9 seconds have not elapsed, sleep until two seconds have passed.
            if (elapsedTime.seconds + (elapsedTime.microseconds / 1000000)) < 2.900:
                sleep(2.9 - (elapsedTime.seconds + (elapsedTime.microseconds / 1000000)))

            # Check which move of the three is the best.
            if not self.kingMove == 0 and self.movesRemaining[1] == 1:
                self.overallBestMove = self.kingMove
            elif not self.kingMove == 0 and (self.movesRemaining[0] == 1 or self.movesRemaining[2] == 1) and \
                    self.kingBoardInterface.turnCount > 1:
                rollSucceded = False
                if self.color == 0:
                    if self.kingBoardInterface.whiteKingPieceCount <= 6:
                        if random.randint(2, 24) <= self.kingBoardInterface.whiteKingPieceCount:
                            rollSucceded = True
                    else:
                        if random.randint(2, 12) <= self.kingBoardInterface.whiteKingPieceCount:
                            rollSucceded = True
                else:
                    if self.kingBoardInterface.blackKingPieceCount <= 6:
                        if random.randint(2, 24) <= self.kingBoardInterface.blackKingPieceCount:
                            rollSucceded = True
                    else:
                        if random.randint(2, 12) <= self.kingBoardInterface.blackKingPieceCount:
                            rollSucceded = True

                if rollSucceded:
                    self.sendToBishop = True
                    self.overallBestMove = self.kingMove

            if not self.bishopMove1 == 0 and (self.overallBestMove == 0 or self.bishopMove1.getValue() > self.overallBestMove.getValue()):
                self.sendToBishop = False
                self.overallBestMove = self.bishopMove1

            if not self.bishopMove2 == 0 and (self.overallBestMove == 0 or self.bishopMove2.getValue() > self.overallBestMove.getValue()):
                self.sendToBishop = False
                self.overallBestMove = self.bishopMove2

        # If the game is paused, wait.
        while self.isRunning and self.kingBoardInterface.getPaused():
            sleep(2.9)

        if self.isRunning:
            # If no move was chosen, skip the turn.
            if self.overallBestMove == 0:
                self.aiSkipDetermined.emit()
            # If the king wants to give its piece to a bishop, set that up and do it.
            elif self.sendToBishop:
                print("They did give to bishop")

                if self.color == 0:
                    if self.movesRemaining[0] == 1 and self.movesRemaining[2] == 1:
                        if self.kingBoardInterface.whiteBishop1PieceCount < self.kingBoardInterface.whiteBishop2PieceCount:
                            self.bishopMove = PieceMoveInfo.PieceMoveInfo(self.overallBestMove.getFromPos(),
                                                                     self.kingBoardInterface.whiteBishop1Position)
                        else:
                            self.bishopMove = PieceMoveInfo.PieceMoveInfo(self.overallBestMove.getFromPos(),
                                                                     self.kingBoardInterface.whiteBishop2Position)
                    elif self.movesRemaining[0] == 1:
                        self.bishopMove = PieceMoveInfo.PieceMoveInfo(self.overallBestMove.getFromPos(),
                                                                 self.kingBoardInterface.whiteBishop1Position)
                    else:
                        self.bishopMove = PieceMoveInfo.PieceMoveInfo(self.overallBestMove.getFromPos(),
                                                                 self.kingBoardInterface.whiteBishop2Position)
                else:
                    if self.movesRemaining[0] == 1 and self.movesRemaining[2] == 1:
                        if self.kingBoardInterface.blackBishop1PieceCount < self.kingBoardInterface.blackBishop2PieceCount:
                            self.bishopMove = PieceMoveInfo.PieceMoveInfo(self.overallBestMove.getFromPos(),
                                                                     self.kingBoardInterface.blackBishop1Position)
                        else:
                            self.bishopMove = PieceMoveInfo.PieceMoveInfo(self.overallBestMove.getFromPos(),
                                                                     self.kingBoardInterface.blackBishop2Position)
                    elif self.movesRemaining[0] == 1:
                        self.bishopMove = PieceMoveInfo.PieceMoveInfo(self.overallBestMove.getFromPos(),
                                                                 self.kingBoardInterface.blackBishop1Position)
                    else:
                        self.bishopMove = PieceMoveInfo.PieceMoveInfo(self.overallBestMove.getFromPos(),
                                                                 self.kingBoardInterface.blackBishop2Position)
                if self.isRunning:
                    self.moveToBishop.emit(self.bishopMove)

                sleep(2.9)

                if self.isRunning:
                    self.moveDetermined.emit(self.overallBestMove)
            # If the AI wants to do a normal move, emit it.
            else:
                self.moveDetermined.emit(self.overallBestMove)
