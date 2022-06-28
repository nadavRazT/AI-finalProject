from state import State, Action
from display import Display
import pygame
from game_setting import *

class Game:
    """
      The Game manages the control flow, soliciting actions from agents.
    """

    def __init__(self, agents, display, map_index):
        pygame.init()
        self.agents = agents
        self.diaplay = Display(display, map_index)
        self.init_state = State(self.map, agents)
        self.state = self.init_state.deepCopy()
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
            agent = self.agents[agentIndex]
            ## generate observation
            # observation = self.state.deepCopy() todo: check if needed
            action = agent.get_action(self.state)
            action_list.append(action)
            self.move_history.append(action)

            if agentIndex == numAgents - 1:
                ## track progress
                self.num_moves += 1
                ## update state
                self.state = self.state.generateSuccessor(action_list)
                ## update display
                self.diaplay.update(self.state)
            agentIndex = (agentIndex + 1) % numAgents


    def get_map(self):
        return self.map

    def get_agents(self):
        return self.agents

    def get_display(self):
        return self.diaplay
