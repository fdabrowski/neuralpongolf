import argparse
import pickle
from src.game import Game
from src.neural_network import NeuralNetwork

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--nn', action="store_true")
    parser.add_argument('-S', '--seed')
    parser.add_argument('-r', '--randomseed', action="store_true")
    parser.add_argument('-s', '--save')
    parser.add_argument('-l', '--load')

    args = parser.parse_args()

    seed ='12-14;05-03;02-16'

    if args.seed:
        seed = args.seed

    if args.randomseed:
        seed = Game.generate_seed()

    if args.load:
        genome = pickle.load(open(args.load, 'rb'))
        nn = NeuralNetwork(False, seed)
        nn.winner = genome
        nn.play_winner()

    elif args.nn:
        nn = NeuralNetwork(False, seed)
        winner = nn.run()

        if args.save:
            with open(args.save, 'wb') as f:
                pickle.dump(winner, f)

        nn.play_winner()

    else:
        game = Game(seed)
        game.run()

