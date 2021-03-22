class PieceMoveInfo:
    def __init__(self, fromPos, toPos):
        super(PieceMoveInfo, self).__init__()

        self.fromPos = fromPos
        self.toPos = toPos

    # Returns the position the piece was moved from.
    def getFromPos(self):
        return self.fromPos

    # Returns the position the piece was moved to.
    def getToPos(self):
        return self.toPos
