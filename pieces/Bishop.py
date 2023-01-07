from pieces.Piece import *


class Bishop(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, PieceType.BISHOP)

    def setAvailablePositions(self, aPos, pPos):
        for i in range(0, 8):
            for j in range(0, 8):
                aPos[i][j] = 0

        currX = self.x
        currY = self.y

        for rowOrder in range(-1, 2):
            for columnOrder in range(-1, 2):
                if rowOrder == 0 or columnOrder == 0:
                    continue

                i = currX + rowOrder
                j = currY + columnOrder

                while True:
                    if i < 0 or i > 7 or j < 0 or j > 7:
                        break

                    if pPos[i][j] is None:
                        aPos[i][j] = 1
                    else:
                        if pPos[i][j].getColor() != self.color:
                            aPos[i][j] = 2
                            if pPos[i][j].getType() == PieceType.KING:
                                # mark it as direct attacker of the king
                                aPos[self.x][self.y] = 5
                                break

                            k = i + rowOrder
                            l = j + columnOrder

                            while True:
                                if k < 0 or k > 7 or l < 0 or l > 7:
                                    break

                                if pPos[k][l] is not None and pPos[k][l].getColor() == self.color:
                                    break

                                if pPos[k][l] is not None and pPos[k][l].getColor() != self.color \
                                        and pPos[k][l].getType() == PieceType.KING:
                                    aPos[i][j] = 4
                                    break

                                k += rowOrder
                                l += columnOrder

                        else:
                            if pPos[i][j] != self:
                                aPos[i][j] = 3
                        break

                    i += rowOrder
                    j += columnOrder
