import pygame
from game_setting import *
from display import draw_score, draw_text

from tank import *

### param ###

def main_menu():
    screen.blit(START_MENU_IMG, (0,0))
    pygame.display.update()
    n = ""
    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                break
            if ev.unicode.isdigit():
                n += pygame.key.name(ev.key)
            elif ev.key == pygame.K_q:
                pygame.quit()
                quit()
        elif ev.type == pygame.QUIT:
            pygame.quit()
            quit()
        else:
            draw_text(screen, "type number of players press ENTER", BLACK, 30, (WIDTH/2, HEIGHT/2))
            draw_text(screen, "press [Q] To Quit",BLACK, 30, (WIDTH/2, (HEIGHT/2)+40))
            pygame.display.update()
    n = int(n)
    pygame.display.update()
    return n

def initilize_game(tank_list, n_rounds, n_teams, n_manual):

    player_numbers = len(tank_list)

    for tank in tank_list:
        tank.reset_balls()
    help_player(n_manual)
    pygame.time.wait(1000)
    for round in range(n_rounds):
        score = main_loop(tank_list, player_numbers, n_teams)
    return score


def main_loop(tank_list ,player_numbers, n_teams):


    ending_time = -1

    while GAME_IS_RUNNING:
        if check_victory(tank_list):
            if ending_time == -1:
                ending_time = time.time()
            if time.time() - ending_time > GAME_OVER_TIME:
                for tank in tank_list:
                    if tank.get_exist():
                        tank.add_score() ## check if number of living or kills
                    draw_score(tank.color, str(tank.get_score()))
                    tank.is_exist = 1
                pygame.time.wait(1000)
                return {tank.color: tank.get_score() for tank in tank_list}

        screen.blit(MAZE, (0, 0))
        screen.blit(SCORE_IMAGES[n_teams], (HEIGHT, 0))


        ##########
        # Events #
        ##########

        ball_list = []
        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            for tank in tank_list:
                tank.shoot_control(event)

        for tank in tank_list:
            ball_list += tank.get_balls()

        for ball in ball_list:
            for tank in tank_list:
                if check_boom(ball, tank) and tank.get_exist() and not ball.to_kill:
                    tank.is_exist = 0
                    play_sound(EXPLOSION_SOUND)
                    tank.destroy()
                    for shooting_tank in tank_list:
                        shooting_tank.poping_ball(ball)
                    player_numbers -= 1

        for tank in tank_list:
            if tank.get_exist():
                tank.move_control()
                tank.build()
            elif time.time() - tank.get_death_time() < EXPLOSION_TIME:
                tank.build()

            for ball in tank.get_balls():
                ball.go(BALL_SPEED)
                ball.draw_ball()
            tank.check_balls()

        for tank in tank_list:
            draw_score(tank.color, str(tank.get_score()))

        clock.tick(60)
        pygame.display.update()



def reset_map():
    map_index = random.randint(1, NUMBER_OF_MAP)
    return pygame.image.load(MAZE_TEXT.format(str(map_index)))

