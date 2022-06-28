import pygame
from game_setting import *

class Display:
    def __init__(self, display, map_index, n_teams):
        self.is_display = display
        self.n_teams = n_teams
        self.map_image = self.reset_map(map_index)

        if display:
            pygame.mixer.init()
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption(GAME_TITLE)
            self.clock = pygame.time.Clock()

    def draw_text(self, surf, text, color, size, location):
        ## selecting a cross platform font to display the score
        font = pygame.font.Font('freesansbold.ttf', size)
        text_surface = font.render(text, True, color)       ## True denotes the font to be anti-aliased
        text_rect = text_surface.get_rect()
        text_rect.midtop = location
        surf.blit(text_surface, text_rect)

    def draw_score(self ,scores):
        location = ()
        for color, score in scores.items():
            if color == "Red":
                location = (849,86)
            if color == "Green" :
                location = (849,236)
            if color == "Blue" :
                location = (849,386)
            if color =="Yellow":
                location = (849, 536)
            self.draw_text(self.screen, str(score), BLACK, 60, location)
        return


    def initilize(self, state):
        return None

    def update(self, state):
        if not self.is_display:
            return
        scores = state.get_score()
        self.draw_score(scores)
        # pygame.time.wait(1000)
        self.screen.blit(self.map_image, (0, 0))
        self.screen.blit(SCORE_IMAGES[self.n_teams], (HEIGHT, 0))

        for tank in state.get_tanks():
            if tank.get_exist():
                self.draw_tank(tank)
            elif time.time() - tank.get_death_time() < EXPLOSION_TIME:
                self.draw_tank(tank)

            for ball in tank.get_balls():
                self.draw_ball(ball)

        self.clock.tick(60)
        pygame.display.update()


    def play_sound(self, sound):
        if not self.is_display:
            return
        pygame.mixer.music.load(sound)
        pygame.mixer.music.set_volume(VOLUME)
        pygame.mixer.music.play(0)


    def draw_tank(self, tank):
        self.screen.blit(tank.get_image(), tank.get_rect())

    def draw_ball(self, ball):
        return pygame.draw.circle(self.screen, BLACK, ball.get_center_location(), BALL_RADIUS)

    def reset_map(self, map_index):
        return pygame.image.load(MAZE_TEXT.format(str(map_index)))