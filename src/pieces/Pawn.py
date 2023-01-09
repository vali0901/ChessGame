from pieces.Piece import *

class Pawn(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, PieceType.PAWN)

    def setAvailablePositions(self, aPos, pPos):
        for i in range(0, 8):
            for j in range(0, 8):
                aPos[i][j] = 0

        currX = self.x
        currY = self.y

        match self.color:
            case Color.LIGHT:
                if pPos[currX - 1][currY] is None:
                    aPos[currX - 1][currY] = 1

                if currX == 6 and pPos[currX - 2][currY] is None and pPos[currX - 1][currY] is None:
                    aPos[currX - 2][currY] = 1

                if currY - 1 >= 0:
                    aPos[currX - 1][currY - 1] = -1

                if currY - 1 >= 0 \
                        and pPos[currX - 1][currY - 1] is not None \
                        and pPos[currX - 1][currY - 1].getColor() != self.getColor():
                    aPos[currX - 1][currY - 1] = 2
                    if pPos[currX - 1][currY - 1].getType() == PieceType.KING:
                        aPos[self.x][self.y] = 5

                if currY - 1 >= 0 \
                        and pPos[currX - 1][currY - 1] is not None \
                        and pPos[currX - 1][currY - 1].getColor() == self.getColor():
                    aPos[currX - 1][currY - 1] = 3

                if currY + 1 < 8:
                    aPos[currX - 1][currY + 1] = -1

                if currY + 1 < 8 \
                        and pPos[currX - 1][currY + 1] is not None \
                        and pPos[currX - 1][currY + 1].getColor() != self.getColor():
                    aPos[currX - 1][currY + 1] = 2
                    if pPos[currX - 1][currY + 1].getType() == PieceType.KING:
                        aPos[self.x][self.y] = 5

                if currY + 1 < 8 \
                        and pPos[currX - 1][currY + 1] is not None \
                        and pPos[currX - 1][currY + 1].getColor() == self.getColor():
                    aPos[currX - 1][currY + 1] = 3

            case Color.DARK:

                if pPos[currX + 1][currY] is None:
                    aPos[currX + 1][currY] = 1

                if currX == 1 and pPos[currX + 2][currY] is None and pPos[currX + 1][currY] is None:
                    aPos[currX + 2][currY] = 1

                if currY - 1 >= 0:
                    aPos[currX + 1][currY - 1] = -1

                if currY - 1 >= 0 and pPos[currX + 1][currY - 1] is not None \
                        and pPos[currX + 1][currY - 1].getColor() != self.getColor():
                    aPos[currX + 1][currY - 1] = 2
                    if pPos[currX + 1][currY - 1].getType() == PieceType.KING:
                        aPos[self.x][self.y] = 5

                if currY - 1 >= 0 and pPos[currX + 1][currY - 1] is not None \
                        and pPos[currX + 1][currY - 1].getColor() == self.getColor():
                    aPos[currX + 1][currY - 1] = 3

                if currY + 1 < 8:
                    aPos[currX + 1][currY + 1] = -1

                if currY + 1 < 8 and pPos[currX + 1][currY + 1] is not None \
                        and pPos[currX + 1][currY + 1].getColor() != self.getColor():
                    aPos[currX + 1][currY + 1] = 2
                    if pPos[currX + 1][currY + 1].getType() == PieceType.KING:
                        aPos[self.x][self.y] = 5

                if currY + 1 < 8 and pPos[currX + 1][currY + 1] is not None \
                        and pPos[currX + 1][currY + 1].getColor() == self.getColor():
                    aPos[currX + 1][currY + 1] = 3
