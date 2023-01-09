from pieces.Piece import *


class Knight(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, PieceType.KNIGHT)

    def setAvailablePositions(self, aPos, pPos):
        for i in range(0, 8):
            for j in range(0, 8):
                aPos[i][j] = 0

        currX = self.x   
        currY = self.y

        for i in range(-2, 3):
            for j in range(-2, 3):

                if i == j or i == -j or i == 0 or j == 0:
                    continue

                if currX + i < 0 or currX + i > 7 or currY + j < 0 or currY + j > 7:
                    continue

                if pPos[currX + i][currY + j] is None:
                    aPos[currX + i][currY + j] = 1
                else:
                    if pPos[currX + i][currY + j].getColor() != self.color:
                        aPos[currX + i][currY + j] = 2
                        if pPos[currX + i][currY + j].getType() == PieceType.KING:
                            aPos[self.x][self.y] = 5
                    else:
                        aPos[currX + i][currY + j] = 3
