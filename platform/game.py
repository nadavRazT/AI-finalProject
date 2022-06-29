from state import State, Action
from display import Display
import pygame
from game_setting import *
from functions import reducer
from functools import reduce

class Game:
    """
      The Game manages the control flow, soliciting actions from agents.
    """

    def __init__(self, agents, display, map_index, n_teams, n_rounds):
        pygame.init()
        self.agents = agents
        self.diaplay = Display(display, map_index, n_teams)
        self.init_state = State(agents, display)
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
            ## generate observation
            # observation = self.state.deepCopy() todo: check if needed
            action = agent.get_action(self.state)
            if action:
                action_list += action
            self.move_history.append(action)
            self.state = self.state.generate_successor(action_list, self.diaplay)
            action_list = []

            if agentIndex == numAgents - 1:
                ## track progress
                self.num_moves += 1
                ## update state
                ## update display
                self.diaplay.update(self.state)
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
        # reset tanks
        for tank in self.agents:
            tank.reset_tank()
        # reset balls
        self.state = self.init_state
        self.diaplay.update(self.state)

    def get_agents(self):
        return self.agents

    def get_display(self):
        return self.diaplay
