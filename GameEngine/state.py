from enum import Enum
import math
import numpy as np
import pygame
from GameEngine.game_setting import *
from GameEngine.tank import *
from GameEngine.functions import *

INFINITY = -1
DIAG = np.sqrt(2) * HEIGHT


class ActionType(Enum):
    FORWARD = 0
    # BACKWARD = 1
    RIGHT = 1
    LEFT = 2
    SHOOT = 3
    STAY = 4


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
            # if action.action_type == ActionType.BACKWARD:
            #     action.agent.go(-1 * MOVEMENT_DEGREE, display)
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
                ball.check_exploded()
            tank.check_balls()

        # checking tank - ball collision
        for ball in self.ball_list:
            for tank in self.tank_list:
                if check_boom(ball, tank) and tank.get_exist() and not ball.to_kill:
                    display.play_sound(EXPLOSION_SOUND)
                    tank.destroy()
                    if tank.get_team() == ball.get_tank().get_team():
                        ball.get_tank().num_kills_round -= 1
                        ball.get_tank().num_kills += 1
                    else:
                        ball.get_tank().update_kills()
                    for shooting_tank in self.tank_list:
                        shooting_tank.poping_ball(ball)

        return State(self.tank_list, display)

    def get_ball_list(self):
        return self.ball_list

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

    def generate_wall_rays(self, agent):
        ret = []
        delta_angle = 12 * math.pi / 180
        delta_r = 10
        for i in range(int(2 * np.pi / delta_angle)):
            curr_x = agent.get_x()
            curr_y = agent.get_y()
            curr_angle = agent.get_angle() * math.pi / 180 + i * delta_angle
            sin = np.sin(curr_angle)
            cos = np.cos(curr_angle)
            while (curr_x > 0 and curr_x < WIDTH and curr_y > 0 and curr_y < HEIGHT):
                if self.display.wall_collision((int(curr_x), int(curr_y))):
                    break
                curr_x -= delta_r * cos
                curr_y += delta_r * sin
            curr_x = min(max(curr_x, 0), WIDTH)
            curr_y = min(max(curr_y, 0), HEIGHT)
            distance = math.sqrt((curr_x - agent.get_x()) ** 2 + (curr_y - agent.get_y()) ** 2)
            ret.append(distance)
        return ret

    def generate_wall_cones(self):  # todo check if neccecery
        cone_size = 12 * math.pi / 180  # 12 degrees in radians
        ret = []
        for i in range(int(2 * math.pi / cone_size)):
            pass

    def extract_features(self, agent):
        return self.generate_wall_rays(agent)

    def get_features(self, agent, state):
        return

    def check_walls_between(self, tank, ball):
        delta_r = 5
        curr_x = ball.get_x()
        curr_y = ball.get_y()
        curr_angle = math.pi * ball.get_angle() / 180
        cos = np.cos(curr_angle)
        sin = np.sin(curr_angle)
        count = 0
        while 0 < curr_x < WIDTH and 0 < curr_y < HEIGHT:
            dist_to_tank = np.sqrt((curr_x - tank.get_x()) ** 2 + (curr_y - tank.get_y()) ** 2)
            if dist_to_tank < TANK_RADIUS:
                return count
            if self.display.wall_collision((int(curr_x), int(curr_y))):
                count += 1
            curr_x -= delta_r * cos
            curr_y += delta_r * sin
        return count

    def extract_features(self, agent):
        wall_ray = self.generate_wall_rays(agent) / DIAG

        team_list, team_boolean_list, enemy_list, enemy_boolean_list = self.get_tank_cone(agent)
        ball_dist_list, ball_boolean_list = self.get_ball_cone(agent)

        return np.concatenate([wall_ray,
                               team_list,
                               enemy_list,
                               ball_dist_list,
                               ])

    def get_reward(self, agent):
        # check danger
        DANGER_FACTOR = 5
        ball_dist_list, ball_boolean_list = self.get_ball_cone(agent)
        danger_factor = -np.sum(ball_dist_list)


        # check kills
        threat_reward = 0
        tank_ball_list = agent.get_balls()
        n_live_balls = 0
        for ball in tank_ball_list:
            if not ball.to_kill:
                n_live_balls += 1
            for tank in self.tank_list:
                if tank == agent:
                    continue
                threat_reward += self.check_tank_threatening(tank, ball, agent.get_team())

        threat_reward /= (n_live_balls + 1)
        # check enemy distance
        dist_enemy_reward = 0
        dist_friend_reward = 0
        walls_between_enemies = 0
        WALLS_BETWEEN_ENEMIES_FACTOR = 1
        for tank in self.tank_list:
            if tank == agent:
                continue

            eff_dist = (DIAG - self.get_dist(tank, agent)) / DIAG
            if tank.get_team() == agent.get_team():
                if dist_friend_reward < eff_dist:
                    dist_friend_reward = eff_dist

            if tank.get_team() != agent.get_team():
                if self.check_walls_between(tank, agent):
                    walls_between_enemies -= WALLS_BETWEEN_ENEMIES_FACTOR
                if dist_enemy_reward < eff_dist:
                    dist_enemy_reward = eff_dist

        #
        # if(threat_reward != 0):
        #     print(f"\n=========\nAGENT: {agent.color}\n"
        #       f" threat_reward: {threat_reward}\n:"
        #       f"danger_factor: {danger_factor}\n"
        #       f"dist_enemy_reward:{dist_enemy_reward}\n"
        #       f"dist_friend_reward: {dist_friend_reward}\n")
        return threat_reward + danger_factor + dist_enemy_reward + dist_friend_reward

    def get_dist(self, obj1, obj2):
        dx = obj1.get_x() - obj2.get_x()
        dy = obj1.get_y() - obj2.get_y()
        return np.sqrt(dx ** 2 + dy ** 2)

    def check_tank_threatening(self, tank, ball, team):
        x_pos = ball.get_x()
        y_pos = ball.get_y()
        dy = y_pos - tank.get_y()
        dx = x_pos - tank.get_x()
        ball_angle = ball.get_angle() * np.pi / 180
        dist = np.sqrt(dx ** 2 + dy ** 2)
        hit_distance = np.abs(np.cos(ball_angle) * dy + np.sin(ball_angle) * dx)
        if hit_distance == 0 or dist == 0:
            threat_reward = 0
        else:
            threat_reward = (DIAG - dist) / max(TANK_RADIUS, hit_distance)
        walls_flag = False
        if self.check_walls_between(tank, ball) > 0:
            threat_reward /= dist
            walls_flag = True
        TEAM_THREAT_FACTOR = -10
        if tank.get_team() == team:
            threat_reward *= TEAM_THREAT_FACTOR
            if walls_flag:
                threat_reward = 0
        return threat_reward

    def get_tank_cone(self, agent):
        tank_list = self.get_tanks()
        cone_rays = np.linspace(0, 2 * np.pi, NUM_OF_CONES - 1)
        enemy_list = np.zeros(NUM_OF_CONES)
        enemy_boolean_list = np.zeros(NUM_OF_CONES)
        team_list = np.zeros(NUM_OF_CONES)
        team_boolean_list = np.zeros(NUM_OF_CONES)
        for tank in tank_list:
            if tank == agent:
                continue
            x_pos = tank.get_x()
            y_pos = tank.get_y()
            dy = y_pos - agent.get_y()
            dx = x_pos - agent.get_x()
            dist = np.sqrt(dx ** 2 + dy ** 2)
            angle_abs = np.arctan2(dy, - dx) % (2 * np.pi)
            angle_rel = (angle_abs - np.pi * agent.get_angle() / 180) % (2 * np.pi)
            cone_index = np.where(cone_rays > angle_rel)[0][0]
            cone_angle = cone_rays[cone_index]
            if tank.get_team() == agent.get_team():
                team_boolean_list[cone_index] += 1
                if team_list[cone_index] > dist:
                    team_list[cone_index] = (DIAG - dist) / DIAG
            else:
                enemy_boolean_list[cone_index] += 1
                if enemy_list[cone_index] > dist or enemy_list[cone_index] == 0:
                    enemy_list[cone_index] = (DIAG - dist) / DIAG

        return team_list, team_boolean_list, enemy_list, enemy_boolean_list

    def check_hit(self, agent, ball):
        x_pos = ball.get_x()
        y_pos = ball.get_y()
        dy = y_pos - agent.get_y()
        dx = x_pos - agent.get_x()
        ball_angle = ball.get_angle() * np.pi / 180

        hit_distance = np.abs(np.cos(ball_angle) * dy + np.sin(ball_angle) * dx)
        if hit_distance < 2 * TANK_RADIUS:
            return True
        return False

    def get_ball_cone(self, agent):

        ball_list = self.get_ball_list()

        cone_rays = np.linspace(0, 2 * np.pi, NUM_OF_CONES - 1)
        ball_hit_list = np.zeros(NUM_OF_CONES)
        ball_boolean_list = np.zeros(NUM_OF_CONES)

        for ball in ball_list:
            if ball.shooting_tank == agent or ball.to_kill:
                continue
            x_pos = ball.get_x()
            y_pos = ball.get_y()
            dy = y_pos - agent.get_y()
            dx = x_pos - agent.get_x()
            ball_angle = ball.get_angle() * np.pi / 180
            dist = np.sqrt(dx ** 2 + dy ** 2)
            angle_abs = np.arctan2(dy, - dx) % (2 * np.pi)
            hit_distance = np.abs(np.cos(ball_angle) * dy + np.sin(ball_angle) * dx)
            if not hit_distance < 4 * TANK_RADIUS or self.check_walls_between(agent, ball) > 0:
                continue
            cone_index = np.where(cone_rays > angle_abs)[0][0]
            ball_boolean_list[cone_index] += 1
            eff_dist = (DIAG - dist) / DIAG
            if eff_dist > ball_hit_list[cone_index]:
                ball_hit_list[cone_index] = eff_dist
        return ball_hit_list, ball_boolean_list

    def calc_dist_to_map_wall(self, agent, cone_angle):
        CORNERS = [(0, 0), (WIDTH, 0), (WIDTH, HEIGHT), (0, HEIGHT)]
        abs_angles = []
        for corner in CORNERS:
            dy = corner[1] - agent.get_y()
            dx = corner[0] - agent.get_x()
            angle_abs = np.arctan2(dy, - dx) % (2 * np.pi)
            abs_angles.append(angle_abs % (2 * np.pi))
        cone_abs_angle = (cone_angle + agent.get_angle() * np.pi / 180) % (2 * np.pi)
        quarter = np.where(abs_angles < cone_abs_angle)
        if len(quarter) == 0:
            quarter = 3
        else:
            quarter = quarter[0]
        if quarter == 0:
            return np.abs(agent.get_y() / (np.sin(cone_abs_angle)))
        if quarter == 1:
            return np.abs((WIDTH - agent.get_x()) / np.cos(cone_abs_angle))
        if quarter == 2:
            return np.abs((HEIGHT - agent.get_y()) / (np.sin(cone_abs_angle)))
        if quarter == 3:
            return np.abs((agent.get_x()) / np.cos(cone_abs_angle))






