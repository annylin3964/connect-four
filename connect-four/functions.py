import logging
from typing import Any, Dict, List
import pandas as pd
import subprocess

from google.cloud.sql.connector import Connector
import sqlalchemy

from constants import (
    BOARD_COL,
    BOARD_ROW,
    MAXIMUM_MOVE,
    PROJECT_ID,
    REGION,
    INSTANCE_NAME,
    DB_NAME,
    DB_PASS,
    DB_USER,
    INSTANCE_CONNECTION_NAME,
    ROLE,
    DB_TABLE_NAME,
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# initialize Connector object
connector = Connector()


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


def result_analysis(
    winner_list: List[str], games_data: Dict[str, List]
) -> pd.DataFrame:
    """Analyse the results

    This function generates overview of the gamaes. It ingests the winner list
    and the matchdata to calculate the following information:
    
    1. player_rank: player rank based on the win%
    2. games_played: number of games player played
    3. won: number of games the player won
    4. lost: number of games the player lost
    5. win%: the percentage of won games

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

    # convert the winning and played dictionary into dataframe
    winning_df = pd.DataFrame.from_dict(player_dict, orient="index", columns=["won"])
    played_df = pd.DataFrame.from_dict(
        player_played_dict, orient="index", columns=["games_played"]
    )
    # merged two dfs
    result_df = winning_df.join(played_df)
    result_df = result_df.reset_index()

    # calculate the number of lost games for players
    result_df["lost"] = result_df["games_played"] - result_df["won"]

    # the games of win in percentage
    result_df["win%"] = round(result_df["won"] / result_df["games_played"], 3) * 100

    # create the ranking based on the win%, if the players have same ranking, use
    # the number of higest rank for them
    result_df["player_rank"] = result_df["won"].rank(ascending=False, method="min")
    print(result_df)
    # sort the result dataframe, rename the column and reset index
    result_df = (
        result_df.sort_values(by=["player_rank"])
        .rename(columns={"index": "player_id"})
        .reset_index()
        .drop(columns=["index"])
    )

    logging.info(f"Check the result_df\n {result_df}")

    return result_df


def gcloud_db_setup() -> None:
    """
    """

    subprocess.run(
        [
            "gcloud",
            "projects",
            "add-iam-policy-binding",
            f"{PROJECT_ID}",
            f"--member=user:{DB_USER}",
            f"--role={ROLE}",
        ]
    )

    # enable cridentials
    subprocess.run(["gcloud", "services", "enable", "sqladmin.googleapis.com"])

    # create database
    subprocess.run(
        [
            "gcloud",
            "sql",
            "databases",
            "create",
            f"{DB_NAME}",
            f"--instance={INSTANCE_NAME}",
        ]
    )

    # create database user
    subprocess.run(
        [
            "gcloud",
            "sql",
            "users",
            "create",
            DB_USER,
            f"--instance={INSTANCE_NAME}",
            f"--password={DB_PASS}",
        ]
    )

    # configuring credentials
    subprocess.run(["gcloud", "auth", "application-default", "login"])


def getconn():
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME, "pg8000", user=DB_USER, password=DB_PASS, db=DB_NAME
    )
    return conn


def insert_result_to_db(result_df: pd.DataFrame) -> None:
    """Insert the analyses result to database
    
    """
    pool = sqlalchemy.create_engine(
        "postgresql+pg8000://", creator=getconn, future=True,
    )
    # connect to connection pool
    with pool.connect() as db_conn:
        # create ratings table in our sandwiches database
        db_conn.execute(
            sqlalchemy.text(
                f"CREATE TABLE IF NOT EXISTS {DB_TABLE_NAME} "
                "( id SERIAL NOT NULL, player_id VARCHAR(255) NOT NULL, "
                "player_rank FLOAT NOT NULL, games_played INT NOT NULL, "
                "won INT NOT NULL, lost INT NOT NULL, "
                "win_per FLOAT NOT NULL, PRIMARY KEY (id));"
            )
        )

        db_conn.commit()

        # insert data into our ratings table

        # insert entries into table
        for i in range(len(result_df)):
            insert_stmt = sqlalchemy.text(
                f"INSERT INTO {DB_TABLE_NAME} (player_rank, player_id, games_played, won, lost, win_per) VALUES (:player_rank, :player_id,:games_played,:won,:lost,:win_per)",
            )
            # db_conn.execute(insert_stmt, parameters={"player_id": result_df.loc[i]["player_id"]})
            # db_conn.execute(insert_stmt, parameters={"player_rank": result_df.loc[i]["player_rank"]})
            # db_conn.execute(insert_stmt, parameters={"win%": result_df.loc[i]["win%"]})
            # db_conn.execute(insert_stmt, parameters={"games_played": result_df.loc[i]["games_played"]})
            # db_conn.execute(insert_stmt, parameters={"won": result_df.loc[i]["won"]})
            # db_conn.execute(insert_stmt, parameters={"lost": result_df.loc[i]["lost"]})

            db_conn.execute(
                insert_stmt,
                parameters={
                    "player_id": result_df.loc[i]["player_id"],
                    "player_rank": result_df.loc[i]["player_rank"],
                    "win_per": result_df.loc[i]["win%"],
                    "games_played": result_df.loc[i]["games_played"],
                    "won": result_df.loc[i]["won"],
                    "lost": result_df.loc[i]["lost"],
                },
            )
            db_conn.commit()

        # query and fetch ratings table
        results = db_conn.execute(
            sqlalchemy.text(f"SELECT * FROM {DB_TABLE_NAME}")
        ).fetchall()

        # show results
        for row in results:
            logger.info(row)
