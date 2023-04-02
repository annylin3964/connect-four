import logging
from typing import List

from constants import MATCH_DATA_PATH
from functions import (
    creat_board,
    gcloud_db_setup,
    insert_result_to_db,
    parse_matchdata,
    play_match,
    result_analysis,
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def run():
    """Run the connect four game

    It reads the game information from matchdata.txt executes the game,
    analyses the results of all the matches and writes into database.

    """
    # read the match data
    f = open(MATCH_DATA_PATH)
    # format the input data and remove the blank line
    data_list = [ln for ln in f.read().splitlines() if ln != ""]
    match_dict = parse_matchdata(dataset=data_list)

    winner_list: List[int] = []

    for players, matches in match_dict.items():
        for match in matches:
            # initialize the board
            board = creat_board()
            # play the match and get the winner
            winner = play_match(players=players, movements=match, board=board)
            # append the winner in the winner list
            winner_list.append(winner)

    logger.info(f"Winning list for all the match {sorted(winner_list)}")
    logger.info("Start to analyse the winning results.")
    # get the analyses results in dataframe
    result_df = result_analysis(winner_list=winner_list, games_data=match_dict)

    # now we got all the information we need to insert in Google cloud database
    # setup the gcloud database
    logger.info("Setup the google cloud services")
    gcloud_db_setup()

    logger.info("Writing the results into the database")
    # insert the result to db
    insert_result_to_db(result_df=result_df)

    logger.info("Assessment finish.")

if __name__ == "__main__":
    run()
