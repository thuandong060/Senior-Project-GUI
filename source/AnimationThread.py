from time import sleep
from PyQt5.QtCore import QThread, pyqtSignal


class AnimationThread(QThread):
    setupAttackArrow = pyqtSignal(list, list)
    fallAttackArrow = pyqtSignal()
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
            self.setupAttackArrow.emit(self.fromPos, self.toPos)
            iterator = 0

        while self.running:
            self.fallAttackArrow.emit()
            sleep(0.0001)
            if iterator >= 50:
                break
            iterator += 1

        if self.running:
            sleep(2.9)

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
            sleep(2.9)

        if self.running:
            # Clean up
            self.finishAnimation.emit(self.fromPos, self.toPos, self.commander, self.rollNeeded, self.rollGot)
