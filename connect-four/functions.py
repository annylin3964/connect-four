import pathlib
from typing import Any, List, Dict
from google.cloud import storage
from constants import BOARD_COL, BOARD_ROW
import numpy as np
import logging

logger = logging.getLogger()





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
    board[row][col] = int(player)


def check_winning(board: List[str], player: str) -> bool:
    # get player number
    player_num = int(player)
    # check the vertical is winning or not
    for c in range(BOARD_COL - 3):
        for r in range(BOARD_ROW):
            mask = (
                board[r][c]
                == board[r][c + 1]
                == board[r][c + 2]
                == board[r][c + 3]
                == player_num
            )
            if mask:
                print(f"PLAYER {player_num} WIN!!!!")
                return True
    # chec the horizontal is winning or not
    for c in range(BOARD_COL):
        for r in range(BOARD_ROW - 3):
            mask = (
                board[r][c]
                == board[r + 1][c]
                == board[r + 2][c]
                == board[r + 3][c]
                == player_num
            )
            if mask:
                print(f"PLAYER {player_num} WIN!!!!")
                return True

    # Check positively sloped diaganols
    for c in range(BOARD_COL - 3):
        for r in range(BOARD_ROW - 3):
            mask = (
                board[r][c]
                == board[r + 1][c + 1]
                == board[r + 2][c + 2]
                == board[r + 3][c + 3]
                == player_num
            )
            if mask:
                print(f"PLAYER {player_num} WIN!!!!")
                return True

    # Check negatively sloped diaganols
    for c in range(BOARD_COL - 3):
        for r in range(3, BOARD_ROW):
            mask = (
                board[r][c]
                == board[r - 1][c + 1]
                == board[r - 2][c + 2]
                == board[r - 3][c + 3]
                == player_num
            )
            if mask:
                print(f"PLAYER {player_num} WIN!!!!")
                return True


def parse_matchdata(dataset: List[List[str]]) -> List:
    """Parse the matchdata to dictionary
    This function helps to parse the matchdata into two lists.
    One is for the players and another one is for the movement, given
    the order won't be altered, simply return two lists.

    Args:
        dataset: matchdata.txt dataset in list format
    Return:
        players list and movement list
    """
    players = []
    movement = []

    for data in dataset:
        if len(data) == 2:
            # make the player A and B as key for the match dictionary
            player1 = data[0].split("_")[-1]
            player2 = data[1].split("_")[-1]
            players.append(f"{player1} {player2}")
        else:
            # simply append the movement
            movement.append(data)

    return players, movement


def parse_2(dataset: List[List[str]]) -> List:
    players = []
    movement = []
    match_dict: Dict(List[str]) = {}

    for data in dataset:
        if len(data.split(",")) ==2:
            # make the player A and B as key for the match dictionary
            player1,player2 = data.split(",")
            player1 = player1.split("_")[-1]
            player2 = player2.split("_")[-1]
            players.append(f"{player1} {player2}")
        else:
            # simply append the movement
            movement.append(data.split(","))
   # print("see movemment after", movement)
    match_dict = {i:[] for i in set(players)}
    for i in range(len(movement)):
        match_dict[players[i]].append(movement[i])
    return match_dict


def get_next_available_row(board: List[Any], col: int) -> int:
    """Get the next available row of the column

    Loop over the row to see which is the empty cell to insert.
    If there is no empty cell for all the row, raise an error.

    Args:
        board: current board status
        col: col of the board need to get the available row
    Return:
        available row position
    """
    for i in range(BOARD_ROW):
        if board[i][col] == -1:
            return i
        else:
            raise ValueError(f"No available next row, check the current board: {board}")


def play_match(players: str, movements: List[str], board: List[int]) -> int:

    game_finish = False

    while not game_finish:
        player1, player2 = players.split(" ")
        turn = 0
        for number, movement in enumerate(movements):
            print("see movement: ", movement)
            if turn == 0:
                # player 1 play
                # get the column of the move
                execute_column = int(movement[-1]) - 1
                execute(
                    board=board,
                    col=execute_column,
                    row=get_next_available_row(board, execute_column),
                    player=player1,
                )
                game_finish = check_winning(board, player1)
                if game_finish is True:
                    return player1
            else:
                # player 2 play
                # get the column of the move
                execute_column = int(movement[-1]) - 1
                execute(
                    board=board,
                    col=execute_column,
                    row=get_next_available_row(board, execute_column),
                    player=player2,
                )
                game_finish = check_winning(board, player2)
                if game_finish is True:
                    return player2
            turn += 1
            turn = turn % 2
            if number == 41:
                return "no one win"
