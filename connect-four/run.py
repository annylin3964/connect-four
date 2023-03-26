import pathlib
from typing import Dict, List, Any

import numpy as np
import pandas as pd

BOARD_ROW = 6
BOARD_COL = 7
CURRENT_FOLDER = pathlib.Path(__file__).parent
MATCH_DATA_PATH = CURRENT_FOLDER / "matchdata.txt"


def creat_board():
    """create the empty board"""
    board = np.zeros((BOARD_ROW, BOARD_COL))
    return board


def execute(board: List[Any], col: int, row: int, player: str) -> None:
    """Execute the movement

    Args:
        board: the current board
        col: colum of movement
        row: row of movement
        player: color represents the player

    Return:
        None, update the board with the color
    """
    board[row][col] = player

    print("check player and board: ", player, board)


# def parse_example_input()


def check_winning():
    # if end game update game_finish to true
    return False


def parse_matchdata(dataset: List[List[str]]) -> Dict[str, List[str]]:
    """Parse the matchdata to dictionary

    This function helps to parse the matchdata into dictionary format.
    It returns the dictionary with players as key and match movement as values.
    e.g.
        match_dict = {
            "player_8 player_4":
                ['R3', 'B6', 'R2', 'B3', 'R3', 'B7', 'R5'...]
        }

    Args:
        dataset: matchdata.txt dataset in list format

    Return:
        dictionary of matchdata
    """
    players = []
    movement = []
    match_dict = {}

    for data in dataset:
        if len(data) == 2:
            # make the player A and B as key for the match dictionary
            players.append(f"{data[0]} {data[1]}")
        else:
            # simply append the movement
            movement.append(data)

    # the dataset is ordered by the players with their movement
    # loop over two list to create a dictionary
    for i in range(len(players)):
        match_dict[players[i]] = movement[i]

    return match_dict


def play_match(players: str, movements: List[str]) -> None:

    print("check players: ", players)
    print("movement: ", movements)
    # create a new board

    board = creat_board()
    game_finish = False

    while not game_finish:
        player1, player2 = players.split(" ")

        for movement in movements:
            turn = 0
            if turn == 0:
                # player 1 play
                execute(board=board, col=int(movement[-1]) - 1, row=1, player=player1)
                check_winning()
            else:
                # player 2 play
                execute(board=board, col=int(movement[-1]) - 1, row=1, player=player2)
                check_winning()
            turn += 1
            turn = turn % 2


def run():

    # read the match data
    f = open(MATCH_DATA_PATH)
    # format the input data and remove the blank line
    data_list = [item.split(",") for item in f.read().splitlines() if item != ""]

    # parse the matchdata to dictionary
    match_dict = parse_matchdata(data_list)

    game_list = match_dict.keys()

    for game in game_list:
        play_match(players=game, movement=match_dict[game])

    return []


if __name__ == "__main__":
    run()
