import pathlib
from typing import List, Any
import numpy as np

from functions import MATCH_DATA_PATH, parse_matchdata, play_match


def run():

    # read the match data
    f = open(MATCH_DATA_PATH)
    # format the input data and remove the blank line
    data_list = [item.split(",") for item in f.read().splitlines() if item != ""]

    # parse the matchdata to dictionary
    player_list, movement_list = parse_matchdata(data_list)

    winner_list = []
    for num in range(len(player_list)):
        winner = play_match(players=player_list[num], movements=movement_list[num])
        winner_list.append(winner)

    print("final winner list: ", len(winner_list))


if __name__ == "__main__":
    run()
