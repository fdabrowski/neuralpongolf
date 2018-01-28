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
    parser.add_argument('--generations')
    parser.add_argument('--noviz', action="store_true")
    parser.add_argument('--multimap', action="store_true")

    args = parser.parse_args()

    seed ='03-03;13-08;10-15'

    if args.seed:
        seed = args.seed

    if args.randomseed:
        seed = Game.generate_seed()

    if args.multimap:
        seed = []

        for i in range(50):
            seed.append(Game.generate_seed())

        generations = 100

        if args.generations:
            generations = int(args.generations)

        nn = NeuralNetwork(False, seed, generations, True)
        winner = nn.run()

        if not args.noviz:
            nn.visualize_results()

        if args.save:
            with open(args.save, 'wb') as f:
                pickle.dump(winner, f)

    if args.load:
        genome = pickle.load(open(args.load, 'rb'))

        try:
            seed = pickle.load(open(args.load + "_seed", 'rb'))

        except FileNotFoundError:
            print("No seed file found")

        nn = NeuralNetwork(False, seed)
        nn.winner = genome
        nn.play_winner()

    elif args.nn:
        generations = 100

        if args.generations:
            generations = int(args.generations)

        nn = NeuralNetwork(False, seed, generations)
        winner = nn.run()

        if not args.noviz:
            nn.visualize_results()

        if args.save:
            with open(args.save, 'wb') as f:
                pickle.dump(winner, f)
            with open(args.save + "_seed", 'wb') as f:
                pickle.dump(seed, f)

        nn.play_winner()

    else:
        game = Game(seed)
        game.run()

