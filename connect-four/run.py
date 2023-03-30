from typing import List

from constants import MATCH_DATA_PATH
from functions import creat_board, parse_matchdata, play_match


def run():

    # read the match data
    f = open(MATCH_DATA_PATH)
    # format the input data and remove the blank line
    data_list = [ln for ln in f.read().splitlines() if ln != ""]
    player_dict = parse_matchdata(dataset=data_list)

    winner_list: List[int] = []

    for players, matches in player_dict.items():
        for match in matches:
            # initia
            board = creat_board()
            winner = play_match(players=players, movements=match, board=board)
            winner_list.append(winner)

    print("final winner list: ", sorted(winner_list))


if __name__ == "__main__":
    run()
