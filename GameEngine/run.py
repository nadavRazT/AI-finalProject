import argparse
from functions import *
# from game_engine import main_menu, initilize_game
from tank import TankFactory
from game import Game
from functools import reduce


def run_game(n_rounds, tanks, display, map_index, n_teams):
    scores = []

    new_game = Game(tanks, display, map_index, n_teams, n_rounds)
    score = new_game.run()

    print(f"---------------\n"
          f"total results: \n"
          f"{score}")
    return


def main():
    parser = argparse.ArgumentParser(description='initilize game')
    parser.add_argument("-n", "--n_manual", help='num of manual players', type=int, default=0)
    parser.add_argument("-m", "--map_index", help='index of map', type=int, default=0)
    parser.add_argument("-d", "--display", help='use display', type=bool, default=False)
    parser.add_argument('-t', '--teams', nargs='+', help='<Required> Set flag')
    parser.add_argument("-r", "--rounds", default=2, help='number of rounds', type=int)

    args = parser.parse_args()
    n_manual = int(args.n_manual)
    teams = {group_colors[t]: int(args.teams[t]) for t in range(len(args.teams))}
    if len(teams) == 1:
        print("need someone to fight")
        exit()
    TF = TankFactory(n_manual, teams)
    tank_list = TF.get_tanks()
    run_game(args.rounds, tank_list, args.display, args.map_index, len(teams))


if __name__ == "__main__":
    main()
