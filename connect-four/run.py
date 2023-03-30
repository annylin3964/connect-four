from typing import List

from constants import MATCH_DATA_PATH
from functions import BOARD_COL, BOARD_ROW, parse_matchdata, play_match


def creat_board():
    """create the empty board"""
    col = [-1 for _ in range(BOARD_COL)]
    board = [col for _ in range(BOARD_ROW)]
    return board


def run():

    # read the match data
    f = open(MATCH_DATA_PATH)
    # format the input data and remove the blank line
    data_list = [ln for ln in f.read().splitlines() if ln != ""]
    player_dict = parse_matchdata(dataset=data_list)

    winner_list: List[int] = []

    for players in player_dict.keys():

        if len(player_dict[players]) == 1:
            board = creat_board()
            winner = play_match(
                players=players, movements=player_dict[players][0], board=board
            )
            winner_list.append(winner)
        else:
            for match_num in range(len(player_dict[players])):
                board = creat_board()
                winner = play_match(
                    players=players,
                    movements=player_dict[players][match_num],
                    board=board,
                )
                winner_list.append(winner)

    print("final winner list: ", sorted(winner_list))


if __name__ == "__main__":
    run()
