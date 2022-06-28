from state import State, Action
from display import Display
import pygame
from game_setting import *


class Game:
    """
      The Game manages the control flow, soliciting actions from agents.
    """

    def __init__(self, agents, display, map_index, n_teams):
        pygame.init()
        self.agents = agents
        self.diaplay = Display(display, map_index, n_teams)
        self.init_state = State(agents)
        self.state = self.init_state
        self.num_moves = 0
        self.startingIndex = 0
        self.move_history = []

    def isGameOver(self):
        return self.state.is_terminal()

    def run(self):
        # self.display.initialize(self.state.data)

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
            action_list += action
            self.move_history.append(action)

            if agentIndex == numAgents - 1:
                ## track progress
                self.num_moves += 1
                ## update state
                self.state = self.state.generate_successor(action_list, self.diaplay)
                ## update display
                self.diaplay.update(self.state)
                action_list = []
            agentIndex = (agentIndex + 1) % numAgents

        return self.state.get_score()

    def get_map(self):
        return self.map

    def get_agents(self):
        return self.agents

    def get_display(self):
        return self.diaplay

