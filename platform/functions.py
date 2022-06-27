import pygame

from game_setting import *
from display import draw_score, draw_text


##################
# Game Functions #
##################


def wall_collision(point):
    global MAZE
    pixel_rgb = get_color(MAZE, point)
    if 85 > pixel_rgb[0] > 70:
        return True


def get_color(surface, position):
    position = list(position)
    position[0] = min(max(position[0], 0), HEIGHT - 1)
    position[1] = min(max(position[1], 0), WIDTH - 1)
    position = tuple(position)
    col = surface.get_at(position)
    return col.r, col.g, col.b


def check_victory(tanks):
    team_list = set()
    for tank in tanks:
        if tank.get_exist():
            team_list.add(tank.get_team())
    if len(team_list) > 1:
        return False
    return True

def check_boom(ball, tank):
    passing_time = time.time() - ball.get_time()
    if passing_time > PASSING_TIME:
        if ((abs(ball.get_center_location()[0] - tank.get_location()[0])) ** 2 + (
        abs(ball.get_center_location()[1] - tank.get_location()[1])) ** 2) ** 0.5 <= BALL_RADIUS + TANK_RADIUS:
            return True
    return False


def play_sound(sound):
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play(0)


def help_player(n_players):
    screen.blit(HELP_IMAGES[n_players], (0, 0))
    pygame.display.update()

    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                break
        elif ev.type == pygame.QUIT:
            pygame.quit()
            quit()
        else:
            draw_text(screen, "Press [ENTER] To Begin", BLACK, 30, (WIDTH / 2, (HEIGHT / 2) + 200))
            pygame.display.update()

    screen.fill(BLACK)
    draw_text(screen, "GET READY!", WHITE, 40, (WIDTH / 2, HEIGHT / 2))
    pygame.display.update()


def get_possible_positions(number):
    final_random_positions = []
    map_positions = list(TANK_POSSIBLE_POSITIONS)

    for i in range(NUMBER_OF_POSITIONS):
        map_positions[i] = list(map_positions[i])

    for i in range(number):
        random_index = random.randint(0, len(map_positions) - 1)
        final_random_positions.append(map_positions[random_index])
        map_positions.pop(random_index)

    return final_random_positions
