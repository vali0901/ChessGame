from tkinter import *
from PIL import Image, ImageTk


class Game:
    gameWindow = None
    buttonMatrix = None

    def __init__(self):
        self.gameWindow = Tk()
        #self.gameWindow.geometry("720x720")
        self.buttonMatrix = []

    def createButtonMatrix(self):
        # creates the button matrix
        for i in range(0, 8):
            helperRow = []
            for j in range(0, 8):
                if (i + j) % 2 == 0:
                    color = '#E6dAB2'
                else:
                    color = '#948245'

                newButton = Button(self.gameWindow, padx=100, pady=80, bg=color)
                newButton.grid(row=i, column=j)
                helperRow.append(newButton)
                newButton.update()

            self.buttonMatrix.append(helperRow)

    def startGame(self):
        self.createButtonMatrix()

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

            print(len(self.buttonMatrix[i]))

        # adding the other pieces

        #King
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

        #Queen
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

        #Knight
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

        #Bishop
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


