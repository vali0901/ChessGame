from tkinter import *
from PIL import Image, ImageTk

from pieces import *
from pieces.Piece import *


class SquareColor(Enum):
    DARK = '#948245'
    LIGHT = '#E6dAB2'
    AVAILABLE = '#FFF5bd'
    ATTACK = '#F74739'


class Game:
    gameWindow = None
    buttonMatrix = None
    piecesMatrix = None
    selectedPiece = None
    selectedPieceCoords = None
    availablePositions = None
    turn = None
    darkKing = None
    darkCheck = None
    lightKing = None
    lightCheck = None
    checkingPosition = None

    darkAttackLayout = None
    lightAttackLayout = None

    def __init__(self):
        self.gameWindow = Tk()
        self.buttonMatrix = []
        self.piecesMatrix = []
        self.availablePositions = []
        self.checkingPosition = []
        self.darkAttackLayout = []
        self.lightAttackLayout = []
        self.turn = Color.LIGHT

        for i in range(0, 8):
            row = []
            for j in range(0, 8):
                row.append(0)
            self.availablePositions.append(row)

        for i in range(0, 8):
            row = []
            for j in range(0, 8):
                row.append(0)
            self.checkingPosition.append(row)

        for i in range(0, 8):
            row = []
            for j in range(0, 8):
                row.append(0)
            self.darkAttackLayout.append(row)

        for i in range(0, 8):
            row = []
            for j in range(0, 8):
                row.append(0)
            self.lightAttackLayout.append(row)

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
                newButton = Button(self.gameWindow, padx=100, pady=80, bg=color.value,
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
        lightP = Image.open("img/Chess_plt60.png")
        helper1 = lightP.resize((self.buttonMatrix[0][0].winfo_width() - 5, self.buttonMatrix[0][0].winfo_height() - 5))
        helper = ImageTk.PhotoImage(helper1)
        lightP = helper

        darkP = Image.open("img/Chess_pdt60.png")
        helper1 = darkP.resize((self.buttonMatrix[0][0].winfo_width() - 5, self.buttonMatrix[0][0].winfo_height() - 5))
        helper = ImageTk.PhotoImage(helper1)
        darkP = helper

        for i in range(0, 8):
            self.buttonMatrix[1][i].configure(image=darkP)
            self.buttonMatrix[6][i].configure(image=lightP)

        # adding the other pieces

        # King
        darkK = Image.open("img/Chess_kdt60.png")
        helper1 = darkK.resize((self.buttonMatrix[0][0].winfo_width() - 5, self.buttonMatrix[0][0].winfo_height() - 5))
        helper = ImageTk.PhotoImage(helper1)
        darkK = helper

        lightK = Image.open("img/Chess_klt60.png")
        helper1 = lightK.resize((self.buttonMatrix[0][0].winfo_width() - 5, self.buttonMatrix[0][0].winfo_height() - 5))
        helper = ImageTk.PhotoImage(helper1)
        lightK = helper

        self.buttonMatrix[0][4].configure(image=darkK)
        self.buttonMatrix[7][4].configure(image=lightK)

        # Queen
        darkQ = Image.open("img/Chess_qdt60.png")
        helper1 = darkQ.resize((self.buttonMatrix[0][0].winfo_width() - 5, self.buttonMatrix[0][0].winfo_height() - 5))
        helper = ImageTk.PhotoImage(helper1)
        darkQ = helper

        lightQ = Image.open("img/Chess_qlt60.png")
        helper1 = lightQ.resize((self.buttonMatrix[0][0].winfo_width() - 5, self.buttonMatrix[0][0].winfo_height() - 5))
        helper = ImageTk.PhotoImage(helper1)
        lightQ = helper

        self.buttonMatrix[0][3].configure(image=darkQ)
        self.buttonMatrix[7][3].configure(image=lightQ)

        # Knight
        darkN = Image.open("img/Chess_ndt60.png")
        helper1 = darkN.resize((self.buttonMatrix[0][0].winfo_width() - 5, self.buttonMatrix[0][0].winfo_height() - 5))
        helper = ImageTk.PhotoImage(helper1)
        darkN = helper

        lightN = Image.open("img/Chess_nlt60.png")
        helper1 = lightN.resize((self.buttonMatrix[0][0].winfo_width() - 5, self.buttonMatrix[0][0].winfo_height() - 5))
        helper = ImageTk.PhotoImage(helper1)
        lightN = helper

        self.buttonMatrix[0][1].configure(image=darkN)
        self.buttonMatrix[7][1].configure(image=lightN)
        self.buttonMatrix[0][6].configure(image=darkN)
        self.buttonMatrix[7][6].configure(image=lightN)

        # Bishop
        darkB = Image.open("img/Chess_bdt60.png")
        helper1 = darkB.resize((self.buttonMatrix[0][0].winfo_width() - 5, self.buttonMatrix[0][0].winfo_height() - 5))
        helper = ImageTk.PhotoImage(helper1)
        darkB = helper

        lightB = Image.open("img/Chess_blt60.png")
        helper1 = lightB.resize((self.buttonMatrix[0][0].winfo_width() - 5, self.buttonMatrix[0][0].winfo_height() - 5))
        helper = ImageTk.PhotoImage(helper1)
        lightB = helper

        self.buttonMatrix[0][2].configure(image=darkB)
        self.buttonMatrix[7][5].configure(image=lightB)
        self.buttonMatrix[0][5].configure(image=darkB)
        self.buttonMatrix[7][2].configure(image=lightB)

        # Rook
        darkR = Image.open("img/Chess_rdt60.png")
        helper1 = darkR.resize((self.buttonMatrix[0][0].winfo_width() - 5, self.buttonMatrix[0][0].winfo_height() - 5))
        helper = ImageTk.PhotoImage(helper1)
        darkR = helper

        lightR = Image.open("img/Chess_rlt60.png")
        helper1 = lightR.resize((self.buttonMatrix[0][0].winfo_width() - 5, self.buttonMatrix[0][0].winfo_height() - 5))
        helper = ImageTk.PhotoImage(helper1)
        lightR = helper

        self.buttonMatrix[0][0].configure(image=darkR)
        self.buttonMatrix[7][0].configure(image=lightR)
        self.buttonMatrix[0][7].configure(image=darkR)
        self.buttonMatrix[7][7].configure(image=lightR)
        self.gameWindow.mainloop()

        # Show window
        self.gameWindow.mainloop()

    def buttonClicked(self, coords):
        if self.piecesMatrix[coords[0]][coords[1]] is not None \
                and self.piecesMatrix[coords[0]][coords[1]].getColor() == self.turn:
            # If a nonempty place is pressed and it has the same color as the player's turn
            # then the user is trying to select that piece
            if self.piecesMatrix[coords[0]][coords[1]].isSelected() == 0:
                if self.selectedPiece is not None:
                    self.selectedPiece.Unselect()

                # print(self.piecesMatrix[coords[0]][coords[1]])

                self.piecesMatrix[coords[0]][coords[1]].Select()

                self.selectedPiece = self.piecesMatrix[coords[0]][coords[1]]
                self.selectedPieceCoords = coords

                self.selectedPiece.setAvailablePositions(self.availablePositions, self.piecesMatrix)

                # print(self.availablePositions)
                self.updateColors()
        else:
            # user is trying to move the piece or attack another
            # (or it's not his turn, in that case nothing is done)

            # trying to move to an unavailable spot (unselect selected piece and reset the colors)
            if self.availablePositions[coords[0]][coords[1]] == 0:
                if self.selectedPiece is not None:
                    self.selectedPiece.Unselect()
                self.selectedPiece = None

                for i in range(0, 8):
                    for j in range(0, 8):
                        self.availablePositions[i][j] = 0
                self.updateColors()

            # trying to move to an empty spot or attack another piece
            else:
                self.moveSelectedPiece(coords)
                if self.turn == Color.LIGHT:
                    self.updateDarkAttackLayout()
                    if self.lightKingIsChecked():
                        print("light in check")
                else:
                    self.updateLightAttackLayout()
                    if self.darkKingIsChecked():
                        print("dark in check")



                for i in range(0, 8):
                    for j in range(0, 8):
                        self.availablePositions[i][j] = 0
                self.updateColors()

    def updateColors(self):
        for i in range(0, 8):
            for j in range(0, 8):
                match self.availablePositions[i][j]:
                    case 1:
                        self.buttonMatrix[i][j].configure(bg=SquareColor.AVAILABLE.value)
                    case 2:
                        self.buttonMatrix[i][j].configure(bg=SquareColor.ATTACK.value)
                    case _:
                        self.buttonMatrix[i][j].configure(
                            bg=SquareColor.LIGHT.value if (i + j) % 2 == 0 else SquareColor.DARK.value)

    def moveSelectedPiece(self, coords):
        # change de piece matrix
        removedPiece = self.piecesMatrix[coords[0]][coords[1]]
        if self.availablePositions[coords[0]][coords[1]] == 2 and removedPiece.getType() == PieceType.KING:
            self.selectedPiece.Unselect()
            return
        self.piecesMatrix[self.selectedPieceCoords[0]][self.selectedPieceCoords[1]] = None
        self.piecesMatrix[coords[0]][coords[1]] = self.selectedPiece
        self.selectedPiece.setCoords(coords)

        # change buttons matrix
        movingPieceImage = self.buttonMatrix[self.selectedPieceCoords[0]][self.selectedPieceCoords[1]].cget('image')
        self.buttonMatrix[self.selectedPieceCoords[0]][self.selectedPieceCoords[1]].configure(image='')
        self.buttonMatrix[coords[0]][coords[1]].configure(image=movingPieceImage)

        self.selectedPiece.Unselect()
        self.selectedPiece = None
        self.selectedPieceCoords = None

        # change the turn
        self.turn = Color.LIGHT if self.turn == Color.DARK else Color.DARK

        # check if the king is in check

    def darkKingIsChecked(self):
        return self.lightAttackLayout[self.darkKing.getCoords()[0]][self.darkKing.getCoords()[1]] == 2
    def lightKingIsChecked(self):
        return self.darkAttackLayout[self.lightKing.getCoords()[0]][self.lightKing.getCoords()[1]] == 2
        # currKing = self.lightKing if self.turn == Color.LIGHT else self.darkKing
        #
        # print(currKing.getColor())
        # for i in range(0, 8):
        #     for j in range(0, 8):
        #         if self.piecesMatrix[i][j] is None:
        #             continue
        #         if self.piecesMatrix[i][j].getColor() != currKing.getColor():
        #             # create an auxiliary position matrix
        #             aux = []
        #             for l in range(0, 8):
        #                 row = []
        #                 for k in range(0, 8):
        #                     row.append(0)
        #                 aux.append(row)
        #
        #             # find this piece's attacking direction
        #             self.piecesMatrix[i][j].setAvailablePositions(aux, self.piecesMatrix)
        #
        #             if aux[currKing.getCoords()[0]][currKing.getCoords()[1]] == 2:
        #                 print(currKing.getColor())
        #                 print("isChecked")


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

                if self.darkAttackLayout[i][j] != 3:
                    self.darkAttackLayout[i][j] = -1

                # create an auxiliary position matrix
                aux = []
                for l in range(0, 8):
                    row = []
                    for k in range(0, 8):
                        row.append(0)
                    aux.append(row)

                # find this piece's attacking direction
                self.piecesMatrix[i][j].setAvailablePositions(aux, self.piecesMatrix)

                match self.piecesMatrix[i][j].getType():
                    case PieceType.PAWN:
                        for k in range(0, 8):
                            for l in range(0, 8):
                                if aux[k][l] == 0:
                                    continue
                                if aux[k][l] == -1:
                                    self.darkAttackLayout[k][l] = 1
                                if aux[k][l] == 2:
                                    self.darkAttackLayout[k][l] = 2
                                if aux[k][l] == 3:
                                    self.darkAttackLayout[k][l] = 3

                    case PieceType.QUEEN:
                        for k in range(0, 8):
                            for l in range(0, 8):
                                if aux[k][l] == 0:
                                    continue
                                if aux[k][l] == 1:
                                    self.darkAttackLayout[k][l] = 1
                                if aux[k][l] == 2:
                                    self.darkAttackLayout[k][l] = 2
                                if aux[k][l] == 3:
                                    self.darkAttackLayout[k][l] = 3
                    case PieceType.KNIGHT:
                        for k in range(0, 8):
                            for l in range(0, 8):
                                if aux[k][l] == 0:
                                    continue
                                if aux[k][l] == 1:
                                    self.darkAttackLayout[k][l] = 1
                                if aux[k][l] == 2:
                                    self.darkAttackLayout[k][l] = 2
                                if aux[k][l] == 3:
                                    self.darkAttackLayout[k][l] = 3

                    case PieceType.BISHOP:
                        for k in range(0, 8):
                            for l in range(0, 8):
                                if aux[k][l] == 0:
                                    continue
                                if aux[k][l] == 1:
                                    self.darkAttackLayout[k][l] = 1
                                if aux[k][l] == 2:
                                    self.darkAttackLayout[k][l] = 2
                                if aux[k][l] == 3:
                                    self.darkAttackLayout[k][l] = 3

                    case PieceType.ROOK:
                        for k in range(0, 8):
                            for l in range(0, 8):
                                if aux[k][l] == 0:
                                    continue
                                if aux[k][l] == 1:
                                    self.darkAttackLayout[k][l] = 1
                                if aux[k][l] == 2:
                                    self.darkAttackLayout[k][l] = 2
                                if aux[k][l] == 3:
                                    self.darkAttackLayout[k][l] = 3
                    case PieceType.KING:
                        for k in range(0, 8):
                            for l in range(0, 8):
                                if aux[k][l] == 0:
                                    continue
                                if aux[k][l] == 1:
                                    self.darkAttackLayout[k][l] = 1
                                if aux[k][l] == 2:
                                    self.darkAttackLayout[k][l] = 2
                                if aux[k][l] == 3:
                                    self.darkAttackLayout[k][l] = 3

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

                if self.lightAttackLayout[i][j] != 3:
                    self.lightAttackLayout[i][j] = -1

                # create an auxiliary position matrix
                aux = []
                for l in range(0, 8):
                    row = []
                    for k in range(0, 8):
                        row.append(0)
                    aux.append(row)

                # find this piece's attacking direction
                self.piecesMatrix[i][j].setAvailablePositions(aux, self.piecesMatrix)

                match self.piecesMatrix[i][j].getType():
                    case PieceType.PAWN:
                        for k in range(0, 8):
                            for l in range(0, 8):
                                if aux[k][l] == 0:
                                    continue
                                if aux[k][l] == -1:
                                    self.lightAttackLayout[k][l] = 1
                                if aux[k][l] == 2:
                                    self.lightAttackLayout[k][l] = 2
                                if aux[k][l] == 3:
                                    self.lightAttackLayout[k][l] = 3

                    case PieceType.QUEEN:
                        for k in range(0, 8):
                            for l in range(0, 8):
                                if aux[k][l] == 0:
                                    continue
                                if aux[k][l] == 1:
                                    self.lightAttackLayout[k][l] = 1
                                if aux[k][l] == 2:
                                    self.lightAttackLayout[k][l] = 2
                                if aux[k][l] == 3:
                                    self.lightAttackLayout[k][l] = 3
                    case PieceType.KNIGHT:
                        for k in range(0, 8):
                            for l in range(0, 8):
                                if aux[k][l] == 0:
                                    continue
                                if aux[k][l] == 1:
                                    self.lightAttackLayout[k][l] = 1
                                if aux[k][l] == 2:
                                    self.lightAttackLayout[k][l] = 2
                                if aux[k][l] == 3:
                                    self.lightAttackLayout[k][l] = 3

                    case PieceType.BISHOP:
                        for k in range(0, 8):
                            for l in range(0, 8):
                                if aux[k][l] == 0:
                                    continue
                                if aux[k][l] == 1:
                                    self.lightAttackLayout[k][l] = 1
                                if aux[k][l] == 2:
                                    self.lightAttackLayout[k][l] = 2
                                if aux[k][l] == 3:
                                    self.lightAttackLayout[k][l] = 3

                    case PieceType.ROOK:
                        for k in range(0, 8):
                            for l in range(0, 8):
                                if aux[k][l] == 0:
                                    continue
                                if aux[k][l] == 1:
                                    self.lightAttackLayout[k][l] = 1
                                if aux[k][l] == 2:
                                    self.lightAttackLayout[k][l] = 2
                                if aux[k][l] == 3:
                                    self.lightAttackLayout[k][l] = 3
                    case PieceType.KING:
                        for k in range(0, 8):
                            for l in range(0, 8):
                                if aux[k][l] == 0:
                                    continue
                                if aux[k][l] == 1:
                                    self.lightAttackLayout[k][l] = 1
                                if aux[k][l] == 2:
                                    self.lightAttackLayout[k][l] = 2
                                if aux[k][l] == 3:
                                    self.lightAttackLayout[k][l] = 3


