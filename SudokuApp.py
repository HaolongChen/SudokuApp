import menu, game, result
import utils
from utils import *

root = Tk()
root.title('SudokuApp')
root.geometry('1000x570')
menuController = menu.Menu(root)
menuController.checkStatus()


root.mainloop()