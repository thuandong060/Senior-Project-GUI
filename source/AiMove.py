from PyQt5.QtCore import QThread, pyqtSignal
from source import PieceMoveInfo
from time import sleep
from datetime import datetime
from source import AiBrain


class AiMove(QThread):
    moveDetermined = pyqtSignal(PieceMoveInfo.PieceMoveInfo)
    aiSkipDetermined = pyqtSignal()

    def __init__(self, kingInterface, bishopInterface1, bishopInterface2, movesRemaining, color):
        super(AiMove, self).__init__()
        self.overallBestMove = 0
        self.kingAi = 0
        self.bishopAi1 = 0
        self.bishopAi2 = 0
        self.kingMove = 0
        self.bishopMove1 = 0
        self.bishopMove2 = 0
        self.kingAiComplete = False
        self.bishopAi1Complete = False
        self.bishopAi2Complete = False
        self.kingInterface = kingInterface
        self.bishopInterface1 = bishopInterface1
        self.bishopInterface2 = bishopInterface2
        self.movesRemaining = movesRemaining
        self.color = color
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

            self.kingAi = AiBrain.AiBrain(self.kingInterface, self.color, 1)
            self.kingAi.foundBestMove.connect(self.kingAiFinished)
            self.kingAi.noMove.connect(self.kingAiNoMove)
            self.kingAi.start()

            self.bishopAi1 = AiBrain.AiBrain(self.bishopInterface1, self.color, 0)
            self.bishopAi1.foundBestMove.connect(self.bishopAi1Finished)
            self.bishopAi1.noMove.connect(self.bishopAi1NoMove)
            self.bishopAi1.start()

            self.bishopAi2 = AiBrain.AiBrain(self.bishopInterface2, self.color, 2)
            self.bishopAi2.foundBestMove.connect(self.bishopAi2Finished)
            self.bishopAi2.noMove.connect(self.bishopAi2NoMove)
            self.bishopAi2.start()

        while self.isRunning and not (self.kingAiComplete and self.bishopAi1Complete and self.bishopAi2Complete):
            sleep(0.5)

        if self.isRunning:
            elapsedTime = datetime.now() - self.startTime

            if (elapsedTime.seconds + (elapsedTime.microseconds / 1000000)) < 2.000:
                sleep(2 - (elapsedTime.seconds + (elapsedTime.microseconds / 1000000)))

            if not self.kingMove == 0:
                self.overallBestMove = self.kingMove

            if not self.bishopMove1 == 0 and (self.overallBestMove == 0 or self.bishopMove1.getValue() > self.overallBestMove.getValue()):
                self.overallBestMove = self.bishopMove1

            if not self.bishopMove2 == 0 and (self.overallBestMove == 0 or self.bishopMove2.getValue() > self.overallBestMove.getValue()):
                self.overallBestMove = self.bishopMove2

        while self.isRunning and self.kingInterface.getPaused():
            sleep(2)

        if self.isRunning:
            if self.overallBestMove == 0 and len(self.kingInterface.getAllPossibleMoves(self.color)) == 1:
                self.moveDetermined.emit(self.kingInterface.getAllPossibleMoves(self.color)[0])
            elif self.overallBestMove == 0:
                self.aiSkipDetermined.emit()
            else:
                self.moveDetermined.emit(self.overallBestMove)
