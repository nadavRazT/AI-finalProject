from enum import Enum

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
    def __init__(self, game, tank_list, ball_list):
        self.tank_list = tank_list
        self.ball_list = ball_list
        self.map_matrix = game.get_map()

    def get_successor(self, action):

