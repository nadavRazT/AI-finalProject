import argparse
from functions import *
from game_engine import main_menu, initilize_game
from tank import TankFactory


def main_manual():

    menu_display = True

    while GAME_IS_RUNNING:
        if menu_display:
            number_of_players = main_menu()
            if number_of_players == 2:
                import AlterTank_2player
            elif number_of_players == 3:
                import AlterTank_3player
            pygame.time.wait(1000)
            menu_display = False
        clock.tick(60)
        pygame.display.update()



def main():
    parser = argparse.ArgumentParser(description='initilize game')
    parser.add_argument("-n", "--n_manual", help='num of manual players', default=0)
    parser.add_argument('-t','--teams', nargs='+', help='<Required> Set flag')
    parser.add_argument("-m", "--manual", default=False, help='is manual')
    parser.add_argument("-r", "--rounds", default=2, help='number of rounds', type=int)


    args = parser.parse_args()
    if args.manual:
        main_manual()
    n_manual = int(args.n_manual)
    teams = [int(t) for t in args.teams]
    if len(teams) == 1:
        print("need someone to fight")
        exit()
    TF = TankFactory(n_manual, teams)
    tank_list = TF.get_tanks()
    score = initilize_game(tank_list, args.rounds, len(teams), n_manual)
    print(score)
    # while GAME_IS_RUNNING:
    #     if menu_display:
    #         number_of_players = main_menu()
    #         if number_of_players == 2:
    #             import AlterTank_2player
    #         elif number_of_players == 3:
    #             import AlterTank_3player
    #         pygame.time.wait(1000)
    #         menu_display = False
    #     clock.tick(60)
    #     pygame.display.update()


if __name__ == "__main__":
    main()
