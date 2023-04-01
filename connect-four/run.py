from typing import List

from constants import MATCH_DATA_PATH
from functions import creat_board, parse_matchdata, play_match, result_analysis
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def run():

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
            winner = play_match(players=players, movements=match, board=board)
            winner_list.append(winner)

    ("final winner list: ", sorted(winner_list))

    result_analysis(winner_list=winner_list, games_data=match_dict)


if __name__ == "__main__":
    run()
