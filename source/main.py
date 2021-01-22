import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QGroupBox, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QMouseEvent, QCursor
from PyQt5.QtCore import Qt


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
        self.pieceSet = [["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                         ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                         ["0", "0", "0", "0", "0", "0", "0", "0"],
                         ["0", "0", "0", "0", "0", "0", "0", "0"],
                         ["0", "0", "0", "0", "0", "0", "0", "0"],
                         ["0", "0", "0", "0", "0", "0", "0", "0"],
                         ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                         ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"]]

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
                        label = pawn(self)
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


class pawn(QLabel):
    previousPos = QPoint()
    isDraggable = False

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        # If the person left clicks, set object as draggable and store position.
        if ev.button() == Qt.LeftButton:
            self.isDraggable = True
            self.previousPos = ev.globalPos()

    def mouseMoveEvent(self, ev: QMouseEvent) -> None:
        # If the object is draggable, use the current and previous global positions
        # to create an offset (the object jitters without this). Set the new position
        # using the current position and the offset. Finally, reset the old position.
        if self.isDraggable:
            offset = QPoint(ev.globalPos() - self.previousPos)
            self.move(self.x() + offset.x(), self.y() + offset.y())
            self.previousPos = ev.globalPos()

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        self.isDraggable = False
        

def chessBoard():
    app = QApplication(sys.argv)
    window = chessBoardWindow()

    window.show()
    sys.exit(app.exec_())


def main():
    chessBoard()


if __name__ == '__main__':
    main()
