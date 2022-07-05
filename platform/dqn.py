from torch import nn
import torch
from collections import deque
import itertools
import numpy as np
import random
from tank import TankFactory
from game import Game
from state import ActionType, Action, State
from tqdm import tqdm

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


class Network(nn.Module):
    def __init__(self):
        super().__init__()
        in_features = 120
        out_features = 6
        self.net = nn.Sequential(nn.Linear(in_features, 120),
                                 nn.Tanh(),
                                 nn.Linear(120, 50),
                                 nn.ReLU(),
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
rew_buffer_1 = deque([0.0], maxlen=100)
rew_buffer_2 = deque([0.0], maxlen=100)


# initialize environment
def init_env():
    teams = {"Red": 1, "Green": 1}
    TF = TankFactory(0, teams)
    tank_list = TF.get_tanks()
    game = Game(tank_list, display=True, map_index=0, n_teams=2, n_rounds=1)
    game.reset_game()
    state = game.state
    return state, game, tank_list


state, game, tank_list = init_env()

episode_reward_1 = 0.0
episode_reward_2 = 0.0

online_net = Network()
target_net = Network()

target_net.load_state_dict(online_net.state_dict())

optimizer = torch.optim.Adam(online_net.parameters(), lr=LEARNING_RATE)

# initialize replay buffer
for i in tqdm(range(MIN_REPLAY_SIZE)):
    action1 = random.randrange(6)
    action1obj = Action(tank_list[0], ActionType(action1))
    action2 = random.randrange(6)
    action2obj = Action(tank_list[1], ActionType(action2))
    actions = [action1obj, action2obj]

    pre_tank1 = state.extract_features(tank_list[0])
    pre_tank2 = state.extract_features(tank_list[1])
    next_state = state.generate_successor(actions, game.display)
    post_tank1 = next_state.extract_features(tank_list[0])
    post_tank2 = next_state.extract_features(tank_list[1])
    rew1 = next_state.get_reward(tank_list[0])
    rew2 = next_state.get_reward(tank_list[1])
    done = next_state.is_terminal()
    transition1 = (pre_tank1, action1, rew1, done, post_tank1)
    transition2 = (pre_tank2, action2, rew2, done, post_tank2)
    replay_buffer.append(transition1)
    replay_buffer.append(transition2)

    game.display.update(state)

    state = next_state

    if done:
        state, game, tank_list = init_env()

for step in itertools.count():
    epsilon = np.interp(step, [0, EPSILON_DECAY], [EPSILON_START, EPSILON_END])

    rnd1 = random.random()
    rnd2 = random.random()

    if rnd1 < epsilon:
        action1 = random.randrange(6)
        action1obj = Action(tank_list[0], ActionType(action1))
    else:
        action1 = online_net.act(state.extract_features(tank_list[0]))
        action1obj = Action(tank_list[0], ActionType(action1))

    if rnd2 < epsilon:
        action2 = random.randrange(6)
        action2obj = Action(tank_list[1], ActionType(action2))
    else:
        action2 = online_net.act(state.extract_features(tank_list[1]))
        action2obj = Action(tank_list[1], ActionType(action2))

    actions = [action1obj, action2obj]

    pre_tank1 = state.extract_features(tank_list[0])
    pre_tank2 = state.extract_features(tank_list[1])
    next_state = state.generate_successor(actions, game.display)
    post_tank1 = next_state.extract_features(tank_list[0])
    post_tank2 = next_state.extract_features(tank_list[1])
    rew1 = next_state.get_reward(tank_list[0])
    rew2 = next_state.get_reward(tank_list[1])
    done = next_state.is_terminal()

    transition1 = (pre_tank1, action1, rew1, done, post_tank1)
    transition2 = (pre_tank2, action2, rew2, done, post_tank2)
    replay_buffer.append(transition1)
    replay_buffer.append(transition2)

    game.display.update(state)

    state = next_state

    episode_reward_1 += rew1
    episode_reward_2 += rew2

    if done:
        state, game, tank_list = init_env()
        rew_buffer_1.append(episode_reward_1)
        rew_buffer_2.append(episode_reward_2)

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

    if step % TARGET_UPDATE_FREQ == 0:
        target_net.load_state_dict(online_net.state_dict())
        print()
        print("Step", step)
        print("Avg Rew 1", np.mean(rew_buffer_1))
        print("Avg Rew 2", np.mean(rew_buffer_2))
