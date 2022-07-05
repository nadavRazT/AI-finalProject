from pygame.locals import *
import pygame
import math
import random
import sys
import keyboard
import time
import os

# pygame.init()
# pygame.mixer.init()
#
# print(os.getcwd())

#################
# Game Settings #
#################
VOLUME = 0.1
WIDTH_ORIG, HEIGHT_ORIG = 1171, 700
WIDTH, HEIGHT = 1004, 600
GAME_OVER_TIME = 2
EXPLOSION_TIME = 1
GAME_IS_RUNNING = 1
PASSING_TIME = 0.1
GAME_TITLE = "Alter Tank"
ARC_ANGLE = 22.5 * (math.pi / 180)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BALL_LIFE = 10
BALL_COUNT = 2
TANK_SIZE_FACTOR = 1
BALL_RADIUS = int(5 // TANK_SIZE_FACTOR)
TANK_RADIUS = int(20 // TANK_SIZE_FACTOR)
group_colors = ["Red", "Green", "Blue"]#, "Yellow"]
NUM_OF_CONES = 30
###############
# Game Images #
###############

NUMBER_OF_MAP = 1
NUMBER_OF_POSITIONS = 7
MAP_NUMBER = random.randint(1, NUMBER_OF_MAP)
MAZE_TEXT = 'maps/map0{0}.jpg'
MAZE = pygame.image.load(MAZE_TEXT.format(str(MAP_NUMBER)))
MAZE = pygame.image.load("maps/map00.jpg")
TANK_SCATTER_INDEX = 50
OFFSET_p = HEIGHT - TANK_SCATTER_INDEX - 2 * TANK_RADIUS
OFFSET_m = TANK_SCATTER_INDEX - 2 * TANK_RADIUS
TEAM_START_POSITIONS = {"Red": (OFFSET_m + 50, OFFSET_m + 50),
                        "Green": (OFFSET_m + 50, OFFSET_p ),
                        "Blue": (OFFSET_p + 50, OFFSET_m - 50),
                        "Yellow": (OFFSET_p, OFFSET_p)}

TANK_POSSIBLE_POSITIONS = ((50, 50),
                           (390, 125),
                           (225, 390),
                           (125, 395),
                           (480, 220),
                           (210, 45),
                           (45, 315))

START_MENU_IMG = pygame.image.load('img/START_MENU.png')
HELP_3PLAYER = pygame.image.load('img/3player_help.png')

HELP_2PLAYER = pygame.image.load('img/2player_help.png')

IMG_TANK1 = pygame.image.load('img/tank1.png')
IMG_TANK2 = pygame.image.load('img/tank2.png')
IMG_TANK3 = pygame.image.load('img/tank3.png')

SCORE_FRAME_2player = pygame.image.load('img/score_frame_2player.png')
SCORE_FRAME_3player = pygame.image.load('img/score_frame_3player.png')

IMG_EXPLOSION = pygame.image.load('img/explosion/explosion.png')

###############
# Game Musics #
###############

EXPLOSION_SOUND = 'musics/explosion.mp3'

####################
# Game Controllers #
####################

MANUAL_CONTROL_TANK = [('up', 'down', 'right', 'left', "/"),
                       ('w', 's', 'd', 'a', "Tab"),
                       ('u', 'j', 'k', 'h', "Space")]
MAN_CONTROL = "manual"
NOT_MAN_CONTROL = "not manual"
AI_CONTROL = "AI"
GENETIC_CONTROL = "genetic"
DQN_CONTROL= "dqn"

###################
# speeds Settings #
###################

ROTATION_DEGREE = 3
MOVEMENT_DEGREE = 2
BALL_SPEED = 2
REFRESH_RATE = 100
################
# transform im #
################

START_MENU_IMG = pygame.transform.scale(START_MENU_IMG, (
    int(WIDTH * START_MENU_IMG.get_width() / WIDTH_ORIG), int(HEIGHT * START_MENU_IMG.get_height() / HEIGHT_ORIG)))
HELP_3PLAYER = pygame.transform.scale(HELP_3PLAYER, (

    int(WIDTH * HELP_3PLAYER.get_width() / WIDTH_ORIG), int(HEIGHT * HELP_3PLAYER.get_height() / HEIGHT_ORIG)))
HELP_2PLAYER = pygame.transform.scale(HELP_2PLAYER, (

    int(WIDTH * HELP_2PLAYER.get_width() / WIDTH_ORIG), int(HEIGHT * HELP_2PLAYER.get_height() / HEIGHT_ORIG)))
IMG_TANK1 = pygame.transform.scale(IMG_TANK1, (
    int(WIDTH * IMG_TANK1.get_width() / (TANK_SIZE_FACTOR * WIDTH_ORIG)),
    int(HEIGHT * IMG_TANK1.get_height() / (TANK_SIZE_FACTOR * HEIGHT_ORIG))))

IMG_TANK2 = pygame.transform.scale(IMG_TANK2, (
    int(WIDTH * IMG_TANK2.get_width() / (TANK_SIZE_FACTOR * WIDTH_ORIG)),
    int(HEIGHT * IMG_TANK2.get_height() / (TANK_SIZE_FACTOR * HEIGHT_ORIG))))

IMG_TANK3 = pygame.transform.scale(IMG_TANK3, (
    int(WIDTH * IMG_TANK3.get_width() / (TANK_SIZE_FACTOR * WIDTH_ORIG)),
    int(HEIGHT * IMG_TANK3.get_height() / (TANK_SIZE_FACTOR * HEIGHT_ORIG))))

SCORE_FRAME_2player = pygame.transform.scale(SCORE_FRAME_2player, (
    int(WIDTH * SCORE_FRAME_2player.get_width() / WIDTH_ORIG),
    int(HEIGHT * SCORE_FRAME_2player.get_height() / HEIGHT_ORIG)))

SCORE_FRAME_3player = pygame.transform.scale(SCORE_FRAME_3player, (
    int(WIDTH * SCORE_FRAME_3player.get_width() / WIDTH_ORIG),
    int(HEIGHT * SCORE_FRAME_3player.get_height() / HEIGHT_ORIG)))

IMG_EXPLOSION = pygame.transform.scale(IMG_EXPLOSION, (
    int(WIDTH * IMG_EXPLOSION.get_width() / WIDTH_ORIG), int(HEIGHT * IMG_EXPLOSION.get_height() / HEIGHT_ORIG)))

MAZE = pygame.transform.scale(MAZE, (
    int(WIDTH * MAZE.get_width() / WIDTH_ORIG), int(HEIGHT * MAZE.get_height() / HEIGHT_ORIG)))

TANK_IMAGES = {"Red": IMG_TANK1, "Green": IMG_TANK2, "Blue": IMG_TANK3}
SCORE_IMAGES = {2: SCORE_FRAME_2player, 3: SCORE_FRAME_3player}
HELP_IMAGES = {2: HELP_2PLAYER, 3: HELP_3PLAYER}
MAZE_HEIGHT = MAZE.get_height()
MAZE_WIDTH = MAZE.get_width()