import copy
from source import BoardInterface
from PyQt5.QtCore import QThread, pyqtSignal
from source import PieceMoveInfo
from time import sleep


class AiMove(QThread):
    moveDetermined = pyqtSignal(PieceMoveInfo.PieceMoveInfo)
    aiSkipDetermined = pyqtSignal()

    def __init__(self, threadBoardInput):
        super(AiMove, self).__init__()
        self.MIN = -10 ** 6
        self.MAX = 10 ** 6
        self.MAXDEPTH = 1
        self.threadBoardInput = threadBoardInput

    def run(self):
        self.nextMove(self.threadBoardInput)

    #def getCopy(self, currentBoard):
        # TODO get copy of currentBoard
    #    return currentBoard
        #return copy.deepcopy(currentBoard)

    def valuePiece(self, board, yIter, xIter):
        # return the value of pieces
        if board.piecePosCopy[yIter][xIter].pieceType == "knight":
            return 6 + board.piecePosCopy[yIter][xIter].knightSpecial
        elif board.piecePosCopy[yIter][xIter].pieceType == "king":
            return 30
        elif board.piecePosCopy[yIter][xIter].pieceType == "queen":
            return 10
        elif board.piecePosCopy[yIter][xIter].pieceType == "bishop":
            return 6
        elif board.piecePosCopy[yIter][xIter].pieceType == "rook":
            return 8
        else:
            return 1

    def eval(self, board, yIter, xIter):
        # return the value of piece and the position
        val = self.valuePiece(board, yIter, xIter)
        res = 1
        # is position of an attack
        #if yIter // 4 != board.piecePosCopy[yIter][xIter].pieceColor:
        #    res += 1

        if board.getTurn() == 0:
            if yIter <= 3:
                res += 1
        else:
            if yIter >= 4:
                res += 1

        # is center
        if 2 <= xIter < 6:
            res += 1
        return res * val

    def evaluate(self, board):
        score = 0

        xIter = 0
        yIter = 0
        for row in board.piecePosCopy:
            for tile in row:
                # If the tile has a piece...
                if not board.piecePosCopy[yIter][xIter] == "0":
                    val = 0
                    val += board.getMovesRemaining()[board.piecePosCopy[yIter][xIter].pieceCommander]
                    val += self.eval(board, yIter, xIter)
                    if not board.piecePosCopy[yIter][xIter].pieceColor == board.getTurn():
                        val *= -1
                    score += val
                xIter += 1
            xIter = 0
            yIter += 1

        return score

    def minimax(self, currentBoard, alpha, beta, depth):
        # test is game over
        gameOver = currentBoard.isGameOver()
        if (gameOver > 0):
            if (gameOver == 1):
                return self.MAX
            elif gameOver == 2:
                return self.MIN
            return 0

        if depth == self.MAXDEPTH:
            return self.evaluate(currentBoard)

        best = 0
        if currentBoard.getTurn() == 1:
            best = self.MIN
        else:
            best = self.MAX

        for move in currentBoard.getAllPossibleMoves():
            copyOfBoard = BoardInterface.BoardInterface(currentBoard.mainBoard)
            copyOfBoard.updatePiecePosCopy(currentBoard.piecePosCopy)
            copyOfBoard.makeMove(move)

            val = self.minimax(copyOfBoard, alpha, beta, depth + 1)

            if currentBoard.getTurn() == 1:
                best = max(best, val)
                alpha = max(best, alpha)
            else:
                best = min(best, val)
                beta = min(best, beta)

            if beta <= alpha:
                break

        return best

    def nextMove(self, currentBoard):
        print("Ai Trigger")
        best = self.MIN
        alpha = self.MIN
        beta = self.MAX
        bestmove = 0
        for move in currentBoard.getAllPossibleMoves():
            copyOfBoard = BoardInterface.BoardInterface(currentBoard.mainBoard)
            copyOfBoard.updatePiecePosCopy(currentBoard.piecePosCopy)
            copyOfBoard.makeMove(move)

            val = self.minimax(copyOfBoard, alpha, beta, 0)

            if (val > best):
                bestmove = move
            best = max(best, val)
            alpha = max(best, alpha)
            if beta <= alpha:
                break

        sleep(2)

        while currentBoard.getPaused():
            sleep(2)

        if bestmove == 0 and len(currentBoard.getAllPossibleMoves()) == 1:
            self.moveDetermined.emit(currentBoard.getAllPossibleMoves()[0])
        elif bestmove == 0:
            self.aiSkipDetermined.emit()
        else:
            self.moveDetermined.emit(bestmove)

