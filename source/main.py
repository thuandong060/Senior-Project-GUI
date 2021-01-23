import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QGroupBox, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QMouseEvent, QCursor
from PyQt5.QtCore import Qt, QPoint


class chessBoardWindow(QMainWindow):
    def __init__(self):
        super(chessBoardWindow, self).__init__()
        # This block sets up the window properties.
        self.setGeometry(400, 200, 300, 300)
        self.setWindowTitle('Chessboard')

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

    # Initialize the board.
    def showBoard(self):
        self.setBoard()

        self.resize(self.tilePos[0][0].width() * 8, self.tilePos[0][0].height() * 8)

    def setBoard(self):
        self.addBoardComponents(self.tileSet, self.tilePos)
        self.addBoardComponents(self.pieceSet, self.piecePos)

    def addBoardComponents(self, sender, destination):
        xiter = 0
        yiter = 0

        # Iterate through all tiles in the tile set array and create images for them.
        # The images are stored in another array that can be manipulated.
        for row in sender:
            for tile in row:
                if not tile == "0":
                    if tile == "wp" or tile == "bp":
                        label = pawn(parent=self)
                    elif tile == "wr" or tile == "br":
                        label = pawn(parent=self)
                    elif tile == "wk" or tile == "bk":
                        label = pawn(parent=self)
                    elif tile == "wb" or tile == "bb":
                        label = pawn(parent=self)
                    elif tile == "wq" or tile == "bq":
                        label = pawn(parent=self)
                    elif tile == "wki" or tile == "bki":
                        label = pawn(parent=self)
                    else:
                        label = QLabel(self)
                    # Set the image based on the array element.
                    label.resize(75, 75)
                    pixmap = QPixmap('../img/' + tile).scaled(label.width(), label.height())
                    label.setPixmap(pixmap)
                    label.move(xiter * label.width(), yiter * label.height())

                    # Move the new label to the label array.
                    destination[yiter][xiter] = label

                xiter += 1
            xiter = 0
            yiter += 1


# Note: A lot of this can and probably will be moves to another method for reuse!
class pawn(QLabel):
    def __init__(self, parent=None):
        super(pawn, self).__init__(parent)

        self.previousPos = QPoint()
        self.offset = QPoint()
        self.isDraggable = False
        self.isOnBoarder = False
        self.startingPosition = [0, 0]
        self.endingPosition = [0, 0]

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        # If the person left clicks, set object as draggable and store position.
        if ev.button() == Qt.LeftButton:
            self.isDraggable = True
            self.previousPos = ev.globalPos()
            self.offset = QPoint(ev.globalPos() - self.previousPos)
            self.startingPosition = [int((self.x() + self.offset.x()) / self.width()),
                                     int((self.y() + self.offset.y()) / self.height())]
            self.raise_()

    def mouseMoveEvent(self, ev: QMouseEvent) -> None:
        # If the object is draggable, use the current and previous global positions
        # to create an offset (the object jitters without this). Set the new position
        # using the current position and the offset. Finally, reset the old position.
        if self.isDraggable:
            self.offset = QPoint(ev.globalPos() - self.previousPos)
            if self.x() + self.offset.x() <= 0:
                self.move(0, self.y() + self.offset.y())
                self.isOnBoarder = True
            if self.y() + self.offset.y() <= 0:
                self.move(self.x() + self.offset.x(), 0)
                self.isOnBoarder = True
            if self.x() + self.offset.x() >= self.width() * 7:
                self.move(self.width() * 7, self.y() + self.offset.y())
                self.isOnBoarder = True
            if self.y() + self.offset.y() >= self.height() * 7:
                self.move(self.x() + self.offset.x(), self.height() * 7)
                self.isOnBoarder = True
            if not self.isOnBoarder:
                self.move(self.x() + self.offset.x(), self.y() + self.offset.y())
            self.previousPos = ev.globalPos()
            self.isOnBoarder = False

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        self.isDraggable = False
        self.isOnBoarder = False
        self.offset = QPoint(ev.globalPos() - self.previousPos)
        # Snap the piece to the nearest grid point when the person releases it.
        self.move(round((self.x() + self.offset.x()) / self.width()) * self.width(),
                  round((self.y() + self.offset.y()) / self.height()) * self.height())
        # Move the object through the array to match its movements on the gui.
        self.endingPosition = [round((self.x() + self.offset.x()) / self.width()),
                               round((self.y() + self.offset.y()) / self.height())]
        if not self.startingPosition == self.endingPosition:
            self.parent().piecePos[self.endingPosition[1]][self.endingPosition[0]] = \
                self.parent().piecePos[self.startingPosition[1]][self.startingPosition[0]]
            self.parent().piecePos[self.startingPosition[1]][self.startingPosition[0]] = "0"
            print(self.parent().piecePos)


def chessBoard():
    app = QApplication(sys.argv)
    window = chessBoardWindow()

    window.show()
    sys.exit(app.exec_())


def main():
    chessBoard()


if __name__ == '__main__':
    main()
