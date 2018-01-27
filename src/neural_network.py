from src.game import Game
import neat
import os
import src.visualize as visualize


class NeuralNetwork:
    GENERATIONS = 100

    def __init__(self, random_seed=False, game_seed=None):
        self.config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                  neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                  os.path.join(os.path.dirname(__file__), '../config'))

        self.population = neat.Population(self.config)

        self.stats = neat.StatisticsReporter()
        self.population.add_reporter(self.stats)
        self.population.add_reporter(neat.StdOutReporter(True))

        self.random_seed = random_seed
        self.game_seed = game_seed

        self.winner = None

    def visualize_results(self):
        visualize.draw_net(self.config, self.winner, True)
        visualize.plot_stats(self.stats, ylog=False, view=True)
        visualize.plot_species(self.stats, view=True)

    def evaluate_genome(self, genomes, config):
        for genome_id, genome in genomes:
            net = neat.nn.FeedForwardNetwork.create(genome, config)

            if not self.random_seed:
                if self.game_seed is not None:
                    game = Game(self.game_seed)
                else:
                    game = Game()
            else:
                game = Game(Game.generate_seed())

            game.run(net, False)

            genome.fitness = game.fitness

    def play_winner(self):
        net = neat.nn.FeedForwardNetwork.create(self.winner, self.config)

        while True:
            if not self.random_seed:
                if self.game_seed is not None:
                    game = Game(self.game_seed)
                else:
                    game = Game()
            else:
                game = Game(Game.generate_seed())

            game.run(net, True)

    def run(self):
        self.winner = self.population.run(self.evaluate_genome, NeuralNetwork.GENERATIONS)
        self.visualize_results()
        self.play_winner()
