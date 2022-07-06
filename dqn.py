from torch import nn
import torch
from collections import deque
import itertools
import numpy as np
import random
from GameEngine.tank import TankFactory
from GameEngine.game import Game
from GameEngine.state import ActionType, Action, State
from tqdm import tqdm
import pygame
import sys
GAMMA = 0.99
BATCH_SIZE = 32
BUFFER_SIZE = 50000
MIN_REPLAY_SIZE = 1000
EPSILON_START = 1.0
EPSILON_END = 0.02
EPSILON_DECAY = 30000
TARGET_UPDATE_FREQ = 1000
INPUT_STATE_FEATURES = 0
LEARNING_RATE = 5e-4
out_features = 5


class Network(nn.Module):
    def __init__(self):
        super().__init__()
        in_features = 120
        self.net = nn.Sequential(nn.Linear(in_features, 50),
                                 nn.Tanh(),
                                 nn.Linear(50, out_features))

    def forward(self, x):
        return self.net(x)

    def act(self, x):
        state_t = torch.as_tensor(np.array(x), dtype=torch.float32)
        q_values = self(state_t.unsqueeze(0))
        max_q_index = torch.argmax(q_values, dim=1)[0]
        action = max_q_index.detach().item()
        return action


replay_buffer = deque(maxlen=BUFFER_SIZE)


# initialize environment
def init_env(dis):
    teams = {"Red": 1, "Green": 1}
    TF = TankFactory(0, teams)
    tank_list = TF.get_tanks()
    map = random.choice([0, 4, 5, 6])
    game = Game(tank_list, display=dis, map_index=map, n_teams=2, n_rounds=1)
    game.reset_game()
    state = game.state
    return state, game, tank_list


state, game, tank_list = init_env(False)

online_net = Network()
target_net = Network()

target_net.load_state_dict(online_net.state_dict())

optimizer = torch.optim.Adam(online_net.parameters(), lr=LEARNING_RATE)
cur_step = 0
# initialize replay buffer
for i in tqdm(range(MIN_REPLAY_SIZE)):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    actions = []
    pre_tank = []
    actions_i = []
    for j in range(len(tank_list)):
        action_i = random.randrange(out_features)
        actions_i.append(action_i)
        actionobj = Action(tank_list[j], ActionType(action_i))
        actions.append(actionobj)
        pre_tank += [state.extract_features(tank_list[j])]

    next_state = state.generate_successor(actions, game.display)

    done = next_state.is_terminal()

    rew = []
    for j in range(len(tank_list)):
        post_tank = next_state.extract_features(tank_list[j])
        rew = next_state.get_reward(tank_list[j])
        transition = (pre_tank[j], actions_i[j], rew, done, post_tank)
        replay_buffer.append(transition)

    game.display.update(state)

    state = next_state

    if done:
        state, game, tank_list = init_env(game.display.is_display)

    # if i % (100) == 0:
    #     cur_step = i
    #     dis = game.display.is_display
    #     dis = not dis
    #     game.display.change_display(dis)


cur_step = 0
for step in itertools.count():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    epsilon = np.interp(step, [0, EPSILON_DECAY], [EPSILON_START, EPSILON_END])
    actions_i = []
    actions = []
    pre_tank = []
    for j in range(len(tank_list)):
        rnd = random.random()

        if rnd < epsilon:
            action_i = random.randrange(out_features)
            actionobj = Action(tank_list[j], ActionType(action_i))
        else:
            action_i = online_net.act(state.extract_features(tank_list[j]))
            actionobj = Action(tank_list[0], ActionType(action_i))
        actions.append(actionobj)
        actions_i.append(action_i)
        pre_tank.append(state.extract_features(tank_list[j]))


    next_state = state.generate_successor(actions, game.display)
    done = next_state.is_terminal()

    rew = []
    episode_reward = np.zeros(len(tank_list))
    for j in range(len(tank_list)):
        post_tank = next_state.extract_features(tank_list[j])
        rew = next_state.get_reward(tank_list[j])
        transition = (pre_tank[j], actions_i[j], rew, done, post_tank)
        replay_buffer.append(transition)
        episode_reward[j] += rew


    game.display.update(state)

    state = next_state
    rew_buffer = [[] for i in range(len(tank_list))]
    if done:
        state, game, tank_list = init_env(game.display.is_display)
    for j in range(len(tank_list)):
        rew_buffer[j].append(episode_reward[j])

    transitions = random.sample(replay_buffer, BATCH_SIZE)

    states = np.asarray([t[0] for t in transitions])
    actions = np.asarray([t[1] for t in transitions])
    rews = np.asarray([t[2] for t in transitions])
    dones = np.asarray([t[3] for t in transitions])
    next_states = np.asarray([t[4] for t in transitions])

    #print(actions)

    states_t = torch.as_tensor(states, dtype=torch.float32)
    actions_t = torch.as_tensor(actions, dtype=torch.int64).unsqueeze(-1)
    rews_t = torch.as_tensor(rews, dtype=torch.float32).unsqueeze(-1)
    dones_t = torch.as_tensor(dones, dtype=torch.float32).unsqueeze(-1)
    next_states_t = torch.as_tensor(next_states, dtype=torch.float32)

    target_q_values = target_net(next_states_t)
    max_target_q_value = target_q_values.max(dim=1, keepdim=True)[0]

    targets = rews_t + GAMMA * (1 - dones_t) * max_target_q_value

    q_values = online_net(states_t)
    action_q_values = torch.gather(input=q_values, dim=1, index=actions_t)
    loss = nn.functional.smooth_l1_loss(action_q_values, targets)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()


    if step % (TARGET_UPDATE_FREQ) == 0:
        cur_step = step
        dis = game.display.is_display
        game.display.change_display(not dis)

    if step % TARGET_UPDATE_FREQ == 0:
        target_net.load_state_dict(online_net.state_dict())
        state, game, tank_list = init_env(game.display.is_display)

        print()
        print("Step", step)
        for i in range(len(tank_list)):
            print(f"Avg Rew {i}", np.mean(rew_buffer[i]))
    if step == 1500:
        break