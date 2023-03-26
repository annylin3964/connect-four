import pathlib
from typing import Dict, List, Any

import numpy as np


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

    board[row][col] = int(player[-1])

    print("check player and board: ", player, "\n", board)


def check_winning(board: List[str], player: str) -> bool:
    # get player number
    player_num = int(player[-1])
    # check the vertical is winning or not
    for c in range(BOARD_COL - 3):
        for r in range(BOARD_ROW):
            if sum(board[r][c : c + 3]) == player_num * 4:
                print(f"PLAYER {player_num} WIN!!!!")
                return True
    print("vertical check finish!")
    # chec the horizontal is winning or not
    for c in range(BOARD_COL):
        for r in range(BOARD_ROW - 3):
            check_sum = (
                board[r][c] + board[r + 1][c] + board[r + 2][c] + board[r + 3][c]
            )
            if check_sum == player_num * 4:
                print(f"PLAYER {player_num} WIN!!!!")
                return True

    print("horizontal check finish!")

    # Check positively sloped diaganols
    for c in range(BOARD_COL - 3):
        for r in range(BOARD_ROW - 3):
            check_sum = (
                board[r][c]
                + board[r + 1][c + 1]
                + board[r + 2][c + 2]
                + board[r + 3][c + 3]
            )
            if check_sum == player_num * 4:
                return True
    print("positively sloped diaganols check finish!")
    # Check negatively sloped diaganols
    for c in range(BOARD_COL - 3):
        for r in range(3, BOARD_ROW):
            check_sum = (
                board[r][c]
                + board[r - 1][c + 1]
                + board[r - 2][c + 2]
                + board[r - 3][c + 3]
            )
            if check_sum == player_num * 4:
                return True

    print("negatively sloped diaganols check finish!")


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
    for i in range(BOARD_ROW):
        if board[i][col] == 0:
            return i


def play_match(players: str, movements: List[str]) -> None:

    print("check players: ", players)
    print("movement: ", movements)
    # create a new board

    board = creat_board()
    game_finish = False

    while not game_finish:
        player1, player2 = players.split(" ")
        turn = 0
        for movement in movements:
            if turn == 0:
                # player 1 play
                # get the column of the move
                execute_column = int(movement[-1]) - 1
                execute(
                    board=board,
                    col=execute_column,
                    row=get_next_available_row(board=board, col=execute_column),
                    player=player1,
                )
                game_finish = check_winning(board=board, player=player1)
            else:
                # player 2 play
                # get the column of the move
                execute_column = int(movement[-1]) - 1
                execute(
                    board=board,
                    col=execute_column,
                    row=get_next_available_row(board=board, col=execute_column),
                    player=player2,
                )
                game_finish = check_winning(board=board, player=player2)
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
        play_match(players=game, movements=match_dict[game])

    return []


if __name__ == "__main__":
    run()
