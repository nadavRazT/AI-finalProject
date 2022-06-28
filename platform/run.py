import argparse
from functions import *
from game_engine import main_menu, initilize_game
from tank import TankFactory



def main():
    parser = argparse.ArgumentParser(description='initilize game')
    parser.add_argument("-n", "--n_manual", help='num of manual players', default=0)
    parser.add_argument("-d", "--display", help='use display', type=bool,default=False)
    parser.add_argument('-t','--teams', nargs='+', help='<Required> Set flag')
    parser.add_argument("-r", "--rounds", default=2, help='number of rounds', type=int)


    args = parser.parse_args()
    n_manual = int(args.n_manual)
    teams = [int(t) for t in args.teams]
    if len(teams) == 1:
        print("need someone to fight")
        exit()
    TF = TankFactory(n_manual, teams)
    tank_list = TF.get_tanks()
    score = initilize_game(tank_list, args.rounds, len(teams), n_manual, args.display)
    print(score)


if __name__ == "__main__":
    main()
