from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import Qt, QPoint
from ChessRule import Rule
from math import sqrt
from math import pow


class piece(QLabel):
    def __init__(self, pieceColor, pieceType, pieceCommander, parent=None):
        super(piece, self).__init__(parent)

        # Set up some properties
        self.previousPos = QPoint()
        self.offset = QPoint()
        self.isDraggable = False
        self.isOnBoarder = False
        self.startingPosition = [0, 0]
        self.endingPosition = [0, 0]
        self.pieceColor = pieceColor
        if self.pieceColor == "b":
            self.pieceColor = 1
        else:
            self.pieceColor = 0
        self.pieceType = pieceType
        self.rules = Rule.Pawn
        if self.pieceType == "knight":
            self.rules = Rule.Knight
        elif self.pieceType == "king":
            self.rules = Rule.King
        elif self.pieceType == "queen":
            self.rules = Rule.Queen
        elif self.pieceType == "rook":
            self.rules = Rule.Rook
        elif self.pieceType == "bishop":
            self.rules = Rule.Bishop

        self.pieceCommander = pieceCommander

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        # Change to for AI ->
        # if self.parent().playerTurnsRemaining[self.pieceCommander] == 1 and self.parent().turn == 0 and self.pieceColor == 0:
        # Make sure it is the right turn for the piece and that the commander has command points.
        if self.parent().playerTurnsRemaining[self.pieceCommander] == 1 and self.parent().turn == self.pieceColor:
            # If the person left clicks, set object as draggable and store position.
            if ev.button() == Qt.LeftButton:
                self.isDraggable = True
                self.previousPos = ev.globalPos()
                self.offset = QPoint(ev.globalPos() - self.previousPos)
                self.startingPosition = [int((self.x() + self.offset.x()) / self.parent().tileSize),
                                         int((self.y() + self.offset.y()) / self.parent().tileSize)]
                self.raise_()

    def mouseMoveEvent(self, ev: QMouseEvent) -> None:
        # Make sure it is the right turn for the piece and that the commander has command points.
        if self.parent().playerTurnsRemaining[self.pieceCommander] == 1 and self.parent().turn == self.pieceColor:
            # If the object is draggable, use the current and previous global positions
            # to create an offset (the object jitters without this). Set the new position
            # using the current position and the offset. Finally, reset the old position.
            # This is a temp fix and should be looked at later!!!!!!
            if self.isDraggable:
                self.offset = QPoint(ev.globalPos() - self.previousPos)
                if self.x() + self.offset.x() <= 0:
                    self.move(0, self.y() + self.offset.y())
                    self.isOnBoarder = True
                if self.y() + self.offset.y() <= 0:
                    self.move(self.x() + self.offset.x(), 0)
                    self.isOnBoarder = True
                if self.x() + self.offset.x() >= self.parent().boardSize - self.parent().tileSize:
                    self.move(self.parent().boardSize - self.parent().tileSize, self.y() + self.offset.y())
                    self.isOnBoarder = True
                if self.y() + self.offset.y() >= self.parent().boardSize - self.parent().tileSize:
                    self.move(self.x() + self.offset.x(), self.parent().boardSize - self.parent().tileSize)
                    self.isOnBoarder = True
                if not self.isOnBoarder:
                    self.move(self.x() + self.offset.x(), self.y() + self.offset.y())
                self.previousPos = ev.globalPos()
                self.isOnBoarder = False

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        # Make sure it is the right turn for the piece and that the commander has command points.
        if self.parent().playerTurnsRemaining[self.pieceCommander] == 1 and self.parent().turn == self.pieceColor:
            # Reset properties and pass things to the board object to handle the movement.
            self.isDraggable = False
            self.isOnBoarder = False
            self.offset = QPoint(ev.globalPos() - self.previousPos)
            self.endingPosition = [round((self.x() + self.offset.x()) / self.parent().tileSize),
                                   round((self.y() + self.offset.y()) / self.parent().tileSize)]

            # self.rules.isPathFree(self, self.startingPosition, self.endingPosition, self.pieceColor, self.parent().piecePos)

            self.parent().movePiece(self.startingPosition, self.endingPosition, self.pieceCommander, self.rules)

    @staticmethod
    def distance(start, end):
        value = 0.0
        if start[0] == end[0]:
            value = abs(end[1] - start[1])
        elif start[1] == end[1]:
            value = abs(end[0] - start[0])
        else:
            # Use if doesn't work numpy.linarg(start - end)
            value = sqrt(pow((end[0] - start[0]), 2) + pow((end[1] - start[1]), 2))
        return value
