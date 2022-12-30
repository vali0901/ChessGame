from enum import Enum


class PieceType(Enum):
    PAWN = 1
    KING = 2
    QUEEN = 3
    BISHOP = 4
    KNIGHT = 5
    ROOK = 6


class Piece:
    x = -1
    y = -1
    selected = -1
    pieceType = None

    def __init__(self, x, y, pieceType):
        self.selected = 0
        self.x = x
        self.y = y
        self.pieceType = pieceType

    def isSelected(self):
        return self.selected

    def Select(self):
        self.selected = 1

    def Unselect(self):
        self.selected = 0


class Pawn(Piece):
    def __init__(self, x, y):
        super().__init__(x, y, PieceType.PAWN)


class King(Piece):
    def __init__(self, x, y):
        super().__init__(x, y, PieceType.KING)


class Queen(Piece):
    def __init__(self, x, y):
        super().__init__(x, y, PieceType.QUEEN)


class Bishop(Piece):
    def __init__(self, x, y):
        super().__init__(x, y, PieceType.BISHOP)


class Knight(Piece):
    def __init__(self, x, y):
        super().__init__(x, y, PieceType.KNIGHT)


class Rook(Piece):
    def __init__(self, x, y):
        super().__init__(x, y, PieceType.ROOK)
