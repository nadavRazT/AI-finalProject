import numpy as np
import neat
import pygame
import sys
import GameEngine as ge
import multiprocessing
import random
import pickle
import visualize
import os
import video
runs_per_net = 2

# reporter
class reporter_play(neat.reporting.BaseReporter):
    def __init__(self):
        neat.reporting.BaseReporter.__init__(self)
        self.gen = 0

    def end_generation(self, config, population, species_set):
        genomes = population
        print(population)
        best_fitness = -np.inf
        best_fitness_id = None
        for genome_id, genome in genomes.items():
            if not genome.fitness:
                continue
            if genome.fitness > best_fitness:
                best_fitness = genome.fitness
                best_fitness_id = genome_id
        print(f"running best of generation {self.gen}")
        if best_fitness_id:
            run_game(neat.nn.FeedForwardNetwork.create(genomes[best_fitness_id], config), gen_num=self.gen)
        self.gen+=1


# initialize environment
def init_env(dis):
    teams = {"Red": 1, "Green": 1}
    TF = ge.TankFactory(0, teams)
    tank_list = TF.get_tanks()
    map = random.choice([0, 5, 6])
    game = ge.Game(tank_list, display=dis, map_index=0, n_teams=2, n_rounds=1)
    game.reset_game(dis)
    state = game.state
    return state, game, tank_list


# Use the NN network phenotype and the discrete actuator force function.
def eval_genome(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    fitnesses = []
    number_of_steps_per_run = 100
    for runs in range(runs_per_net):
        state, game, agent_list = init_env(False)
        # Run the given simulation for up to num_steps time steps.
        fitness = 0.0
        done = False
        step = 0
        game.reset_game(False)
        while step < number_of_steps_per_run:
            ## for pygame ## 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            actions = []
            for j in range(len(agent_list)):
                action_i = np.argmax(net.activate(state.extract_features(agent_list[j])))
                # print(net.activate(state.extract_features(agent_list[j])))
                actionobj = ge.Action(agent_list[j], ge.ActionType(action_i))
                actions.append(actionobj)
            state = state.generate_successor(actions, game.display, step)
            game.display.update(state)
            step += 1
            done = state.is_terminal()
            if done:
                game.reset_game(False)
                done = False
            fitness += np.max([state.get_reward(agent)[1] for agent in agent_list])
        # print(fitness)
        fitnesses.append(fitness)
    # The genome's fitness is its worst performance across all runs.
    genome.fitness = np.mean(fitnesses)
    return np.mean(fitnesses)


def eval_genomes(genomes, config):
    best_fitness = 0
    best_fitness_id = None
    for genome_id, genome in genomes:
        genome.fitness = eval_genome(genome, config)
        if genome.fitness > best_fitness:
            best_fitness = genome.fitness
            best_fitness_id = genome_id

    run_game(neat.nn.FeedForwardNetwork.create(genomes[best_fitness_id], config), 3)


def run_game(net, gen_num,num_games=1):
    n = 0
    number_of_steps_per_run = 100

    while n < num_games:
        state, game, agent_list = init_env(True)
        n += 1
        # Run the given simulation for up to num_steps time steps.
        done = False
        step = 0
        game.reset_game(True)
        vid = video.Video(0)
        while not done and step < number_of_steps_per_run:
            ## for pygame ##
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            actions = []
            for j in range(len(agent_list)):
                action_i = np.argmax(net.activate(state.extract_features(agent_list[j])))
                # print(net.activate(state.extract_features(agent_list[j])))
                actionobj = ge.Action(agent_list[j], ge.ActionType(action_i))
                actions.append(actionobj)
            vid.make_png(state.display.screen)
            state = state.generate_successor(actions, game.display, step)
            game.display.update(state)
            step += 1
            done = state.is_terminal()
        vid.make_mp4(gen_num)
        game.close_game()


def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    stats = neat.StatisticsReporter()

    # restore prev run
    # p = neat.Checkpointer.restore_checkpoint('neat_checkpoint/cp-14') # remove if necc

    # create reporters to check progress
    p.add_reporter(stats)
    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(reporter_play())
    p.add_reporter(neat.Checkpointer(5, filename_prefix='neatAgent/neat_checkpoint/cp-'))

    # Run for up to 300 generations.
    pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome)
    winner = p.run(pe.evaluate, 50)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))
    # Save the winner.
    with open('winner-basic-train-small-grid', 'wb') as f:
        pickle.dump(winner, f)

    visualize.plot_stats(stats, ylog=True, view=True, filename="feedforward-fitness.svg")
    visualize.plot_species(stats, view=True, filename="feedforward-speciation.svg")

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    run_game(winner_net, gen_num=50, num_games=20)



def load_net(filename):
    # load the winner
    with open(filename, 'rb') as f:
        c = pickle.load(f)

    print('Loaded genome:')
    print(c)

    # Load the config file, which is assumed to live in
    # the same directory as this script.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, '../config')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    net = neat.nn.FeedForwardNetwork.create(c, config)
    return net


if __name__ == "__main__":
    #
    # winner_net = load_net('winner-basic-train-small-grid')
    # run_game(winner_net, 20)
    #
    run('../config')
