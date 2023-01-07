from pieces.Piece import *


class King(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, PieceType.KING)

    def setAvailablePositions(self, aPos, pPos):
        for i in range(0, 8):
            for j in range(0, 8):
                aPos[i][j] = 0

        currX = self.x
        currY = self.y

        # might not be complete
        for i in range(currX - 1, currX + 2):
            for j in range(currY - 1, currY + 2):
                if i < 0 or j < 0 or i > 7 or j > 7:
                    continue

                if pPos[i][j] is None:
                    aPos[i][j] = 1
                else:
                    if pPos[i][j].getColor() != self.getColor():
                        aPos[i][j] = 2
                    else:
                        aPos[i][j] = 3
