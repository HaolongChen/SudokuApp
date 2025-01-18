import os
import requests
from openai import OpenAI

def askGPT(puzzle):
    """
    ask chatGPT for the tips for next step of solving the puzzle
    Using chatGPT 4o mini of GitHub model
    :param puzzle: current puzzle including user's input
    :return: message returned from chatGPT
    """
    token = open("API.lib", "r").read()
    endpoint = "https://models.inference.ai.azure.com"
    modelName = "gpt-4o-mini"
    client = OpenAI(
        base_url=endpoint,
        api_key=token,
    )
    prompt = """
    You will receive a Sudoku puzzle represented as a 2D array. Each row is a list of 9 integers, where 0 represents an empty cell. 
    Your task is to provide a single tip for the next step in solving the puzzle. 
    Follow these rules strictly:
    0. You should think as a human, not as a computer.
    1. Check each row, column, and 3x3 grid for possible values.
    2. Identify the most obvious and direct number that can be inferred based on Sudoku rules.
    3. The row and column of sudoku puzzle are 1-indexed.
    4. Analyze the puzzle and use one method of Scanning (Single Candidate), Elimination (Pencil Marks), Unique Candidate (Only Choice),
    Naked Single,Hidden Single,Naked Pair,Hidden Pair,
    Naked Triple,Hidden Triple,Pointing Pair,Pointing Triple. 
    Try to use Scanning (Single Candidate), Elimination (Pencil Marks), Unique Candidate (Only Choice) first, 
    infer step by step and double like a human check whether the tip you provide is absolutely correct.
    5. Before you are ready to give a tip, solve the puzzle completely and check whether the tip you provide is correct.
    If incorrect, repeat rule 4.
    6. Response template: By using [method], the cell in row [x] and column [y] has the number [z].
    7. Do not provide any extra information or code.
    """
    res = ""
    row = 1
    for array in puzzle:
        res += "row" + str(row) + ": "
        for number in array:
            res = res + str(number) + " "
        row += 1
    response = client.chat.completions.create(
        messages=[{"role": "system", "content": prompt}, {"role": "user", "content": res}],
        temperature=1.0,
        top_p=1.0,
        max_tokens=1000,
        model=modelName
    )
    return response.choices[0].message.content


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