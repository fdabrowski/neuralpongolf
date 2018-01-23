from src.game import Game
import neat
import os

def evaluate_genome(genomes, config):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        game = Game('03-03;17-05;08-10')
        game.run(net, True)

        genome.fitness = game.fitness


def run_neural():
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         os.path.join(os.path.dirname(__file__), 'config'))

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    winner = p.run(evaluate_genome, 100)


if __name__ == "__main__":
    run_neural()
    # print("fitness: " + str(game.simulate(list('uuuuuddddlrlrlrrrrrrlldddddddduuuuuu'))))
    # game = Game()
    # print(game.simulate(list('-')))
    # game.run()

