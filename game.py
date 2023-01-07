from tkinter import *
from tkinter import messagebox
from numpy import *
from PIL import Image, ImageTk

import sys
import os

from pieces.Bishop import Bishop
from pieces.King import King
from pieces.Knight import Knight
from pieces.Pawn import Pawn
from pieces.Piece import *
from pieces.Queen import Queen
from pieces.Rook import Rook


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class SquareColor(Enum):
    DARK = '#948245'
    LIGHT = '#E6dAB2'
    AVAILABLE = '#FFF5bd'
    ATTACK = '#F74739'


class Game:
    gameWindow = None
    pawnPromotionWin = None
    buttonMatrix = None
    piecesMatrix = None
    selectedPiece = None
    selectedPieceCoords = None

    # selected piece's available positions where it can be moved
    availablePositions = None

    turn = None
    darkKing = None
    lightKing = None

    # the layout for every color
    # contains info about the directions of attack, pieces 'in danger' (when an enemy piece can be attacked),
    # 'protected' pieces (if a piece is staying on the attack direction of a friendly piece),
    # 'last piece standing' (when a piece is staying between an attacker and its king)
    darkAttackLayout = None
    lightAttackLayout = None

    pawnPromotionPieceType = None
    pawnPromotionPieceImgPath = None

    def __init__(self):
        self.gameWindow = Tk()
        self.buttonMatrix = []
        self.piecesMatrix = []
        self.availablePositions = np.zeros((8, 8))
        self.checkingPosition = np.zeros((8, 8))
        self.darkAttackLayout = np.zeros((8, 8))
        self.lightAttackLayout = np.zeros((8, 8))
        self.turn = Color.LIGHT

        self.darkCheck = 0
        self.lightCheck = 0

    def createButtonMatrix(self):
        # creates the button matrix
        for i in range(0, 8):
            helperRow = []
            for j in range(0, 8):
                if (i + j) % 2 == 0:
                    color = SquareColor.LIGHT
                else:
                    color = SquareColor.DARK

                # creates a new button that will do buttonClicked method each time it is pressed
                # m contains this button's arguments
                newButton = Button(self.gameWindow, padx=20, pady=12, bg=color.value,
                                   command=lambda coords=(i, j): self.buttonClicked(coords))
                newButton.grid(row=i, column=j)
                helperRow.append(newButton)
                newButton.update()

            self.buttonMatrix.append(helperRow)

    def createPiecesMatrix(self):
        # creates the pieces matrix (as it is at the beginning of the game)
        lightPawnRow = []
        darkPawnRow = []
        lightBackRow = []
        darkBackRow = []

        for i in range(0, 8):
            lightPawnRow.append(Pawn(6, i, Color.LIGHT))
            darkPawnRow.append(Pawn(1, i, Color.DARK))
            match i:
                case 0:
                    lightBackRow.append(Rook(7, i, Color.LIGHT))
                    darkBackRow.append(Rook(0, i, Color.DARK))
                case 1:
                    lightBackRow.append(Knight(7, i, Color.LIGHT))
                    darkBackRow.append(Knight(0, i, Color.DARK))
                case 2:
                    lightBackRow.append(Bishop(7, i, Color.LIGHT))
                    darkBackRow.append(Bishop(0, i, Color.DARK))
                case 3:
                    lightBackRow.append(Queen(7, i, Color.LIGHT))
                    darkBackRow.append(Queen(0, i, Color.DARK))
                case 4:
                    self.lightKing = King(7, i, Color.LIGHT)
                    lightBackRow.append(self.lightKing)
                    self.darkKing = King(0, i, Color.DARK)
                    darkBackRow.append(self.darkKing)
                case 5:
                    lightBackRow.append(Bishop(7, i, Color.LIGHT))
                    darkBackRow.append(Bishop(0, i, Color.DARK))
                case 6:
                    lightBackRow.append(Knight(7, i, Color.LIGHT))
                    darkBackRow.append(Knight(0, i, Color.DARK))
                case 7:
                    lightBackRow.append(Rook(7, i, Color.LIGHT))
                    darkBackRow.append(Rook(0, i, Color.DARK))

            for i in range(0, 8):
                match i:
                    case 0:
                        self.piecesMatrix.append(darkBackRow)
                    case 1:
                        self.piecesMatrix.append(darkPawnRow)
                    case 6:
                        self.piecesMatrix.append(lightPawnRow)
                    case 7:
                        self.piecesMatrix.append(lightBackRow)
                    case _:
                        emptyRow = [None] * 8
                        self.piecesMatrix.append(emptyRow)

    def startGame(self):
        self.createButtonMatrix()
        self.createPiecesMatrix()

        # adding images to buttons

        # adding Pawns
        lightP = Image.open(resource_path("img/Chess_plt60.png"))
        helper1 = lightP.resize((self.buttonMatrix[0][0].winfo_width() - 5, self.buttonMatrix[0][0].winfo_height() - 5))
        helper = ImageTk.PhotoImage(helper1)
        lightP = helper

        darkP = Image.open(resource_path("img/Chess_pdt60.png"))
        helper1 = darkP.resize((self.buttonMatrix[0][0].winfo_width() - 5, self.buttonMatrix[0][0].winfo_height() - 5))
        helper = ImageTk.PhotoImage(helper1)
        darkP = helper

        for i in range(0, 8):
            self.buttonMatrix[1][i].configure(image=darkP)
            self.buttonMatrix[6][i].configure(image=lightP)

        # adding the other pieces

        # King
        darkK = Image.open(resource_path("img/Chess_kdt60.png"))
        helper1 = darkK.resize((self.buttonMatrix[0][0].winfo_width() - 5, self.buttonMatrix[0][0].winfo_height() - 5))
        helper = ImageTk.PhotoImage(helper1)
        darkK = helper

        lightK = Image.open(resource_path("img/Chess_klt60.png"))
        helper1 = lightK.resize((self.buttonMatrix[0][0].winfo_width() - 5, self.buttonMatrix[0][0].winfo_height() - 5))
        helper = ImageTk.PhotoImage(helper1)
        lightK = helper

        self.buttonMatrix[0][4].configure(image=darkK)
        self.buttonMatrix[7][4].configure(image=lightK)

        # Queen
        darkQ = Image.open(resource_path("img/Chess_qdt60.png"))
        helper1 = darkQ.resize((self.buttonMatrix[0][0].winfo_width() - 5, self.buttonMatrix[0][0].winfo_height() - 5))
        helper = ImageTk.PhotoImage(helper1)
        darkQ = helper

        lightQ = Image.open(resource_path("img/Chess_qlt60.png"))
        helper1 = lightQ.resize((self.buttonMatrix[0][0].winfo_width() - 5, self.buttonMatrix[0][0].winfo_height() - 5))
        helper = ImageTk.PhotoImage(helper1)
        lightQ = helper

        self.buttonMatrix[0][3].configure(image=darkQ)
        self.buttonMatrix[7][3].configure(image=lightQ)

        # Knight
        darkN = Image.open(resource_path("img/Chess_ndt60.png"))
        helper1 = darkN.resize((self.buttonMatrix[0][0].winfo_width() - 5, self.buttonMatrix[0][0].winfo_height() - 5))
        helper = ImageTk.PhotoImage(helper1)
        darkN = helper

        lightN = Image.open(resource_path("img/Chess_nlt60.png"))
        helper1 = lightN.resize((self.buttonMatrix[0][0].winfo_width() - 5, self.buttonMatrix[0][0].winfo_height() - 5))
        helper = ImageTk.PhotoImage(helper1)
        lightN = helper

        self.buttonMatrix[0][1].configure(image=darkN)
        self.buttonMatrix[7][1].configure(image=lightN)
        self.buttonMatrix[0][6].configure(image=darkN)
        self.buttonMatrix[7][6].configure(image=lightN)

        # Bishop
        darkB = Image.open(resource_path("img/Chess_bdt60.png"))
        helper1 = darkB.resize((self.buttonMatrix[0][0].winfo_width() - 5, self.buttonMatrix[0][0].winfo_height() - 5))
        helper = ImageTk.PhotoImage(helper1)
        darkB = helper

        lightB = Image.open(resource_path("img/Chess_blt60.png"))
        helper1 = lightB.resize((self.buttonMatrix[0][0].winfo_width() - 5, self.buttonMatrix[0][0].winfo_height() - 5))
        helper = ImageTk.PhotoImage(helper1)
        lightB = helper

        self.buttonMatrix[0][2].configure(image=darkB)
        self.buttonMatrix[7][5].configure(image=lightB)
        self.buttonMatrix[0][5].configure(image=darkB)
        self.buttonMatrix[7][2].configure(image=lightB)

        # Rook
        darkR = Image.open(resource_path("img/Chess_rdt60.png"))
        helper1 = darkR.resize((self.buttonMatrix[0][0].winfo_width() - 5, self.buttonMatrix[0][0].winfo_height() - 5))
        helper = ImageTk.PhotoImage(helper1)
        darkR = helper

        lightR = Image.open(resource_path("img/Chess_rlt60.png"))
        helper1 = lightR.resize((self.buttonMatrix[0][0].winfo_width() - 5, self.buttonMatrix[0][0].winfo_height() - 5))
        helper = ImageTk.PhotoImage(helper1)
        lightR = helper

        self.buttonMatrix[0][0].configure(image=darkR)
        self.buttonMatrix[7][0].configure(image=lightR)
        self.buttonMatrix[0][7].configure(image=darkR)
        self.buttonMatrix[7][7].configure(image=lightR)

        # Show window
        self.gameWindow.mainloop()

    def buttonClicked(self, coords):
        # SELECTING / UNSELECTING A PIECE

        # pressing on a non-piece button (if it's an unavailable position) or
        # pressing on a piece of different color -> (resets colors)
        if (self.availablePositions[coords[0]][coords[1]] == 0
            and self.piecesMatrix[coords[0]][coords[1]] is None) \
                or (self.piecesMatrix[coords[0]][coords[1]] is not None and
                    self.piecesMatrix[coords[0]][coords[1]].getColor() != self.turn
                    and self.availablePositions[coords[0]][coords[1]] != 2
                    and self.availablePositions[coords[0]][coords[1]] != 4):
            if self.selectedPiece is not None:
                self.selectedPiece = None
            self.resetColors()
            return

        # pressing on a piece of the right color -> select it
        if self.selectedPiece is None \
                or (self.piecesMatrix[coords[0]][coords[1]] is not None and
                    self.piecesMatrix[coords[0]][coords[1]].getColor() == self.turn):
            self.selectedPiece = self.piecesMatrix[coords[0]][coords[1]]
            self.selectedPieceCoords = self.selectedPiece.getCoords()
            self.selectedPiece.setAvailablePositions(self.availablePositions, self.piecesMatrix)

            if self.turn == Color.LIGHT \
                    and (self.darkAttackLayout[coords[0]][coords[1]] == 4
                         or self.lightKingIsChecked()):
                self.specialSetPositions()
                self.updateColors()
                return

            if self.turn == Color.DARK \
                    and (self.lightAttackLayout[coords[0]][coords[1]] == 4
                         or self.darkKingIsChecked()):
                self.specialSetPositions()
                self.updateColors()
                return

            if self.selectedPiece.getType() == PieceType.KING:
                self.setKingPositions()

            self.updateColors()
            return

        # MOVING A PIECE

        # moving a piece to an unavailable spot -> do nothing
        if self.availablePositions[coords[0]][coords[1]] == 0:
            return

        # moving a piece to an available spot -> just move it there
        if self.availablePositions[coords[0]][coords[1]] == 1:
            self.simpleMove(coords)
            self.changeTurn()
            self.resetColors()
            if self.isCheckmate():
                if self.turn == Color.LIGHT:
                    message = "Dark won!"
                else:
                    message = "Light won!"
                messagebox.showinfo("Game ended", message)
                self.gameWindow.destroy()
                exit(0)
            else:
                if self.isDraw():
                    message = "Draw!"
                    messagebox.showinfo("Game ended", message)
                    self.gameWindow.destroy()
                    exit(0)

            return

        # attacking a piece
        if self.availablePositions[coords[0]][coords[1]] == 2 \
                or self.availablePositions[coords[0]][coords[1]] == 4:
            self.attackPiece(coords)
            self.changeTurn()
            self.resetColors()
            if self.isCheckmate():
                if self.turn == Color.LIGHT:
                    message = "Light won!"
                else:
                    message = "Dark won!"
                messagebox.showinfo("Game ended", message)
            else:
                if self.isDraw():
                    message = "Draw!"
                    messagebox.showinfo("Game ended", message)

    def isDraw(self):
        for i in range(0, 8):
            for j in range(0, 8):
                if self.piecesMatrix[i][j] is None:
                    continue
                if self.piecesMatrix[i][j].getType() != PieceType.KING:
                    return False

        return True

    def isCheckmate(self):
        for i in range(0, 8):
            for j in range(0, 8):
                if self.piecesMatrix[i][j] is None:
                    continue
                if self.piecesMatrix[i][j].getColor() != self.turn:
                    continue

                self.piecesMatrix[i][j].setAvailablePositions(self.availablePositions, self.piecesMatrix)
                self.selectedPiece = self.piecesMatrix[i][j]
                self.selectedPieceCoords = self.selectedPiece.getCoords()

                if self.turn == Color.LIGHT \
                        and (self.darkAttackLayout[self.piecesMatrix[i][j].getCoords()[0]][
                                 self.piecesMatrix[i][j].getCoords()[1]] == 4
                             or self.lightKingIsChecked()):
                    self.specialSetPositions()
                else:
                    if self.turn == Color.DARK \
                            and (self.lightAttackLayout[self.piecesMatrix[i][j].getCoords()[0]][
                                     self.piecesMatrix[i][j].getCoords()[1]] == 4
                                 or self.darkKingIsChecked()):
                        self.specialSetPositions()
                    else:
                        if self.piecesMatrix[i][j].getType() == PieceType.KING:
                            self.setKingPositions()

                for k in range(0, 8):
                    for l in range(0, 8):
                        if self.availablePositions[k][l] != 0:
                            self.selectedPiece = None
                            self.selectedPieceCoords = None

                            return False

        self.selectedPiece = None
        self.selectedPieceCoords = None

        return True

    def setKingPositions(self):
        for i in range(0, 8):
            for j in range(0, 8):
                if self.availablePositions[i][j] == 1 or self.availablePositions[i][j] == 2:
                    if self.selectedPiece.getColor() == Color.LIGHT:
                        if self.darkAttackLayout[i][j] == 3 or self.darkAttackLayout[i][j] == 1:
                            self.availablePositions[i][j] = 0
                    else:
                        if self.lightAttackLayout[i][j] == 3 or self.lightAttackLayout[i][j] == 1:
                            self.availablePositions[i][j] = 0

    def specialSetPositions(self):
        match self.turn:
            case Color.LIGHT:
                if self.lightKingIsChecked():
                    if self.selectedPiece.getType() == PieceType.KING:
                        for i in range(0, 8):
                            for j in range(0, 8):
                                if (self.availablePositions[i][j] == 1 and self.darkAttackLayout[i][j] == 1) \
                                        or (self.availablePositions[i][j] == 2 and
                                            (self.darkAttackLayout[i][j] == 3 or self.darkAttackLayout[i][j] == 6)) \
                                        or self.availablePositions[i][j] == 3:
                                    self.availablePositions[i][j] = 0

                        # don't let the king move on the attacking direction

                        # find the attacking piece
                        attackingPiece = None
                        for i in range(0, 8):
                            for j in range(0, 8):
                                if self.darkAttackLayout[i][j] == 5 or self.darkAttackLayout[i][j] == 6:
                                    attackingPiece = self.piecesMatrix[i][j]

                        if attackingPiece.getType() == PieceType.QUEEN \
                                or attackingPiece.getType() == PieceType.ROOK \
                                or attackingPiece.getType() == PieceType.BISHOP:
                            kingX = self.lightKing.getCoords()[0]
                            kingY = self.lightKing.getCoords()[1]
                            attX = attackingPiece.getCoords()[0]
                            attY = attackingPiece.getCoords()[1]

                            rowOrder = -1 if kingX - attX < 0 else (1 if kingX - attX > 0 else 0)
                            columnOrder = -1 if kingY - attY < 0 else (1 if kingY - attY > 0 else 0)
                            if (kingX + rowOrder) in range(0, 8) and (kingY + columnOrder) in range(0, 8):
                                self.availablePositions[kingX + rowOrder][kingY + columnOrder] = 0

                    else:
                        if self.darkAttackLayout[self.selectedPieceCoords[0]][self.selectedPieceCoords[1]] == 4:
                            for i in range(0, 8):
                                for j in range(0, 8):
                                    self.availablePositions[i][j] = 0
                            return

                        # find the attacking piece
                        attackingPiece = None
                        for i in range(0, 8):
                            for j in range(0, 8):
                                if self.darkAttackLayout[i][j] == 5 or self.darkAttackLayout[i][j] == 6:
                                    attackingPiece = self.piecesMatrix[i][j]

                        # init a helper matrix
                        helper = np.zeros((8, 8))

                        match attackingPiece.getType():
                            case PieceType.PAWN | PieceType.KNIGHT:
                                for i in range(0, 8):
                                    for j in range(0, 8):
                                        if i == attackingPiece.getCoords()[0] and j == attackingPiece.getCoords()[1] \
                                                and (self.availablePositions[i][j] == 2
                                                     or self.availablePositions[i][j] == 4):
                                            helper[i][j] = 2
                                        else:
                                            helper[i][j] = 0

                            case PieceType.QUEEN | PieceType.ROOK | PieceType.BISHOP:
                                kingX = self.lightKing.getCoords()[0]
                                kingY = self.lightKing.getCoords()[1]
                                attX = attackingPiece.getCoords()[0]
                                attY = attackingPiece.getCoords()[1]

                                rowOrder = -1 if kingX - attX < 0 else (1 if kingX - attX > 0 else 0)
                                columnOrder = -1 if kingY - attY < 0 else (1 if kingY - attY > 0 else 0)

                                i = attX
                                j = attY

                                while True:
                                    if self.availablePositions[i][j] == 1 \
                                            or self.availablePositions[i][j] == 2 \
                                            or self.availablePositions[i][j] == 4:
                                        helper[i][j] = self.availablePositions[i][j]

                                    i += rowOrder
                                    j += columnOrder

                                    if i == kingX and j == kingY:
                                        break

                        self.availablePositions = helper
                    return

                # "last man standing" -> this piece prevents a check, it can only move to the attacking piece,
                # or on the attacking way
                if self.darkAttackLayout[self.selectedPieceCoords[0]][self.selectedPieceCoords[1]] == 4:
                    # init a helper matrix
                    helper = np.zeros((8, 8))

                    kingX = self.lightKing.getCoords()[0]
                    kingY = self.lightKing.getCoords()[1]
                    selX = self.selectedPieceCoords[0]
                    selY = self.selectedPieceCoords[1]

                    rowOrder = -1 if selX - kingX < 0 else 1 if selX - kingX > 0 else 0
                    columnOrder = -1 if selY - kingY < 0 else 1 if selY - kingY > 0 else 0

                    i = selX + rowOrder
                    j = selY + columnOrder

                    # go towards the attacking piece
                    while True:
                        if i < 0 or i > 7 or j < 0 or j > 7:
                            break

                        helper[i][j] = self.availablePositions[i][j]

                        # break if you find that piece and you can attack it
                        if self.availablePositions[i][j] == 2:
                            break

                        # break if you find the piece and you cannot attack it
                        if self.piecesMatrix[i][j] is not None:
                            break

                        i += rowOrder
                        j += columnOrder

                    self.availablePositions = helper

                return

            case Color.DARK:
                if self.darkKingIsChecked():
                    if self.selectedPiece.getType() == PieceType.KING:
                        for i in range(0, 8):
                            for j in range(0, 8):
                                if (self.availablePositions[i][j] == 1 and self.lightAttackLayout[i][j] == 1) \
                                        or (self.availablePositions[i][j] == 2 and
                                            (self.lightAttackLayout[i][j] == 3 or self.lightAttackLayout[i][j] == 6)) \
                                        or (self.availablePositions[i][j] == 3):
                                    self.availablePositions[i][j] = 0

                        # don't let the king move on the attacking direction

                        # find the attacking piece
                        attackingPiece = None
                        for i in range(0, 8):
                            for j in range(0, 8):
                                if self.lightAttackLayout[i][j] == 5 or self.lightAttackLayout[i][j] == 6:
                                    attackingPiece = self.piecesMatrix[i][j]
                        if attackingPiece.getType() == PieceType.QUEEN \
                                or attackingPiece.getType() == PieceType.ROOK \
                                or attackingPiece.getType() == PieceType.BISHOP:
                            kingX = self.darkKing.getCoords()[0]
                            kingY = self.darkKing.getCoords()[1]
                            attX = attackingPiece.getCoords()[0]
                            attY = attackingPiece.getCoords()[1]

                            rowOrder = -1 if kingX - attX < 0 else (1 if kingX - attX > 0 else 0)
                            columnOrder = -1 if kingY - attY < 0 else (1 if kingY - attY > 0 else 0)
                            if (kingX + rowOrder) in range(0, 8) and (kingY + columnOrder) in range(0, 8):
                                self.availablePositions[kingX + rowOrder][kingY + columnOrder] = 0

                    else:
                        for i in range(0, 8):
                            for j in range(0, 8):
                                if self.lightAttackLayout[self.selectedPieceCoords[0]][
                                    self.selectedPieceCoords[1]] == 4:
                                    for i in range(0, 8):
                                        for j in range(0, 8):
                                            self.availablePositions[i][j] = 0
                                    return
                                # init a helper matrix
                                helper = np.zeros((8, 8))

                                # find the attacking piece
                                attackingPiece = None
                                for i in range(0, 8):
                                    for j in range(0, 8):
                                        if self.lightAttackLayout[i][j] == 5 or self.lightAttackLayout[i][j] == 6:
                                            attackingPiece = self.piecesMatrix[i][j]

                                match attackingPiece.getType():
                                    case PieceType.PAWN | PieceType.KNIGHT:
                                        for i in range(0, 8):
                                            for j in range(0, 8):
                                                if i == attackingPiece.getCoords()[0] \
                                                        and j == attackingPiece.getCoords()[1] \
                                                        and (self.availablePositions[i][j] == 2
                                                             or self.availablePositions[i][j] == 4):
                                                    helper[i][j] = 2
                                                else:
                                                    helper[i][j] = 0

                                    case PieceType.QUEEN | PieceType.BISHOP | PieceType.ROOK:
                                        kingX = self.darkKing.getCoords()[0]
                                        kingY = self.darkKing.getCoords()[1]
                                        attX = attackingPiece.getCoords()[0]
                                        attY = attackingPiece.getCoords()[1]

                                        rowOrder = -1 if kingX - attX < 0 else 1 if kingX - attX > 0 else 0
                                        columnOrder = -1 if kingY - attY < 0 else 1 if kingY - attY > 0 else 0

                                        i = attX
                                        j = attY

                                        while True:
                                            if self.availablePositions[i][j] == 1 \
                                                    or self.availablePositions[i][j] == 2 \
                                                    or self.availablePositions[i][j] == 4:
                                                helper[i][j] = self.availablePositions[i][j]

                                            i += rowOrder
                                            j += columnOrder

                                            if i == kingX and j == kingY:
                                                break

                                self.availablePositions = helper

                    return

                # "last man standing" -> this piece prevents a check, it can only move to the attacking piece,
                # or on the attacking way
                if self.lightAttackLayout[self.selectedPieceCoords[0]][self.selectedPieceCoords[1]] == 4:
                    # init a helper matrix
                    helper = np.zeros((8, 8))
                    # for i in range(0, 8):
                    #     row = []
                    #     for j in range(0, 8):
                    #         row.append(0)
                    #     helper.append(row)

                    kingX = self.darkKing.getCoords()[0]
                    kingY = self.darkKing.getCoords()[1]
                    selX = self.selectedPieceCoords[0]
                    selY = self.selectedPieceCoords[1]

                    rowOrder = -1 if selX - kingX < 0 else 1 if selX - kingX > 0 else 0
                    columnOrder = -1 if selY - kingY < 0 else 1 if selY - kingY > 0 else 0

                    i = selX + rowOrder
                    j = selY + columnOrder

                    # go towards the attacking piece
                    while True:
                        if i < 0 or i > 7 or j < 0 or j > 7:
                            break

                        helper[i][j] = self.availablePositions[i][j]

                        # break if you find that piece and you can attack it
                        if self.availablePositions[i][j] == 2:
                            break

                        # break if you find the piece and you cannot attack it
                        if self.piecesMatrix[i][j] is not None:
                            break

                        i += rowOrder
                        j += columnOrder

                    self.availablePositions = helper

                return
    def createImage(self, imgPath):
        img = Image.open(imgPath)
        helper1 = img.resize(
            (self.buttonMatrix[0][0].winfo_width() - 5, self.buttonMatrix[0][0].winfo_height() - 5))
        helper = ImageTk.PhotoImage(helper1)
        img = helper

        return img

    def simpleMove(self, coords):
        self.piecesMatrix[self.selectedPieceCoords[0]][self.selectedPieceCoords[1]] = None
        self.piecesMatrix[coords[0]][coords[1]] = self.selectedPiece
        self.selectedPiece.setCoords(coords)

        movingPieceImage = self.buttonMatrix[self.selectedPieceCoords[0]][self.selectedPieceCoords[1]].cget('image')
        self.buttonMatrix[self.selectedPieceCoords[0]][self.selectedPieceCoords[1]].configure(image='')
        self.buttonMatrix[coords[0]][coords[1]].configure(image=movingPieceImage)

        if self.selectedPiece.getType() == PieceType.PAWN:
            pawnPromotion = False
            match self.turn:
                case Color.LIGHT:
                    if coords[0] == 0:
                        pawnPromotion = True
                case Color.DARK:
                    if coords[0] == 7:
                        pawnPromotion = True
            if pawnPromotion:
                self.pawnPromotionWin = Toplevel(self.gameWindow)
                self.pawnPromotionWin.title("Change pawn to one of the pieces below")

                qbutt = rbutt = kbutt = bbutt = None
                match self.turn:
                    case Color.LIGHT:
                        # create pieces buttons
                        qbutt = Button(self.pawnPromotionWin, padx=20, pady=12, bg=SquareColor.LIGHT.value,
                                       command=lambda: self.pawnPromotionQueen(coords, 'pyimage6'))
                        img1 = self.createImage(resource_path("img/Chess_qlt60.png"))
                        qbutt.configure(image=img1)

                        rbutt = Button(self.pawnPromotionWin, padx=20, pady=12, bg=SquareColor.DARK.value,
                                       command=lambda: self.pawnPromotionRook(coords, 'pyimage12'))
                        img2 = self.createImage(resource_path("img/Chess_rlt60.png"))
                        rbutt.configure(image=img2)

                        bbutt = Button(self.pawnPromotionWin, padx=20, pady=12, bg=SquareColor.LIGHT.value,
                                       command=lambda: self.pawnPromotionBishop(coords, 'pyimage10'))
                        img3 = self.createImage(resource_path("img/Chess_blt60.png"))
                        bbutt.configure(image=img3)

                        kbutt = Button(self.pawnPromotionWin, padx=20, pady=12, bg=SquareColor.DARK.value,
                                       command=lambda: self.pawnPromotionKnight(coords, 'pyimage8'))
                        img4 = self.createImage(resource_path("img/Chess_nlt60.png"))
                        kbutt.configure(image=img4)

                    case Color.DARK:
                        qbutt = Button(self.pawnPromotionWin, padx=20, pady=12, bg=SquareColor.LIGHT.value,
                                       command=lambda: self.pawnPromotionQueen(coords, 'pyimage5'))
                        img1 = self.createImage(resource_path("img/Chess_qdt60.png"))
                        qbutt.configure(image=img1)

                        rbutt = Button(self.pawnPromotionWin, padx=20, pady=12, bg=SquareColor.DARK.value,
                                       command=lambda: self.pawnPromotionRook(coords, 'pyimage11'))
                        img2 = self.createImage(resource_path("img/Chess_rdt60.png"))
                        rbutt.configure(image=img2)

                        bbutt = Button(self.pawnPromotionWin, padx=20, pady=12, bg=SquareColor.LIGHT.value,
                                       command=lambda: self.pawnPromotionBishop(coords, 'pyimage9'))
                        img3 = self.createImage(resource_path("img/Chess_bdt60.png"))
                        bbutt.configure(image=img3)

                        kbutt = Button(self.pawnPromotionWin, padx=20, pady=12, bg=SquareColor.DARK.value,
                                       command=lambda: self.pawnPromotionKnight(coords, 'pyimage7'))
                        img4 = self.createImage(resource_path("img/Chess_ndt60.png"))
                        kbutt.configure(image=img4)

                qbutt.grid(row=0, column=0)
                kbutt.grid(row=0, column=1)
                bbutt.grid(row=0, column=2)
                rbutt.grid(row=0, column=3)

                self.pawnPromotionWin.grab_set()
                self.gameWindow.wait_window(self.pawnPromotionWin)

        self.selectedPiece = None
        self.selectedPieceCoords = None

    def pawnPromotionQueen(self, coords, img):
        self.buttonMatrix[coords[0]][coords[1]].configure(image=img)
        self.piecesMatrix[coords[0]][coords[1]] = Queen(coords[0], coords[1], self.turn)

        self.pawnPromotionWin.grab_release()
        self.pawnPromotionWin.destroy()

    def pawnPromotionKnight(self, coords, img):
        self.buttonMatrix[coords[0]][coords[1]].configure(image=img)
        self.piecesMatrix[coords[0]][coords[1]] = Knight(coords[0], coords[1], self.turn)

        self.pawnPromotionWin.grab_release()
        self.pawnPromotionWin.destroy()


    def pawnPromotionRook(self, coords, img):
        self.buttonMatrix[coords[0]][coords[1]].configure(image=img)
        self.piecesMatrix[coords[0]][coords[1]] = Rook(coords[0], coords[1], self.turn)

        self.pawnPromotionWin.grab_release()
        self.pawnPromotionWin.destroy()

    def pawnPromotionBishop(self, coords, img):
        self.buttonMatrix[coords[0]][coords[1]].configure(image=img)
        self.piecesMatrix[coords[0]][coords[1]] = Bishop(coords[0], coords[1], self.turn)

        self.pawnPromotionWin.grab_release()
        self.pawnPromotionWin.destroy()\

    def attackPiece(self, coords):
        removedPiece = self.piecesMatrix[coords[0]][coords[1]]
        removedPieceImage = self.buttonMatrix[coords[0]][coords[1]].cget('image')
        # needs to be added to a list or sth
        self.simpleMove(coords)

    def changeTurn(self):
        if self.turn == Color.DARK:
            self.updateDarkAttackLayout()
            # print(self.darkAttackLayout)
            self.turn = Color.LIGHT
        else:
            self.updateLightAttackLayout()
            # print(self.lightAttackLayout)
            self.turn = Color.DARK

    def updateColors(self):
        for i in range(0, 8):
            for j in range(0, 8):
                match self.availablePositions[i][j]:
                    case 1:
                        self.buttonMatrix[i][j].configure(bg=SquareColor.AVAILABLE.value)
                    case 2:
                        self.buttonMatrix[i][j].configure(bg=SquareColor.ATTACK.value)
                    case 4:
                        self.buttonMatrix[i][j].configure(bg=SquareColor.ATTACK.value)
                    case _:
                        self.buttonMatrix[i][j].configure(
                            bg=SquareColor.LIGHT.value if (i + j) % 2 == 0 else SquareColor.DARK.value)

    def resetColors(self):
        for i in range(0, 8):
            for j in range(0, 8):
                self.availablePositions[i][j] = 0
        self.updateColors()

    def darkKingIsChecked(self):
        return self.lightAttackLayout[self.darkKing.getCoords()[0]][self.darkKing.getCoords()[1]] == 2

    def lightKingIsChecked(self):
        return self.darkAttackLayout[self.lightKing.getCoords()[0]][self.lightKing.getCoords()[1]] == 2

    def updateDarkAttackLayout(self):
        for i in range(0, 8):
            for j in range(0, 8):
                self.darkAttackLayout[i][j] = 0

        for i in range(0, 8):
            for j in range(0, 8):
                if self.piecesMatrix[i][j] is None:
                    continue
                if self.piecesMatrix[i][j].getColor() == Color.LIGHT:
                    continue

                if self.darkAttackLayout[i][j] == 0:
                    self.darkAttackLayout[i][j] = -1

                # create an auxiliary position matrix
                aux = np.zeros((8, 8))

                # find this piece's attacking layout
                self.piecesMatrix[i][j].setAvailablePositions(aux, self.piecesMatrix)

                # update this layout
                for k in range(0, 8):
                    for l in range(0, 8):
                        if aux[k][l] == 0:
                            continue
                        if (aux[k][l] == 1 and self.piecesMatrix[i][j].getType() != PieceType.PAWN) \
                                or aux[k][l] == -1:
                            self.darkAttackLayout[k][l] = 1
                        if aux[k][l] == 2:
                            self.darkAttackLayout[k][l] = 2
                        if aux[k][l] == 3:
                            if self.darkAttackLayout[k][l] == 5 \
                                    or self.darkAttackLayout[k][l] == 6:
                                self.darkAttackLayout[k][l] = 6
                            else:
                                self.darkAttackLayout[k][l] = 3
                        if aux[k][l] == 4:
                            self.darkAttackLayout[k][l] = 4
                        if aux[k][l] == 5:
                            if self.darkAttackLayout[k][l] == -1:
                                self.darkAttackLayout[k][l] = 5
                            else:
                                self.darkAttackLayout[k][l] = 6

    def updateLightAttackLayout(self):
        for i in range(0, 8):
            for j in range(0, 8):
                self.lightAttackLayout[i][j] = 0

        for i in range(0, 8):
            for j in range(0, 8):
                if self.piecesMatrix[i][j] is None:
                    continue
                if self.piecesMatrix[i][j].getColor() == Color.DARK:
                    continue

                if self.lightAttackLayout[i][j] == 0:
                    self.lightAttackLayout[i][j] = -1

                # create an auxiliary position matrix
                aux = np.zeros((8, 8))

                # find this piece's attacking layout
                self.piecesMatrix[i][j].setAvailablePositions(aux, self.piecesMatrix)

                # update this layout
                for k in range(0, 8):
                    for l in range(0, 8):
                        if aux[k][l] == 0:
                            continue
                        if (aux[k][l] == 1 and self.piecesMatrix[i][j].getType() != PieceType.PAWN) \
                                or aux[k][l] == -1:
                            self.lightAttackLayout[k][l] = 1
                        if aux[k][l] == 2:
                            self.lightAttackLayout[k][l] = 2
                        if aux[k][l] == 3:
                            if self.lightAttackLayout[k][l] == 5 \
                                    or self.lightAttackLayout[k][l] == 6:
                                self.lightAttackLayout[k][l] = 6
                            else:
                                self.lightAttackLayout[k][l] = 3
                        if aux[k][l] == 4:
                            self.lightAttackLayout[k][l] = 4
                        if aux[k][l] == 5:
                            if self.lightAttackLayout[k][l] == -1:
                                self.lightAttackLayout[k][l] = 5
                            else:
                                self.lightAttackLayout[k][l] = 6
