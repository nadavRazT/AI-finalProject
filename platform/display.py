import pygame
from game_setting import *


def draw_text(surf, text, color, size, location):
    ## selecting a cross platform font to display the score
    font = pygame.font.Font('freesansbold.ttf', size)
    text_surface = font.render(text, True, color)       ## True denotes the font to be anti-aliased
    text_rect = text_surface.get_rect()
    text_rect.midtop = location
    surf.blit(text_surface, text_rect)

def draw_score(color ,score):
    if color == "Red":
        location = (849,86)
    if color == "Green" :
        location = (849,236)
    if color == "Blue" :
        location = (849,386)
    if color =="Yellow":
        location = (849, 536)
    draw_text(screen, score, BLACK, 60, location)
