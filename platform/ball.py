from game_setting import HEIGHT, WIDTH
from functions import *


class Ball:

    def __init__(self, x, y, angle, tank):
        self.__yPos = y
        self.__angle = angle
        angle_radian = (self.__angle*(math.pi/180))
        self.__xPos = x - (TANK_RADIUS-BALL_RADIUS+2)*math.cos(angle_radian)
        self.__yPos = y + (TANK_RADIUS-BALL_RADIUS+2)*math.sin(angle_radian)
        self.vertical_move = 0
        self.horizontal_move = 0
        self.__time = time.time()
        self.__points = {}
        self.horizontal_neg = 1
        self.vertical_neg = 1
        self.to_kill = False
        self.shooting_tank = tank

    def go(self, value, display):

        x = int(self.__xPos)
        y = int(self.__yPos)

        self.__points ={
                        "right": (min(x+BALL_RADIUS, WIDTH), min(y+0, HEIGHT)),
                        "top": (min(x+0, WIDTH), min(y+BALL_RADIUS, HEIGHT)),
                        "left": (max(x-BALL_RADIUS, 0), min(y-0, HEIGHT)),
                        "bottom": (min(x-0, WIDTH), max(y-BALL_RADIUS, 0))}

        angle_radian = (self.__angle*(math.pi/180))

        if display.wall_collision(self.__points['right']) or display.wall_collision(self.__points['left']):
            self.horizontal_neg *= -1
            self.to_kill = True
        if display.wall_collision(self.__points['bottom']) or display.wall_collision(self.__points['top']):
            self.vertical_neg *= -1
            self.to_kill = True

        self.horizontal_move = self.horizontal_neg * -value*math.cos(angle_radian)
        self.vertical_move = self.vertical_neg * value*math.sin(angle_radian)

        self.__xPos += self.horizontal_move
        self.__yPos += self.vertical_move

    def get_center_location(self):
        return int(self.__xPos), int(self.__yPos)

    def get_angle(self):
        return self.__angle

    def get_time(self):
        return self.__time


    def get_tank(self):
        return self.shooting_tank