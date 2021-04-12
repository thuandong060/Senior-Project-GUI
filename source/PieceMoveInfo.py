class PieceMoveInfo:
    def __init__(self, fromPos, toPos):
        super(PieceMoveInfo, self).__init__()

        self.fromPos = fromPos
        self.toPos = toPos
        self.value = 0

    # Returns the position the piece was moved from.
    def getFromPos(self):
        return self.fromPos

    # Returns the position the piece was moved to.
    def getToPos(self):
        return self.toPos

    # Set the value of a move.
    def setValue(self, value):
        self.value = value

    # Get the Value of a move.
    def getValue(self):
        return self.value
