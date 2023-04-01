import logging
from typing import Any, Dict, List
import pandas as pd

from constants import BOARD_COL, BOARD_ROW, MAXIMUM_MOVE

logger = logging.getLogger()
logger.setLevel(logging.INFO)


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
                return True

    return False


def parse_matchdata(dataset: List[List[str]]) -> Dict:
    """Parse the matchdata to dictionary
    This function helps to parse the matchdata into dictionary.
    It stores the players and the movement separately, then create
    the dictionary to store the data. The format looks like:

    match_dict = {
        "player1, player2": [match1, match2, match3],
        "player3, player5": [match1],
        ...
    }

    Args:
        dataset: matchdata.txt dataset in list format
    Return:
        players list and movement list
    """
    players = []
    movement = []
    match_dict: Dict[str, List[str]] = {}

    for data in dataset:
        # check the data is player line or movement line
        if len(data.split(",")) == 2:
            # make the player A and B as key for the match dictionary
            player1, player2 = data.split(",")
            player1 = player1.split("_")[-1]
            player2 = player2.split("_")[-1]
            players.append(f"{player1} {player2}")
        else:
            # simply append the movement
            movement.append(data)

    # initiate the dictionary
    match_dict = {i: [] for i in set(players)}

    # loop over the data and fill the dictionary
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
            raise ValueError(
                "No available next row" f"check the current board: {board}"
            )


def play_match(players: str, movements: str, board: List[int]) -> str:

    game_finish = False

    while not game_finish:
        player1, player2 = players.split(" ")
        turn = 0
        movement_list = movements.split(",")
        if len(movement_list) > MAXIMUM_MOVE:
            raise ValueError(
                f"Number of movement {len(movement_list)} exceed the maximum"
            )
        for movement in movement_list:
            # player 1 play
            # get the column of the movement
            execute_column = int(movement[-1]) - 1

            # validate the execuable column
            if execute_column > 6:
                raise ValueError(f"Execute column {movement[-1]} is not valid")

            if turn == 0:
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


def creat_board():
    """create the empty board"""
    col = [-1 for _ in range(BOARD_COL)]
    board = [col for _ in range(BOARD_ROW)]
    return board


def result_analysis(winner_list: List[str], games_data: Dict[str, List]) -> None:
    """Analyse the results

    Args:
        winner_list: list of winning player number

    player_rank | player_id | games_played | won | lost | win%
    """

    # initiate the full played list for all the players
    full_list = []
    for player, games in games_data.items():
        for _ in games:
            temp_list = player.split(" ")
            full_list.append(temp_list)

    full_list = [player for players in full_list for player in players]

    # create a player played dictionary to store the number of games
    # the given player played
    # add player prefix to prevent the confusion of played number
    player_played_dict = {"player" + i: 0 for i in set(full_list)}
    for p in full_list:
        player_played_dict["player" + p] += 1

    # create a palyer winning dictionary to calculate the results
    # add player prefix to prevent the confusion of winning number
    player_dict = {"player" + i: 0 for i in set(full_list)}
    logger.info(f"chech the full list {player_dict}")

    # loop over the winning list and store to the winner
    for w in winner_list:
        player_dict["player" + w] += 1

    winning_df = pd.DataFrame.from_dict(player_dict, orient="index", columns=["win"])
    played_df = pd.DataFrame.from_dict(
        player_played_dict, orient="index", columns=["games_played"]
    )

    result_df = winning_df.join(played_df)
    result_df = result_df.reset_index()
    result_df["lost"] = result_df["games_played"] - result_df["win"]
    result_df["win%"] = round(result_df["win"] / result_df["games_played"], 3)
    result_df["player_rank"] = result_df["win"].rank(ascending=False, method="min")
    result_df = result_df.sort_values(by=["player_rank"]).reset_index()
    logging.info(f"Check the result_df\n {result_df}")
