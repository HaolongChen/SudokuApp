import result
import utils, math, copy, menu
from tkinter import *
from tkinter import messagebox


class Grid:
    def __init__(self, master, puzzle):
        self.master = master
        self.frameOfGame = Frame(self.master)
        self.frameOfGame.grid(row=0, column=0, sticky=NSEW)
        self.puzzle = puzzle
        self.cellSize = 60
        self.canvasWidth = self.cellSize * 10 + 30
        self.canvasHeight = self.cellSize * 10
        self.canvasOfGame = Canvas(self.frameOfGame, width=self.canvasWidth,
                                   height=self.canvasHeight)
        self.prevRow = None
        self.prevCol = None
        self.drawGrid()
        self.drawNumber()
        self.canvasOfGame.bind("<Button-1>", self.handleClick)
        self.answerOfUser = copy.deepcopy(self.puzzle)
        self.canvasOfGame.grid(row=0, column=0, sticky=W, rowspan=55)


    def drawGrid(self):
        """
        Draws the grid without numbers
        Among 100 lines, 8 bold lines are drawn
        to split blocks whose width is 3px,
        while width of thin lines is 1px
        set background color of 4 blocks to grey
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
                                              (self.cellSize + 1) * i + math.ceil(i / 3) * 2 + 8,
                                                   width=0, fill='black')

        for i in range(1, 10):
            for j in range(1, 10):
                # i represents column
                # j represents row
                x1 = ((self.cellSize + 1) * i + math.ceil(i / 3) * 2 - self.cellSize) + 5
                y1 = ((self.cellSize + 1) * j + math.ceil(j / 3) * 2 - self.cellSize) + 5
                x2 = ((self.cellSize + 1) * i + math.ceil(i / 3) * 2) + 5
                y2 = ((self.cellSize + 1) * j + math.ceil(j / 3) * 2) + 5
                if (4 <= i <= 6 and (1 <= j <= 3 or 7 <= j <= 9)) or (1 <= i <= 3 and 4 <= j <= 6) or (
                        7 <= i <= 9 and 4 <= j <= 6):
                    if self.puzzle[j - 1][i - 1] != 0:
                        self.canvasOfGame.create_rectangle(x1, y1, x2, y2, fill="light grey", width=0)
                    else:
                        self.canvasOfGame.create_rectangle(x1, y1, x2, y2, fill="light grey",
                                                           tags=f"empty{j - 1}_{i - 1}", width=0)
                else:
                    if self.puzzle[j - 1][i - 1] != 0:
                        self.canvasOfGame.create_rectangle(x1, y1, x2, y2, fill="white", width=0)
                    else:
                        self.canvasOfGame.create_rectangle(x1, y1, x2, y2, fill="white",
                                                           tags=f"empty{j - 1}_{i - 1}", width=0)

        return self.canvasOfGame



    def drawNumber(self):
        # draw all non-zero numbers to the grid
        # mark lattices without numbers as vacant
        for i in range(1, 10):
            for j in range(1, 10):
                """
                i represents column
                j represents row
                """
                x = (self.cellSize + 1) * i + math.ceil(i / 3) * 2 - self.cellSize / 2 + 5
                y = (self.cellSize + 1) * j + math.ceil(j / 3) * 2 - self.cellSize / 2 + 5
                if self.puzzle[j - 1][i - 1] != 0:
                    self.canvasOfGame.create_text(x, y, text=str(self.puzzle[j - 1][i - 1]),
                                                  font=("Arial", 20), tags="numbers")
                else:
                    self.canvasOfGame.create_text(x, y, text="", font=("Allura", 20, "bold"),
                                                  tags=f"number{j - 1}_{i - 1}", fill="blue")


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
        if 9 > j >= 0 == self.puzzle[j][i] and 0 <= i < 9:
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





class MainUI:
    def __init__(self, master, counter):
        self.buttonX = None
        self.restart = None
        self.reset = None
        self.master = master
        self.n9 = None
        self.n8 = None
        self.n7 = None
        self.n6 = None
        self.n5 = None
        self.n4 = None
        self.n3 = None
        self.n2 = None
        self.n1 = None
        self.numberOfClicked = None
        self.timer = None
        self.counter = counter
        self.timeId = None
        self.displayTimer()
        self.displayNuber()
        self.displayReset()
        self.displayRestart()
        self.displayX()

    def displayTimer(self):
        # display timer
        self.timer = Label(self.master, text="00:00", font=("Arial", 35, "bold"))
        self.timer.grid(row=0, column=2, sticky='nw', padx=1, pady=5, columnspan=3)
        self.updateTimer()

    def updateTimer(self):
        # update timer
        self.counter += 1
        self.timer.config(text=utils.getMinAndSec(self.counter))
        self.timeId = self.master.after(1000, self.updateTimer)

    def stopTimer(self):
        # stop updating timer
        self.master.after_cancel(self.timeId)
        self.timeId = None


    def recordNumberOfClicked(self, number):
        """
        record the button of clicked
        :param number: tag of button of clicked
        """
        self.numberOfClicked = number

    def displayNuber(self):
        # display button of numbers
        self.n1 = Button(self.master, text="1", font=("Arial", 35, "bold"), width=3, height=1,
                         bg="light grey", command=lambda: self.recordNumberOfClicked("1"))
        self.n2 = Button(self.master, text="2", font=("Arial", 35, "bold"), width=3, height=1,
                         bg="light grey", command=lambda: self.recordNumberOfClicked("2"))
        self.n3 = Button(self.master, text="3", font=("Arial", 35, "bold"), width=3, height=1,
                         bg="light grey", command=lambda: self.recordNumberOfClicked("3"))
        self.n4 = Button(self.master, text="4", font=("Arial", 35, "bold"), width=3, height=1,
                         bg="light grey", command=lambda: self.recordNumberOfClicked("4"))
        self.n5 = Button(self.master, text="5", font=("Arial", 35, "bold"), width=3, height=1,
                         bg="light grey", command=lambda: self.recordNumberOfClicked("5"))
        self.n6 = Button(self.master, text="6", font=("Arial", 35, "bold"), width=3, height=1,
                         bg="light grey", command=lambda: self.recordNumberOfClicked("6"))
        self.n7 = Button(self.master, text="7", font=("Arial", 35, "bold"), width=3, height=1,
                         bg="light grey", command=lambda: self.recordNumberOfClicked("7"))
        self.n8 = Button(self.master, text="8", font=("Arial", 35, "bold"), width=3, height=1,
                         bg="light grey", command=lambda: self.recordNumberOfClicked("8"))
        self.n9 = Button(self.master, text="9", font=("Arial", 35, "bold"), width=3, height=1,
                         bg="light grey", command=lambda: self.recordNumberOfClicked("9"))
        self.n1.grid(row=1, column=1, padx=1, pady=1, sticky=EW)
        self.n2.grid(row=1, column=2, padx=1, pady=1, sticky=EW)
        self.n3.grid(row=1, column=3, padx=1, pady=1, sticky=EW)
        self.n4.grid(row=2, column=1, padx=1, pady=1, sticky=EW)
        self.n5.grid(row=2, column=2, padx=1, pady=1, sticky=EW)
        self.n6.grid(row=2, column=3, padx=1, pady=1, sticky=EW)
        self.n7.grid(row=3, column=1, padx=1, pady=1, sticky=EW)
        self.n8.grid(row=3, column=2, padx=1, pady=1, sticky=EW)
        self.n9.grid(row=3, column=3, padx=1, pady=1, sticky=EW)

    def displayReset(self):
        # display reset button
        self.reset = Button(self.master, text="reset", font=("Arial", 35, "bold"), width=3, height=1,
                            bg="light grey", command=lambda: self.recordNumberOfClicked("reset"))
        self.reset.grid(row=4, column=1, padx=1, pady=1, sticky=EW, columnspan=2)

    def displayRestart(self):
        # display restart button
        self.restart = Button(self.master, text="restart", font=("Arial", 35, "bold"), width=3, height=1,
                              bg="light grey", command=lambda: self.recordNumberOfClicked("restart"))
        self.restart.grid(row=5, column=1, padx=1, pady=1, sticky=EW, columnspan=3)

    def displayX(self):
        # display X button for clearing the current cell
        self.buttonX = Button(self.master, text="x", font=("Arial", 35, "bold"), width=3, height=1,
                              bg="light grey", command=lambda: self.recordNumberOfClicked(""))
        self.buttonX.grid(row=4, column=3, padx=1, pady=1, sticky=EW)


class GameController(Grid, MainUI):
    def __init__(self, master, puzzle, counter):
        self.localMaster = master
        self.puzzle = puzzle
        self.warn = False
        Grid.__init__(self, master, puzzle)
        MainUI.__init__(self, self.frameOfGame, counter)
        self.status = None


    def monitor(self):
        """
        monitor game status
        :return: 0 if restarting, 1 if running normally
        """
        if self.numberOfClicked == "restart":
            # clear all and run menu
            self.frameOfGame.after_cancel(self.status)
            self.canvasOfGame.delete("all")
            utils.clearFrame(self.frameOfGame)
            self.stopTimer()
            self.status = None
            menuController = menu.Menu(self.localMaster)
            menuController.checkStatus()
            return 0

        if self.numberOfClicked == "reset":
            # clear all and run game again retaining same puzzle and counter
            self.frameOfGame.after_cancel(self.status)
            self.canvasOfGame.delete("all")
            utils.clearFrame(self.frameOfGame)
            self.stopTimer()
            self.status = None
            self.__init__(self.localMaster, self.puzzle, self.counter)
            return self.monitor()

        if self.numberOfClicked is not None and self.prevCol is not None and self.prevRow is not None:
            # input a number to the puzzle
            if len(self.numberOfClicked) > 0:
                self.answerOfUser[self.prevRow][self.prevCol] = int(self.numberOfClicked)
            self.canvasOfGame.itemconfig(f"number{self.prevRow}_{self.prevCol}",
                                         text=self.numberOfClicked)
            self.numberOfClicked = None
            self.warn = False

        if all(0 not in self.answerOfUser[i] for i in range(9)):
            # check if completed
            if utils.validity(self.answerOfUser):
                # correct
                self.stopTimer()
                self.frameOfGame.after_cancel(self.status)
                if self.canvasOfGame.winfo_exists():
                    self.canvasOfGame.delete("all")
                utils.clearFrame(self.frameOfGame)
                self.status = None
                result.Result(self.counter, self.localMaster)
                return 1

            else:
                # incorrect
                if not self.warn:
                    messagebox.showwarning("Warning", "The puzzle is incorrect")
                self.warn = True

        self.status = self.frameOfGame.after(10, self.monitor)
