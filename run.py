from src.game import Game
from src.neural_network import NeuralNetwork

if __name__ == "__main__":
    nn = NeuralNetwork(False, '12-14;05-03;02-16')
    nn.run()

    # game = Game(Game.generate_seed())
    # game.run()

