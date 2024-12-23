import game
import utils
from tkinter import *

class Menu:
    def __init__(self, master):
        self.master = master
        self.difficulty = None
        self.statusId = None
        self.url = ("https://sudoku-api.vercel.app/api/dosuku?query={newboard(limit:20){grids{value,solution,difficulty}}}")
        self.frameOfMenu = utils.createFrameOfMenu(self.master)
        self.frameOfMenu.grid(row=0, column=0, sticky=NSEW, padx=10, pady=10)
        self.displayMenu()

    def displayMenu(self):
        """
        display the menu by placing all required widgets
        :return: the frame of menu
        """
        tipsForChoosingDifficulty = Label(self.frameOfMenu, text="Choose difficulty", font=("Arial", 25, "bold"))
        tipsForChoosingDifficulty.grid(row=0, column=0, sticky=N, padx=360, pady=10)
        easy = Button(self.frameOfMenu, text="Easy", font=("Arial", 20), command=lambda: self.saveDifficulty("Easy"), relief=GROOVE, width=7)
        easy.grid(row=1, column=0, sticky=N, padx=10, pady=10)
        medium = Button(self.frameOfMenu, text="Medium", font=("Arial", 20), command=lambda: self.saveDifficulty("Medium"), relief=GROOVE, width=7)
        medium.grid(row=2, column=0, sticky=N, padx=10, pady=10)
        hard = Button(self.frameOfMenu, text="Hard", font=("Arial", 20), command=lambda: self.saveDifficulty("Hard"), relief=GROOVE, width=7)
        hard.grid(row=3, column=0, sticky=N, padx=10, pady=10)
        return self.frameOfMenu

    def saveDifficulty(self, difficulty):
        print("Requesting puzzles online...")
        self.difficulty = difficulty

    def checkStatus(self):
        """
        check whether difficulty has been chosen by running this function per 10 ms
        if chosen, start game
        """
        if self.difficulty is not None:
            self.master.after_cancel(self.statusId)
            value, solution = utils.getPuzzle(self.url, self.difficulty, 0)
            utils.clearFrame(self.frameOfMenu)
            gameController = game.GameController(self.master, value, solution)
        else:
            self.statusId = self.master.after(10, self.checkStatus) # run self.checkStatus per 10 ms