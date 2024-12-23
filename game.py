import utils, math
from tkinter import *

class Game:
    def __init__(self, master):
        self.master = master
        self.frameOfGame = utils.createFrameOfMenu(self.master)
        self.frameOfGame.grid(row=0, column=0, sticky=NSEW)


class Grid(Game):
    def __init__(self, master, value, solution):
        super().__init__(master)
        self.value = value
        self.solution = solution
        self.cellSize = 60
        self.canvasWidth = self.cellSize * 10
        self.canvasHeight = self.cellSize * 10
        self.canvasOfGame = Canvas(self.frameOfGame, width=self.canvasWidth,
                                   height=self.canvasHeight)
        self.prevRow = None
        self.prevCol = None
        self.drawGrid()
        self.drawNumber()
        self.canvasOfGame.bind("<Button-1>", self.handleClick)
        self.answerOfUser = self.value
        self.canvasOfGame.grid(row=0, column=0, sticky=W)


    def drawGrid(self):
        """
        Draws the grid without numbers
        Among 100 lines, 8 bold lines are drawn
        to split subgrids whose width is 3px,
        while width of thin lines is 1px
        set background color of 4 subgrids to grey
        for better visualization
        :return: canvas of the grid
        """

        for i in range(10):
            if i % 3 != 0:
                self.canvasOfGame.create_rectangle((self.cellSize + 1) * i + math.ceil(i / 3) * 2 + 5, 0 + 5,
                                              (self.cellSize + 1) * i + math.ceil(i / 3) * 2 + 6,
                                              self.cellSize * 9 + 22, width=0, fill='grey')
                self.canvasOfGame.create_rectangle(5, (self.cellSize + 1) * i + math.ceil(i / 3) * 2 + 5,
                                              self.cellSize * 9 + 22,
                                              (self.cellSize + 1) * i + math.ceil(i / 3) * 2 + 6,
                                              width=0, fill='grey')
        for i in range(10):
            if i % 3 == 0:
                self.canvasOfGame.create_rectangle((self.cellSize + 1) * i + math.ceil(i / 3) * 2 + 5, 5,
                                              (self.cellSize + 1) * i + math.ceil(i / 3) * 2 + 8,
                                              self.cellSize * 9 + 22, width=0, fill='black')
                self.canvasOfGame.create_rectangle(5, (self.cellSize + 1) * i + math.ceil(i / 3) * 2 + 5,
                                              self.cellSize * 9 + 22,
                                              (self.cellSize + 1) * i + math.ceil(i / 3) * 2 + 8, width=0, fill='black')

        for i in range(1, 10):
            for j in range(1, 10):
                """
                i represents column
                j represents row
                """
                x1 = ((self.cellSize + 1) * i + math.ceil(i / 3) * 2 - self.cellSize) + 5
                y1 = ((self.cellSize + 1) * j + math.ceil(j / 3) * 2 - self.cellSize) + 5
                x2 = ((self.cellSize + 1) * i + math.ceil(i / 3) * 2) + 5
                y2 = ((self.cellSize + 1) * j + math.ceil(j / 3) * 2) + 5
                if (4 <= i <= 6 and (1 <= j <= 3 or 7 <= j <= 9)) or (1 <= i <= 3 and 4 <= j <= 6) or (
                        7 <= i <= 9 and 4 <= j <= 6):
                    if self.value[j - 1][i - 1] != 0:
                        self.canvasOfGame.create_rectangle(x1, y1, x2, y2, fill="light grey", width=0)
                    else:
                        self.canvasOfGame.create_rectangle(x1, y1, x2, y2, fill="light grey",
                                                           tags=f"empty{j - 1}_{i - 1}", width=0)
                else:
                    if self.value[j - 1][i - 1] != 0:
                        self.canvasOfGame.create_rectangle(x1, y1, x2, y2, fill="white", width=0)
                    else:
                        self.canvasOfGame.create_rectangle(x1, y1, x2, y2, fill="white",
                                                           tags=f"empty{j - 1}_{i - 1}", width=0)

        return self.canvasOfGame



    def drawNumber(self):
        """
        draw all non-zero numbers to the grid
        mark lattices without numbers as vacant
        """
        for i in range(1, 10):
            for j in range(1, 10):
                """
                i represents column
                j represents row
                """
                if self.value[j - 1][i - 1] != 0:
                    x = (self.cellSize + 1) * i + math.ceil(i / 3) * 2 - self.cellSize / 2 + 5
                    y = (self.cellSize + 1) * j + math.ceil(j / 3) * 2 - self.cellSize / 2 + 5
                    self.canvasOfGame.create_text(x, y, text=str(self.value[j - 1][i - 1]),
                                                  font=("Arial", 20), tags="numbers")


    def handleClick(self, event):
        """
        handle click event
        :param event: position where user clicked
        """
        j = event.y - 5
        i = event.x - 5
        for k in range(1, 10):
            prev = (self.cellSize + 1) * k + math.ceil(k / 3) * 2 - self.cellSize
            nxt = (self.cellSize + 1) * (k + 1) + math.ceil((k + 1) / 3) * 2 - self.cellSize
            if prev <= j <= nxt:
                j = k - 1
                break
        else:
            return

        for k in range(1, 10):
            prev = (self.cellSize + 1) * k + math.ceil(k / 3) * 2 - self.cellSize
            nxt = (self.cellSize + 1) * (k + 1) + math.ceil((k + 1) / 3) * 2 - self.cellSize
            if prev <= i <= nxt:
                i = k - 1
                break
        else:
            return
        if 9 > j >= 0 == self.value[j][i] and 0 <= i < 9:
            self.cellOfSelected(i, j)

    def cellOfSelected(self, i, j):
        """
        turn chosen cell to light blue and previous cell to normal
        :param i: column index
        :param j: row index
        """
        if self.prevRow is not None and self.prevCol is not None:
            if (3 <= self.prevCol <= 5 and (0 <= self.prevRow <= 2 or 6 <= self.prevRow <= 8)) or (
                    0 <= self.prevCol <= 2 and 3 <= self.prevRow <= 5) or (
                    6 <= self.prevCol <= 8 and 3 <= self.prevRow <= 5):
                self.canvasOfGame.itemconfig(f"empty{self.prevRow}_{self.prevCol}", fill="light grey")
            else:
                self.canvasOfGame.itemconfig(f"empty{self.prevRow}_{self.prevCol}", fill="white")

        self.prevCol = i
        self.prevRow = j
        self.canvasOfGame.itemconfig(f"empty{self.prevRow}_{self.prevCol}", fill="light blue")





class MainUI(Game):
    def __init__(self, master):
        super().__init__(master)
        self.counter = -1
        self.timeId = None


class GameController(Grid, MainUI):
    def __init__(self, master, value, solution):
        MainUI.__init__(self, master)
        Grid.__init__(self, master, value, solution)

    def startGame(self):
        Grid().master.configure(bg='')
        Grid().__init__(self, self.value, self.solution)
