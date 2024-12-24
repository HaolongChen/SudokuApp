import requests


def clearFrame(frame):
    # remove all widgets from a frame
    for widget in frame.winfo_children():
        widget.destroy()
    frame.grid_forget()
    frame.destroy()

def getPuzzle(geturl, posturl):
    """
    get a puzzle
    :param geturl: url for getting puzzle
    :param posturl: url for posting puzzle
    :return: a puzzle
    """
    response = requests.get(geturl)
    if response.status_code == 200:
        puzzle = response.json()
        return puzzle['board']
    else:
        print("Error: API request failed with status code {}".format(response.status_code))
        if response.status_code == 504:
            print("To many requests, try again later")
        return None

def getMinAndSec(counter):
    """
    :param counter: total time in seconds
    :return: minute and second in form of MM:SS
    """
    minute, second = counter // 60, counter % 60
    timer = str(minute) + ":" + str(second)
    if timer.find(":") <= 1:
        timer = '0' + timer
    if len(timer) - timer.find(":") <= 2:
        timer = timer[0:timer.find(":") + 1] + '0' + timer[timer.find(":") + 1:]
    return timer

def validity(puzzle):
    """
    check if a puzzle is valid
    :param puzzle: user's puzzle
    :return: True if valid, False if not
    """
    for i in range(9):
        if not repeat(puzzle[i]):
            return False
    for i in range(9):
        numbers = list()
        for j in range(9):
            numbers.append(puzzle[j][i])
        if not repeat(numbers):
            return False
    rows = [0, 3, 6]
    cols = [0, 3, 6]
    for row in rows:
        for col in cols:
            numbers = list()
            for i in range(3):
                for j in range(3):
                    numbers.append(puzzle[row + i][col + j])
            if not repeat(numbers):
                return False
    return True


def repeat(numbers):
    """
    check if a list of numbers is repeated
    :param numbers: a row, a column or a block
    :return: True if not repeated, False if repeated
    """
    for i in range(1, 10):
        if i not in numbers:
            return False
    return True