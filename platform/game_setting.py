from pygame.locals import *
import pygame
import math
import random
import sys
import keyboard
import time
import os

pygame.init()
pygame.mixer.init()

print(os.getcwd())

###############
# Game Images #
###############

NUMBER_OF_MAP = 1
NUMBER_OF_POSITIONS = 7
MAP_NUMBER = random.randint(1, NUMBER_OF_MAP)
MAZE_TEXT = 'maps/map0{0}.jpg'
#MAZE = pygame.image.load(MAZE_TEXT.format(str(MAP_NUMBER)))
MAZE = pygame.image.load("maps/mapempty.jpg")
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

CONTROL_TANK1 = ('up', 'down', 'right', 'left', pygame.K_SLASH)
CONTROL_TANK2 = ('w', 's', 'd', 'a', pygame.K_TAB)
CONTROL_TANK3 = ('u', 'j', 'k', 'h', pygame.K_SPACE)

#################
# Game Settings #
#################

WIDTH_ORIG, HEIGHT_ORIG = 1171, 700
WIDTH, HEIGHT = 1004, 600
GAME_OVER_TIME = 5
EXPLOSION_TIME = 2
GAME_IS_RUNNING = 1
GAME_TITLE = "Alter Tank"
ARC_ANGLE = 22.5*(math.pi/180)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BALL_RADIUS = 5
BALL_LIFE = 10
BALL_COUNT = 5
TANK_RADIUS = 20

###################
# speeds Settings #
###################

ROTATION_DEGREE = 5
MOVEMENT_DEGREE = 4
BALL_SPEED = 12

################
# Black window #
################

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()

################
# transform im #
################


START_MENU_IMG = pygame.transform.scale(START_MENU_IMG, (int(WIDTH * START_MENU_IMG.get_width() / WIDTH_ORIG), int(HEIGHT * START_MENU_IMG.get_height() / HEIGHT_ORIG)))
HELP_3PLAYER = pygame.transform.scale(HELP_3PLAYER, (int(WIDTH * HELP_3PLAYER.get_width() / WIDTH_ORIG), int(HEIGHT * HELP_3PLAYER.get_height() / HEIGHT_ORIG)))
HELP_2PLAYER = pygame.transform.scale(HELP_2PLAYER, (int(WIDTH * HELP_2PLAYER.get_width() / WIDTH_ORIG), int(HEIGHT * HELP_2PLAYER.get_height() / HEIGHT_ORIG)))
IMG_TANK1 = pygame.transform.scale(IMG_TANK1, (int(WIDTH * IMG_TANK1.get_width() / WIDTH_ORIG), int(HEIGHT * IMG_TANK1.get_height() / HEIGHT_ORIG)))
IMG_TANK2 = pygame.transform.scale(IMG_TANK2, (int(WIDTH * IMG_TANK2.get_width() / WIDTH_ORIG), int(HEIGHT * IMG_TANK2.get_height() / HEIGHT_ORIG)))
IMG_TANK3 = pygame.transform.scale(IMG_TANK3, (int(WIDTH * IMG_TANK3.get_width() / WIDTH_ORIG), int(HEIGHT * IMG_TANK3.get_height() / HEIGHT_ORIG)))
SCORE_FRAME_2player = pygame.transform.scale(SCORE_FRAME_2player, (int(WIDTH * SCORE_FRAME_2player.get_width() / WIDTH_ORIG), int(HEIGHT * SCORE_FRAME_2player.get_height() / HEIGHT_ORIG)))
SCORE_FRAME_3player = pygame.transform.scale(SCORE_FRAME_3player, (int(WIDTH * SCORE_FRAME_3player.get_width() / WIDTH_ORIG), int(HEIGHT * SCORE_FRAME_3player.get_height() / HEIGHT_ORIG)))
IMG_EXPLOSION = pygame.transform.scale(IMG_EXPLOSION, (int(WIDTH * IMG_EXPLOSION.get_width() / WIDTH_ORIG), int(HEIGHT * IMG_EXPLOSION.get_height() / HEIGHT_ORIG)))
MAZE = pygame.transform.scale(MAZE, (int(WIDTH * MAZE.get_width() / WIDTH_ORIG), int(HEIGHT * MAZE.get_height() / HEIGHT_ORIG)))

