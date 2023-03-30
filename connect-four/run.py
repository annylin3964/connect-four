from functions import parse_matchdata, play_match, BOARD_COL, BOARD_ROW, parse_2
from constants import MATCH_DATA_PATH
import numpy as np


def creat_board():
    """create the empty board"""
    col = [-1 for _ in range(BOARD_COL)]
    board = [ col for _ in range(BOARD_ROW)]
    return board

def run():

    # read the match data
    f = open(MATCH_DATA_PATH)
    # format the input data and remove the blank line
    data_list = [ln for ln in f.read().splitlines() if ln != ""]
    print(data_list)
    player_dict = parse_2(dataset=data_list)

    # parse the matchdata to dictionary
    player_list, movement_list = parse_matchdata(data_list)

    winner_list = []
    # for num in range(len(player_list)):
    #     board = creat_board()
    #     winner = play_match(player_list[num], movement_list[num], board=board)
    #     winner_list.append(winner)

    for players in player_dict.keys():

        if len(player_dict[players]) ==1:
            board = creat_board()
          #  print("movement: ", player_dict[players])
            print("see another here: ", player_dict[players])
            winner = play_match(players=players,movements=player_dict[players], board=board)
            winner_list.append(winner)
        else:
            print("len of player dict: ", len(player_dict[players]))
            for match_num in range(len(player_dict[players])):
                board = creat_board()
                print("see the dictionary here: ", player_dict[players][match_num])
                winner = play_match(players=players,movements=player_dict[players][match_num],board=board)
                winner_list.append(winner)

    print("final winner list: ", sorted(winner_list))


if __name__ == "__main__":
    run()
