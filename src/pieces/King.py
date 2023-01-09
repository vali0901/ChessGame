from pieces.Piece import *


class King(Piece):
    hasMoved = None
    def __init__(self, x, y, color):
        super().__init__(x, y, color, PieceType.KING)
        self.hasMoved = 0

    def setAvailablePositions(self, aPos, pPos):
        for i in range(0, 8):
            for j in range(0, 8):
                aPos[i][j] = 0

        currX = self.x
        currY = self.y

        for i in range(currX - 1, currX + 2):
            for j in range(currY - 1, currY + 2):
                if i < 0 or j < 0 or i > 7 or j > 7:
                    continue
                if i == currX and j == currY:
                    continue

                if pPos[i][j] is None:
                    aPos[i][j] = 1
                else:
                    if pPos[i][j].getColor() != self.getColor():
                        aPos[i][j] = 2
                    else:
                        aPos[i][j] = 3

        if self.hasMoved == 1:
            return

        right = 1
        left = 1
        if pPos[currX][7] is None or pPos[currX][7].getType() != PieceType.ROOK \
                or pPos[currX][7].getMove() != 0:
            right = 0

        if pPos[currX][0] is None or pPos[currX][0].getType() != PieceType.ROOK \
                or pPos[currX][0].getMove() != 0:
            left = 0

        for i in range(currY + 1, 7):
            if pPos[currX][i] is not None:
                right = 0
                break

        for i in range(1, currY - 1):
            if pPos[currX][i] is not None:
                left = 0
                break

        if right == 1:
            aPos[currX][currY + 2] = 7

        if left == 1:
            aPos[currX][currY - 2] = 7

    def getMove(self):
        return self.hasMoved
    def pieceMove(self):
        self.hasMoved = 1
