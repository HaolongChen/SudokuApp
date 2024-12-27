import menu
from tkinter import *

root = Tk()
root.title('SudokuApp')
root.geometry('1000x570')
menuController = menu.Menu(root)
menuController.checkStatus()

root.mainloop()