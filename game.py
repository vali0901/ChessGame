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
    selectedPieceCoords = None;
    availablePositions = None
    turn = None

    def __init__(self):
        self.gameWindow = Tk()
        self.buttonMatrix = []
        self.piecesMatrix = []
        self.availablePositions = []
        self.turn = Color.LIGHT

        for i in range(0, 8):
            row = []
            for j in range(0, 8):
                row.append(0)
            self.availablePositions.append(row)

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
                    lightBackRow.append(King(7, i, Color.LIGHT))
                    darkBackRow.append(King(0, i, Color.DARK))
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
        if self.piecesMatrix[coords[0]][coords[1]] is not None\
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

                for i in range(0, 8):
                    for j in range(0, 8):
                        self.availablePositions[i][j] = 0
                self.updateColors()

    def updateColors(self):
        for i in range(0, 8):
            for j in range(0, 8):
                match self.availablePositions[i][j]:
                    case 0:
                        self.buttonMatrix[i][j].configure(
                            bg=SquareColor.LIGHT.value if (i + j) % 2 == 0 else SquareColor.DARK.value)
                    case 1:
                        self.buttonMatrix[i][j].configure(bg=SquareColor.AVAILABLE.value)
                    case 2:
                        self.buttonMatrix[i][j].configure(bg=SquareColor.ATTACK.value)

    def moveSelectedPiece(self, coords):
        # change de piece matrix
        self.piecesMatrix[self.selectedPieceCoords[0]][self.selectedPieceCoords[1]] = None
        removedPiece = self.piecesMatrix[coords[0]][coords[1]]
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


