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


class Queen(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, PieceType.QUEEN)

    def setAvailablePositions(self, aPos, pPos):
        for i in range(0, 8):
            for j in range(0, 8):
                aPos[i][j] = 0

        currX = self.x
        currY = self.y

        for rowOrder in range(-1, 2):
            for columnOrder in range(-1, 2):

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
                                    break;

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
                                    break;

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


class Rook(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, PieceType.ROOK)

    def setAvailablePositions(self, aPos, pPos):
        for i in range(0, 8):
            for j in range(0, 8):
                aPos[i][j] = 0

        currX = self.x
        currY = self.y

        for rowOrder in range(-1, 2):
            for columnOrder in range(-1, 2):
                if rowOrder != 0 and columnOrder != 0:
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
