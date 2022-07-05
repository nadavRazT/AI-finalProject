from ball import *
from game_setting import *
from state import Action, ActionType
import numpy as np


class ATank:
    def __init__(self, color, x_pos, y_pos, angle, tank_image, controls, team, controller):
        self.is_released = True
        self.__i_xpos = x_pos
        self.__i_ypos = y_pos
        self.__xPos = x_pos
        self.__yPos = y_pos
        self.__orgImage = tank_image
        self.__image = tank_image
        self.__angle = angle + 180
        self.__rect = self.__image.get_rect().move(self.get_location())
        self.__points = {}
        self.__balls = []
        self.__controls = controls
        self.controller = controller
        self.__death = None
        self.vertical_move = 0
        self.horizontal_move = 0
        self.rotate_value = 0
        self.num_kills = 0
        self.num_kills_round = 0
        self.num_destroyed = 0
        self.move_value = 0
        self.is_exist = 1
        self.color = color
        self.team = team


    def __str__(self):
        return self.color

    def reset_tank(self):
        self.__xPos = self.__i_xpos + random.randint(-TANK_SCATTER_INDEX, TANK_SCATTER_INDEX) // 2
        self.__yPos = self.__i_ypos + random.randint(-TANK_SCATTER_INDEX, TANK_SCATTER_INDEX) // 2
        self.reset_balls()
        self.__image = self.__orgImage
        self.is_exist =1
        self.__rect.center = (self.__xPos, self.__yPos)
        self.num_kills_round = 0
        return

    def get_team(self):
        return self.color

    def get_score(self):
        return self.team.get_score()

    def rotate(self, degree):

        self.__angle += degree
        self.__angle %= 360
        self.__image = pygame.transform.rotate(self.__orgImage, self.__angle)
        x, y = self.__rect.center
        self.__rect = self.__image.get_rect()
        self.__rect.center = (x, y)

    def go(self, value, display):

        self.__points = {
            'right': [(self.__rect.center[0] + 14, self.__rect.center[1] - 14),
                      (self.__rect.center[0] + 18, self.__rect.center[1] - 7),
                      (self.__rect.center[0] + 20, self.__rect.center[1] + 0),
                      (self.__rect.center[0] + 18, self.__rect.center[1] + 7),
                      (self.__rect.center[0] + 14, self.__rect.center[1] + 14)],
            'top': [(self.__rect.center[0] + 14, self.__rect.center[1] + 14),
                    (self.__rect.center[0] + 7, self.__rect.center[1] + 18),
                    (self.__rect.center[0] + 0, self.__rect.center[1] + 20),
                    (self.__rect.center[0] - 7, self.__rect.center[1] + 18),
                    (self.__rect.center[0] - 14, self.__rect.center[1] + 14)],
            'left': [(self.__rect.center[0] - 14, self.__rect.center[1] + 14),
                     (self.__rect.center[0] - 18, self.__rect.center[1] + 7),
                     (self.__rect.center[0] - 20, self.__rect.center[1] + 0),
                     (self.__rect.center[0] - 18, self.__rect.center[1] - 7),
                     (self.__rect.center[0] - 14, self.__rect.center[1] - 14)],
            'bottom': [(self.__rect.center[0] - 14, self.__rect.center[1] - 14),
                       (self.__rect.center[0] - 7, self.__rect.center[1] - 18),
                       (self.__rect.center[0] - 0, self.__rect.center[1] - 20),
                       (self.__rect.center[0] + 7, self.__rect.center[1] - 18),
                       (self.__rect.center[0] + 14, self.__rect.center[1] - 14)]}

        angle_radian = (self.__angle * (math.pi / 180))

        self.horizontal_move = -value * math.cos(angle_radian)
        self.vertical_move = value * math.sin(angle_radian)
        wall_calculation_horizontal = self.calculate_horizontal(self.horizontal_move, display)
        wall_calculation_vertical = self.calculate_vertical(self.vertical_move, display)

        if wall_calculation_horizontal:
            self.horizontal_move = 0

        if wall_calculation_vertical:
            self.vertical_move = 0

        self.__xPos += self.horizontal_move
        self.__yPos += self.vertical_move
        self.__rect.center = (self.__xPos, self.__yPos)

    def add_score(self):
        self.team.add_score()
        return

    def calculate_horizontal(self, value, display):

        right, left = self.__points['right'], self.__points['left']

        if value >= 0:
            for point in right:
                if display.wall_collision(point):
                    return True
            return False
        elif value < 0:
            for point in left:
                if display.wall_collision(point):
                    return True
            return False

    def calculate_vertical(self, value, display):

        top, bottom = self.__points['top'], self.__points['bottom']

        if value >= 0:
            for point in top:
                if display.wall_collision(point):
                    return True
            return False
        elif value < 0:
            for point in bottom:
                if display.wall_collision(point):
                    return True
            return False

    def shoot(self):
        shooting_ball = Ball(self.__xPos, self.__yPos, self.__angle, self)
        self.__balls.append(shooting_ball)

    def check_balls(self):

        for ball in self.__balls:
            if ball.to_kill:
                self.__balls.remove(ball)
                # print(self.__balls)

    def poping_ball(self, ball):
        try:
            self.__balls.remove(ball)
        except:
            pass

    def change_location(self, x, y, angle=0):
        self.__xPos = x
        self.__yPos = y

    def reset_balls(self):
        self.__balls = []

    def destroy(self):
        self.is_exist = 0
        self.num_destroyed += 1
        self.__death = time.time()
        self.__image = IMG_EXPLOSION

    def update_kills(self):
        self.num_kills += 1
        self.num_kills_round += 1

    def get_x(self):
        return self.__xPos

    def get_y(self):
        return self.__yPos

    def get_balls(self):
        return self.__balls

    def get_location(self):
        return self.__xPos, self.__yPos

    def get_image(self):
        return self.__image

    def get_angle(self):
        return self.__angle

    def get_rect(self):
        return self.__rect

    def get_death_time(self):
        return self.__death

    def get_exist(self):
        return self.is_exist

    def get_points(self):
        return self.__points

    def get_manual_actions(self):

        actions = []
        if keyboard.is_pressed(self.__controls[3]):
            actions.append(Action(self, ActionType.LEFT))
        if keyboard.is_pressed(self.__controls[2]):
            actions.append(Action(self, ActionType.RIGHT))
        if keyboard.is_pressed(self.__controls[0]):
            actions.append(Action(self, ActionType.FORWARD))
        if keyboard.is_pressed(self.__controls[1]):
            actions.append(Action(self, ActionType.BACKWARD))
        if keyboard.is_pressed(self.__controls[4]) and self.is_released:
            actions.append(Action(self, ActionType.SHOOT))
            self.is_released = False
        if not keyboard.is_pressed(self.__controls[4]):
            self.is_released = True
        return actions

    def get_action(self, state):
        if self.controller == MAN_CONTROL:
            #print(self.__angle)
            return self.get_manual_actions()


class Team:
    def __init__(self, color, n_tanks):
        self.score = 0
        self.n_tanks = n_tanks

    def get_score(self):
        return self.score

    def add_score(self):
        self.score += 1

    def get_n_tanks(self):
        return self.n_tanks

    def kill_tank(self):
        self.n_tanks -= 1


class TankFactory:
    def __init__(self, n_manual, teams):
        """
        n_tanks - number of tanks
        n_manual - number of manual agents
        teams - number of teams and devision
        """
        positions = get_team_positions(teams)
        self.tank_list = []
        i = 0
        for color, n_players in teams.items():
            team = Team(color, n_players)
            for _ in range(n_players):
                if i < n_manual:
                    self.tank_list.append(
                        ATank(color, positions[i][0], positions[i][1], 180, TANK_IMAGES[color],
                              MANUAL_CONTROL_TANK[i % len(MANUAL_CONTROL_TANK)], team, MAN_CONTROL))
                else:
                    self.tank_list.append(
                        ATank(color, positions[i][0], positions[i][1], 180, TANK_IMAGES[color], AI_CONTROL,
                              team, NOT_MAN_CONTROL))
                i += 1

    def get_tanks(self):
        return self.tank_list
