from enum import Enum
import pygame
from game_setting import *
from display import draw_score, draw_text
from tank import *
from functions import *

class ActionType(Enum):
    FORWARD = 0
    BACKWARD = 1
    RIGHT = 2
    LEFT = 3
    SHOOT = 4
    STAY = 5

class Action:
    def __init__(self, agent, action_type):
        self.agent = agent
        self.action_type = action_type

class State:
    def __init__(self, tank_list):
        self.tank_list = tank_list

    def generate_successor(self, actions):
        # perform actions
        for action in actions:
            if action.agent.get_exist() == 0:
                continue
            if action.action_type == ActionType.FORWARD:
                action.agent.go(game_setting.MOVEMENT_DEGREE)
            if action.action_type == ActionType.BACKWARD:
                action.agent.go(-1 * game_setting.MOVEMENT_DEGREE)
            if action.action_type == ActionType.RIGHT:
                action.agent.rotate(-1 * game_setting.ROTATION_DEGREE)
            if action.action_type == ActionType.LEFT:
                action.agent.rotate(game_setting.ROTATION_DEGREE)
            if action.action_type == ActionType.SHOOT:
                action.agent.shoot()
            if action.action_type == ActionType.STAY:
                continue

        # moving balls
        for tank in self.tank_list:
            for ball in tank.get_balls():
                ball.go(game_setting.BALL_SPEED)

        # checking tank - ball collision
        for ball in ball_list:
            for tank in tank_list:
                if functions.check_boom(ball, tank) and tank.get_exist() and not ball.to_kill:
                    if display:
                        play_sound(EXPLOSION_SOUND)
                    tank.destroy()
                    for shooting_tank in tank_list:
                        shooting_tank.poping_ball(ball)

        return State(self.tank_list)


    def is_terminal(self):
        team_list = set()
        for tank in self.tank_list:
            if tank.get_exist():
                team_list.add(tank.get_team())
        if len(team_list) > 1:
            return False
        return True

    def get_tanks(self):
        return self.tank_list

    def get_score(self):
        ret = dict()
        for color in game_setting.team_colors:
            ret[color] = 0
        return ret
