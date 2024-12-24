import game
import utils
from tkinter import *


class Menu:
    def __init__(self, master):
        self.waiting = None
        self.master = master
        self.difficulty = None
        self.statusId = None
        self.urlForGet = "https://sugoku.onrender.com/board?difficulty="
        self.urlForPost = "https://sugoku.onrender.com/solve"
        self.frameOfMenu = Frame(self.master)
        self.frameOfMenu.grid(row=0, column=0, sticky=NSEW, padx=10, pady=10)
        self.displayMenu()

    def displayMenu(self):
        """
        display the menu by placing all required widgets
        :return: the frame of menu
        """
        tipsForChoosingDifficulty = Label(self.frameOfMenu, text="Choose difficulty",
                                          font=("Arial", 25, "bold"))
        tipsForChoosingDifficulty.grid(row=0, column=0, sticky=N, padx=360, pady=10)
        easy = Button(self.frameOfMenu, text="Easy", font=("Arial", 20),
                      command=lambda: self.saveDifficulty("easy"), relief=GROOVE, width=7)
        easy.grid(row=1, column=0, sticky=N, padx=10, pady=10)
        medium = Button(self.frameOfMenu, text="Medium", font=("Arial", 20),
                        command=lambda: self.saveDifficulty("medium"), relief=GROOVE, width=7)
        medium.grid(row=2, column=0, sticky=N, padx=10, pady=10)
        hard = Button(self.frameOfMenu, text="Hard", font=("Arial", 20),
                      command=lambda: self.saveDifficulty("hard"), relief=GROOVE, width=7)
        hard.grid(row=3, column=0, sticky=N, padx=10, pady=10)
        self.waiting = Label(self.frameOfMenu, text="Requesting puzzles online...",
                             font=("Arial", 30, "bold"), fg="black")
        return self.frameOfMenu

    def saveDifficulty(self, difficulty):
        """
        save the difficulty
        :param difficulty: preferred difficulty
        """
        self.waiting.grid(row=4, column=0, sticky=N, padx=10, pady=10)
        self.difficulty = difficulty
        self.urlForGet += self.difficulty

    def checkStatus(self):
        # check whether difficulty has been chosen by running this function per 10 ms if chosen, start game
        if self.difficulty is not None:
            self.master.after_cancel(self.statusId)
            puzzle = utils.getPuzzle(self.urlForGet, self.urlForPost)
            utils.clearFrame(self.frameOfMenu)
            gameController = game.GameController(self.master, puzzle, -1)
            temp = gameController.monitor()
        else:
            self.statusId = self.master.after(10, self.checkStatus) # run self.checkStatus per 10 ms