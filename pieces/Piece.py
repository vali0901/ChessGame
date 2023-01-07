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
