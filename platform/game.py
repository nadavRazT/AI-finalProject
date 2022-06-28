class Game:
    """
      The Game manages the control flow, soliciting actions from agents.
    """

    def __init__(self, agents, display, map):
        self.agents = agents
        self.diaplay = display
        self.map = map
        self.init_state = GameState()
        self.state = self.init_state.deepCopy()



    def get_map(self):
        return self.map

    def get_agents(self):
        return self.agents

    def get_display(self):
        return self.diaplay
