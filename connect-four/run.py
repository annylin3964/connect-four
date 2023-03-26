import pathlib
from typing import Dict, List, Any

import numpy as np


ROW_NUM = 6
BOARD_ROW = [-1 for _ in range(ROW_NUM)]
COL_NUM = 7
CURRENT_FOLDER = pathlib.Path(__file__).parent
MATCH_DATA_PATH = CURRENT_FOLDER / "matchdata.txt"


def creat_board():
    """create the empty board"""
    board = [BOARD_ROW for _ in range(COL_NUM)]
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


def check_winning(board: List[str], player: str) -> int:

    # check the vertical is winning or not
    for c in range(COL_NUM - 3):
        for r in range(ROW_NUM):
            mask = (
                board[r][c] == player
                and board[r][c + 1] == player
                and board[r][c + 2] == player
                and board[r][c + 3] == player
            )
            if mask:
                print(f"{player} WIN!!!!")
                print(board)
                return player
    # chec the horizontal is winning or not
    for c in range(COL_NUM):
        for r in range(ROW_NUM - 3):
            mask = (
                board[r][c] == player
                and board[r + 1][c] == player
                and board[r + 2][c] == player
                and board[r + 3][c] == player
            )
            if mask:
                print(f"{player} WIN!!!!")
                print(board)
                return player

    # Check positively sloped diaganols
    for c in range(COL_NUM - 3):
        for r in range(ROW_NUM - 3):
            mask = (
                board[r][c] == player
                and board[r + 1][c + 1] == player
                and board[r + 2][c + 2] == player
                and board[r + 3][c + 3] == player
            )
            if mask:
                print(f"{player} WIN!!!!")
                print(board)
                return player

    # Check negatively sloped diaganols
    for c in range(COL_NUM - 3):
        for r in range(3, ROW_NUM):
            mask = (
                board[r][c] == player
                and board[r - 1][c + 1] == player
                and board[r - 2][c + 2] == player
                and board[r - 3][c + 3] == player
            )
            if mask:
                print(f"{player} WIN!!!!")
                print(board)
                return player


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


def get_next_available_row(board: List[Any], col: int) -> int:
    """Get the next available row of the column

    Args:
        board: current board status
        col: col of the board need to get the available row

    Return:
        available row position

    """

    for i in range(ROW_NUM):
        if board[i][col] == -1:
            return i


def play_match(players: str, movements: List[str]) -> str:

    # create a new board

    board = creat_board()

    player1, player2 = players.split(" ")
    turn = 0
    print(player1, player2)
    for movement in movements:
        execute_column = int(movement[-1]) - 1
        if turn == 0:
            # player 1 play
            # get the column of the move
            execute(
                board=board,
                col=execute_column,
                row=get_next_available_row(board=board, col=execute_column),
                player=player1,
            )
            game_winner = check_winning(board=board, player=player1)
        else:
            # player 2 play
            # get the column of the move
            execute(
                board=board,
                col=execute_column,
                row=get_next_available_row(board=board, col=execute_column),
                player=player2,
            )
            game_winner = check_winning(board=board, player=player2)
        turn += 1
        turn = turn % 2
        if game_winner:
            return f"Player {game_winner} win"


def run():

    # read the match data
    f = open(MATCH_DATA_PATH)
    # format the input data and remove the blank line
    data_list = [item.split(",") for item in f.read().splitlines() if item != ""]

    # parse the matchdata to dictionary
    match_dict = parse_matchdata(data_list)

    game_list = match_dict.keys()

    for game in game_list:
        winner = play_match(players=game, movements=match_dict[game])
        print(winner)


if __name__ == "__main__":
    run()
