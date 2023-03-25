import pandas as pd
from typing import List
import numpy as np
import pathlib

BOARD_ROW = 6
BOARD_COL = 7
CURRENT_FOLDER = pathlib.Path(__file__).parent
MATCH_DATA_PATH = CURRENT_FOLDER / "matchdata.txt"

PLAYER = 1

def creat_board():
    """create the empty board"""
    board=np.zeros((BOARD_ROW,BOARD_COL))
    return board

def execute(board: List[str], col:int,row: int, player:int)->None:
    """Execute the movement

    Args:
        board: the current board
        col: colum of movement
        row: row of movement
        color: color represents the player

    Return:
        None, update the board with the color
    """
    board[row][col]= player


def check_winning():
    return False

def run():

    data = pd.read_csv(MATCH_DATA_PATH)
    print(data)

    board = creat_board()

    turn = 0
    game_finish = False

    while not game_finish:
        if turn ==0:
            # player 1 play
            execute(board=board,col=1,row=1,player=0)
            check_winning()
        else:
            # player 2 play
            execute(board=board,col=1,row=1,player=0)
            check_winning()


    return []

if __name__ =="__main__":
    run()
