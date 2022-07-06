import random

from GameEngine.state import State, Action
from GameEngine.display import Display
import pygame
from GameEngine.game_setting import *
from GameEngine.functions import reducer
from GameEngine.functions import get_team_positions
from functools import reduce

class Game:
    """
      The Game manages the control flow, soliciting actions from agents.
    """

    def __init__(self, agents, display, map_index, n_teams, n_rounds):
        pygame.init()
        self.n_teams = n_teams
        self.agents = agents
        self.display = Display(display, map_index, n_teams)
        self.init_state = State(agents, self.display)
        self.state = self.init_state
        self.num_moves = 0
        self.startingIndex = 0
        self.move_history = []
        self.n_rounds = n_rounds
        self.score = 0

    def isGameOver(self):
        return self.state.is_terminal()

    def run_round(self):
        agentIndex = self.startingIndex
        numAgents = len(self.agents)
        action_list = []
        while not self.isGameOver():
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            agent = self.agents[agentIndex]

            action = agent.get_action(self.state)
            self.state.get_ball_cone(agent)
            if action:
                action_list += action
            self.move_history.append(action)
            self.state = self.state.generate_successor(action_list, self.display)


            action_list = []

            if agentIndex == numAgents - 1:
                ## track progress
                self.num_moves += 1
                ## update state
                ## update display
                self.display.update(self.state)
            agentIndex = (agentIndex + 1) % numAgents
        return self.state.get_score()

    def run(self):
        scores = []
        for i in range(self.n_rounds):
            self.reset_game()
            round_score = self.run_round()
            scores += [round_score]
        self.score = reduce(reducer, scores, {})
        pygame.quit()
        return self.score


    def reset_game(self):
        start_pos = random.sample(TEAM_START_POSITIONS, k=self.n_teams)

        # reset tanks
        cur_team = self.agents[0].get_team()
        prev_team = self.agents[0].get_team()
        i = 0
        for tank in self.agents:
            cur_team = tank.get_team()
            if cur_team != prev_team:
                i += 1
            tank.reset_tank(start_pos[i])
            prev_team = cur_team
        # reset balls
        self.state = self.init_state
        self.display.update(self.state)

    def get_agents(self):
        return self.agents

    def get_display(self):
        return self.display
