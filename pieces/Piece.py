from enum import Enum


class PieceType(Enum):
    PAWN = 1
    KING = 2
    QUEEN = 3
    BISHOP = 4
    KNIGHT = 5
    ROOK = 6


class Color(Enum):
    LIGHT = 1
    DARK = 2


class Piece:
    x = -1
    y = -1
    selected = -1
    pieceType = None
    color = None

    def __init__(self, x, y, color, pieceType):
        self.selected = 0
        self.x = x
        self.y = y
        self.color = color
        self.pieceType = pieceType

    def isSelected(self):
        return self.selected

    def Select(self):
        self.selected = 1

    def Unselect(self):
        self.selected = 0

    def getType(self):
        return self.pieceType

    def getColor(self):
        return self.color

    def getCoords(self):
        return self.x, self.y

    def setCoords(self, coords):
        self.x = coords[0]
        self.y = coords[1]

    # method used for coloring the buttons when a piece is selected
    # aPos -> available positions where this piece can be moved
    # pPos -> current positions of all the pieces on the table
    def setAvailablePositions(self, aPos, pPos):
        for i in range(0, 8):
            for j in range(0, 8):
                aPos[i][j] = 0

    # # returns a matrix containing the direction ths piece can go,
    # # regardless of the other existing pieces
    # def getGeneralDirection(self):
    #     return None



class Pawn(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, PieceType.PAWN)

    def setAvailablePositions(self, aPos, pPos):
        # init with 0 the whole matrix
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

                if currY - 1 >= 0 and pPos[currX + 1][currY - 1] is not None\
                        and pPos[currX + 1][currY - 1].getColor() != self.getColor():

                    aPos[currX + 1][currY - 1] = 2

                if currY - 1 >= 0 and pPos[currX + 1][currY - 1] is not None\
                        and pPos[currX + 1][currY - 1].getColor() == self.getColor():

                    aPos[currX + 1][currY - 1] = 3

                if currY + 1 < 8:
                    aPos[currX + 1][currY + 1] = -1

                if currY + 1 < 8 and pPos[currX + 1][currY + 1] is not None \
                        and pPos[currX + 1][currY + 1].getColor() != self.getColor():
                    aPos[currX + 1][currY + 1] = 2

                if currY + 1 < 8 and pPos[currX + 1][currY + 1] is not None \
                        and pPos[currX + 1][currY + 1].getColor() == self.getColor():
                    aPos[currX + 1][currY + 1] = 3


class King(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, PieceType.KING)

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

                # check if the other king is near to this position
                # otherKingNear = 0
                # for k in range(i - 1, i + 2):
                #     for l in range(j - 1, j + 2):
                #         if k < 0 or l < 0 or k > 7 or l > 7 or pPos[k][l] == self:
                #             continue
                #         if pPos[k][l] is not None and pPos[k][l].getType == PieceType.KING:
                #             otherKingNear = 1
                #
                # if otherKingNear == 1:
                #     continue

                if pPos[i][j] is None:
                    aPos[i][j] = 1
                else:
                    # needs another check that verifies if the king will be in check in this position
                    if pPos[i][j].getColor() != self.getColor():
                        aPos[i][j] = 2
                    else:
                        aPos[i][j] = 3


class Queen(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, PieceType.QUEEN)

    def setAvailablePositions(self, aPos, pPos):
        for i in range(0, 8):
            for j in range(0, 8):
                aPos[i][j] = 0

        currX = self.x
        currY = self.y

        # check the horizontal line
        for j in range(currY - 1, -1, -1):
            if j < 0:
                continue

            if pPos[currX][j] is None:
                aPos[currX][j] = 1
            else:
                if pPos[currX][j].getColor() != self.color:
                    aPos[currX][j] = 2
                else:
                    aPos[currX][j] = 3
                break

        for j in range(currY + 1, 8):
            if j > 7:
                continue
            if pPos[currX][j] is None:
                aPos[currX][j] = 1
            else:
                if pPos[currX][j].getColor() != self.color:
                    aPos[currX][j] = 2
                else:
                    aPos[currX][j] = 3
                break

        # check the vertical line
        for i in range(currX - 1, -1, -1):
            if i < 0:
                continue
            if pPos[i][currY] is None:
                aPos[i][currY] = 1
            else:
                if pPos[i][currY].getColor() != self.color:
                    aPos[i][currY] = 2
                else:
                    aPos[i][currY] = 3
                break

        for i in range(currX + 1, 8):
            if i > 7:
                continue

            if pPos[i][currY] is None:
                aPos[i][currY] = 1
            else:
                if pPos[i][currY].getColor() != self.color:
                    aPos[i][currY] = 2
                else:
                    aPos[i][currY] = 3
                break

        # check diagonal lines
        d1 = d2 = d3 = d4 = 0
        for k in range(1, 8):
            if d1 == 0 and currX + k < 8 and currY + k < 8:
                if pPos[currX + k][currY + k] is None:
                    aPos[currX + k][currY + k] = 1
                else:
                    if pPos[currX + k][currY + k].getColor() != self.color:
                        aPos[currX + k][currY + k] = 2
                    else:
                        aPos[currX + k][currY + k] = 3
                    d1 = 1
            else:
                d1 = 1

            if d2 == 0 and currX - k >= 0 and currY + k < 8:
                if pPos[currX - k][currY + k] is None:
                    aPos[currX - k][currY + k] = 1
                else:
                    if pPos[currX - k][currY + k].getColor() != self.color:
                        aPos[currX - k][currY + k] = 2
                    else:
                        aPos[currX - k][currY + k] = 3
                    d2 = 1
            else:
                d2 = 1

            if d3 == 0 and currX + k < 8 and currY - k >= 0:
                if pPos[currX + k][currY - k] is None:
                    aPos[currX + k][currY - k] = 1
                else:
                    if pPos[currX + k][currY - k].getColor() != self.color:
                        aPos[currX + k][currY - k] = 2
                    else:
                        aPos[currX + k][currY - k] = 3
                    d3 = 1
            else:
                d3 = 1

            if d4 == 0 and currX - k >= 0 and currY - k >= 0:
                if pPos[currX - k][currY - k] is None:
                    aPos[currX - k][currY - k] = 1
                else:
                    if pPos[currX - k][currY - k].getColor() != self.color:
                        aPos[currX - k][currY - k] = 2
                    else:
                        aPos[currX - k][currY - k] = 3
                    d4 = 1
            else:
                d4 = 1


class Bishop(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, PieceType.BISHOP)

    def setAvailablePositions(self, aPos, pPos):
        for i in range(0, 8):
            for j in range(0, 8):
                aPos[i][j] = 0

        currX = self.x
        currY = self.y

        # check diagonal lines
        d1 = d2 = d3 = d4 = 0
        for k in range(1, 8):
            if d1 == 0 and currX + k < 8 and currY + k < 8:
                if pPos[currX + k][currY + k] is None:
                    aPos[currX + k][currY + k] = 1
                else:
                    if pPos[currX + k][currY + k].getColor() != self.color:
                        aPos[currX + k][currY + k] = 2
                    else:
                        aPos[currX + k][currY + k] = 3
                    d1 = 1
            else:
                d1 = 1

            if d2 == 0 and currX - k >= 0 and currY + k < 8:
                if pPos[currX - k][currY + k] is None:
                    aPos[currX - k][currY + k] = 1
                else:
                    if pPos[currX - k][currY + k].getColor() != self.color:
                        aPos[currX - k][currY + k] = 2
                    else:
                        aPos[currX - k][currY + k] = 3
                    d2 = 1
            else:
                d2 = 1

            if d3 == 0 and currX + k < 8 and currY - k >= 0:
                if pPos[currX + k][currY - k] is None:
                    aPos[currX + k][currY - k] = 1
                else:
                    if pPos[currX + k][currY - k].getColor() != self.color:
                        aPos[currX + k][currY - k] = 2
                    else:
                        aPos[currX + k][currY - k] = 3
                    d3 = 1
            else:
                d3 = 1

            if d4 == 0 and currX - k >= 0 and currY - k >= 0:
                if pPos[currX - k][currY - k] is None:
                    aPos[currX - k][currY - k] = 1
                else:
                    if pPos[currX - k][currY - k].getColor() != self.color:
                        aPos[currX - k][currY - k] = 2
                    else:
                        aPos[currX - k][currY - k] = 3
                    d4 = 1
            else:
                d4 = 1


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
                    else:
                        aPos[currX + i][currY + j] = 3


class Rook(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, PieceType.ROOK)

    def setAvailablePositions(self, aPos, pPos):
        for i in range(0, 8):
            for j in range(0, 8):
                aPos[i][j] = 0

        currX = self.x
        currY = self.y

        # check the horizontal line
        for j in range(currY - 1, -1, -1):
            if j < 0:
                continue

            if pPos[currX][j] is None:
                aPos[currX][j] = 1
            else:
                if pPos[currX][j].getColor() != self.color:
                    aPos[currX][j] = 2
                else:
                    aPos[currX][j] = 3
                break

        for j in range(currY + 1, 8):
            if j > 7:
                continue
            if pPos[currX][j] is None:
                aPos[currX][j] = 1
            else:
                if pPos[currX][j].getColor() != self.color:
                    aPos[currX][j] = 2
                else:
                    aPos[currX][j] = 3
                break

        # check the vertical line
        for i in range(currX - 1, -1, -1):
            if i < 0:
                continue
            if pPos[i][currY] is None:
                aPos[i][currY] = 1
            else:
                if pPos[i][currY].getColor() != self.color:
                    aPos[i][currY] = 2
                else:
                    aPos[i][currY] = 3
                break

        for i in range(currX + 1, 8):
            if i > 7:
                continue

            if pPos[i][currY] is None:
                aPos[i][currY] = 1
            else:
                if pPos[i][currY].getColor() != self.color:
                    aPos[i][currY] = 2
                else:
                    aPos[i][currY] = 3
                break
