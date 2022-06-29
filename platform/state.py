from enum import Enum
import pygame
from game_setting import *
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
    def __init__(self, tank_list, display):
        self.display = display
        self.tank_list = tank_list
        self.ball_list = []
        for tank in tank_list:
            self.ball_list += tank.get_balls()

    def generate_successor(self, actions, display):
        # perform actions
        for action in actions:
            if action.agent.get_exist() == 0:
                continue
            if action.action_type == ActionType.FORWARD:
                action.agent.go(MOVEMENT_DEGREE, display)
            if action.action_type == ActionType.BACKWARD:
                action.agent.go(-1 * MOVEMENT_DEGREE, display)
            if action.action_type == ActionType.RIGHT:
                action.agent.rotate(-1 * ROTATION_DEGREE)
            if action.action_type == ActionType.LEFT:
                action.agent.rotate(ROTATION_DEGREE)
            if action.action_type == ActionType.SHOOT:
                action.agent.shoot()
            if action.action_type == ActionType.STAY:
                continue

        # moving balls
        for tank in self.tank_list:
            for ball in tank.get_balls():
                ball.go(BALL_SPEED, display)
            tank.check_balls()

    # checking tank - ball collision
        for ball in self.ball_list:
            for tank in self.tank_list:
                if check_boom(ball, tank) and tank.get_exist() and not ball.to_kill:
                    display.play_sound(EXPLOSION_SOUND)
                    tank.destroy()
                    ball.get_tank().update_kills()
                    for shooting_tank in self.tank_list:
                        shooting_tank.poping_ball(ball)

        return State(self.tank_list, display)


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
        for tank in self.tank_list:
            if tank.color not in ret.keys():
                ret[tank.color] = 0
            if tank.get_exist():
                ret[tank.color] += tank.num_kills_round
        return ret

    def get_features(self, agent, state):
        return

    def get_reward(self, agent, state):
        return

    def get_enemy_cone(self):
        return boolean_list, distance_list

    def get_team_cone(self):
        return boolean_list, distance_list

    def get_ball_cone(self):
        return boolean_list, distance_list

