import utils, menu
from tkinter import *

class Result:
    def __init__(self, counter, master):
        self.counter = counter
        self.master = master
        self.text = str(self.counter // 60) + " min " + str(self.counter % 60) + " sec"
        self.frameOfResult = Frame(self.master)
        self.frameOfResult.grid(row=0, column=0, sticky=NSEW)
        self.displayResult()
        self.displayRestart()

    def displayResult(self):
        # display the time user spends
        res = Label(self.frameOfResult, text="You spent " + self.text, font=("Arial", 20))
        res.grid(row=0, column=0, sticky=N, padx=372, pady=20)

    def displayRestart(self):
        # display a button for restarting the game
        restart = Button(self.frameOfResult, text="Restart", font=("Arial", 30), command=self.restart)
        restart.grid(row=1, column=0, sticky=N, pady=50)

    def restart(self):
        # restart the game
        utils.clearFrame(self.frameOfResult)
        menuController = menu.Menu(self.master)
        menuController.checkStatus()