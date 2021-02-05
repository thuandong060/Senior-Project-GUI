from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import Qt, QPoint
from ChessRule import Rule


class piece(QLabel):
    def __init__(self, pieceColor, pieceType, pieceCommander, parent=None):
        super(piece, self).__init__(parent)

        # Set up some properties
        self.labelPos = QPoint()
        self.isDraggable = False
        self.isOnBoarder = False
        self.startingPosition = [0, 0]
        self.endingPosition = [0, 0]
        self.pieceColor = pieceColor
        self.knightSpecial = False
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
        # (self.parent().playerTurnsRemaining[self.pieceCommander] == 1 or
        # (self.parent().playerTurnsRemaining[self.pieceCommander] == 2 and self.pieceType == "knight"))

        if self.parent().turn == self.pieceColor and not self.parent().gameOver:
            # If the person left clicks, set object as draggable and store position.
            if ev.button() == Qt.LeftButton:
                self.isDraggable = True
                self.labelPos = ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30))
                self.startingPosition = [int(self.labelPos.x() / self.parent().tileSize),
                                         int(self.labelPos.y() / self.parent().tileSize)]
                self.raise_()

    def mouseMoveEvent(self, ev: QMouseEvent) -> None:
        # Make sure it is the right turn for the piece and that the commander has command points.
        if self.parent().turn == self.pieceColor and not self.parent().gameOver:
            # If the object is draggable, use the current global position and the position of the parent window to
            # determine where the label should be displayed
            if self.isDraggable:
                if ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30)).x() < (0 + (self.parent().tileSize / 2)) \
                        and ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30)).y() < \
                        (0 + (self.parent().tileSize / 2)):
                    self.labelPos = QPoint(0 + (self.parent().tileSize / 2),
                                           0 + (self.parent().tileSize / 2))
                    self.isOnBoarder = True
                elif ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30)).y() < (0 + (self.parent().tileSize / 2)) \
                        and ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30)).x() > \
                        (self.parent().tileSize * 8 - (self.parent().tileSize / 2)):
                    self.labelPos = QPoint(self.parent().tileSize * 8 - (self.parent().tileSize / 2),
                                           0 + (self.parent().tileSize / 2))
                    self.isOnBoarder = True
                elif ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30)).x() > \
                        (self.parent().tileSize * 8 - (self.parent().tileSize / 2)) and \
                        ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30)).y() > \
                        (self.parent().tileSize * 8 - (self.parent().tileSize / 2)):
                    self.labelPos = QPoint(self.parent().tileSize * 8 - (self.parent().tileSize / 2),
                                           self.parent().tileSize * 8 - (self.parent().tileSize / 2))
                    self.isOnBoarder = True
                elif ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30)).x() < (0 + (self.parent().tileSize / 2)) \
                        and ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30)).y() > \
                        (self.parent().tileSize * 8 - (self.parent().tileSize / 2)):
                    self.labelPos = QPoint(0 + (self.parent().tileSize / 2),
                                           self.parent().tileSize * 8 - (self.parent().tileSize / 2))
                    self.isOnBoarder = True
                elif ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30)).x() < (0 + (self.parent().tileSize / 2)):
                    self.labelPos = QPoint(0 + (self.parent().tileSize / 2),
                                           (ev.globalPos().y() - self.parent().pos().y()) - 30)
                    self.isOnBoarder = True
                elif ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30)).y() < (0 + (self.parent().tileSize / 2)):
                    self.labelPos = QPoint((ev.globalPos().x() - self.parent().pos().x()) - 0,
                                           0 + (self.parent().tileSize / 2))
                    self.isOnBoarder = True
                elif ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30)).x() > \
                        (self.parent().tileSize * 8 - (self.parent().tileSize / 2)):
                    self.labelPos = QPoint(self.parent().tileSize * 8 - (self.parent().tileSize / 2),
                                           (ev.globalPos().y() - self.parent().pos().y()) - 30)
                    self.isOnBoarder = True
                elif ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30)).y() > \
                        (self.parent().tileSize * 8 - (self.parent().tileSize / 2)):
                    self.labelPos = QPoint((ev.globalPos().x() - self.parent().pos().x()) - 0,
                                           (self.parent().tileSize * 8 - (self.parent().tileSize / 2)))
                    self.isOnBoarder = True
                if not self.isOnBoarder:
                    self.labelPos = ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30))
                self.move(self.labelPos - QPoint(self.parent().tileSize / 2, (self.parent().tileSize / 2)))
                self.isOnBoarder = False


    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        # Make sure it is the right turn for the piece and that the commander has command points.
        if self.parent().turn == self.pieceColor and not self.parent().gameOver:
            # Reset properties and pass things to the board object to handle the movement.
            self.isDraggable = False
            self.isOnBoarder = False
            self.endingPosition = [int(self.labelPos.x() / self.parent().tileSize),
                                   int(self.labelPos.y() / self.parent().tileSize)]

            # self.rules.isPathFree(self, self.startingPosition, self.endingPosition, self.pieceColor, self.parent().piecePos)

            self.parent().movePiece(self.startingPosition, self.endingPosition, self.pieceCommander, self.rules)
