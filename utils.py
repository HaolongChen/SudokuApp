import requests
from tkinter import *

def clearFrame(frame):
    """remove all widgets from a frame"""
    for widget in frame.winfo_children():
        widget.destroy()

def getPuzzle(url, difficulty, step):
    """
    get a puzzle from url matching the difficulty
    :param url: a website url where the puzzles are generated
    :param difficulty: the difficulty of the puzzle user chooses
    :return: a list of puzzle named value and a list of solution named solution
    """
    response = requests.get(url)
    print("getting puzzle")
    if response.status_code == 200:
        print("matching puzzle")
        data = response.json()
        print (data)
        for i in range(0, 20):
            if data["newboard"]["grids"][i]["difficulty"] == difficulty:
                return (data["newboard"]["grids"][i]["value"],
                        data["newboard"]["grids"][i]["solution"])
            if step > 5 and difficulty == "Easy":
                if data["newboard"]["grids"][i]["difficulty"] == "Medium":
                    return (data["newboard"]["grids"][i]["value"],
                            data["newboard"]["grids"][i]["solution"])
        return getPuzzle(url, difficulty, step + 1)
    else:
        print("Error: API request failed with status code {}".format(response.status_code))
        if response.status_code == 504:
            print("To many requests, try again later")
            return getPuzzle(url, difficulty, step)
        return None

def createFrameOfMenu(master):
    """
    creates a new frame of menu
    :return: a new frame of menu
    """
    return Frame(master)