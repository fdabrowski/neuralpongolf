import pygame
import time
from src.game_field import GameField, ElementSymbol
from random import randint


class Game:
    GAME_SCALE = 20
    TICKS_PER_SECOND = 100

    @staticmethod
    def generate_seed():
        hole_position = (randint(0, 18), randint(0, 18))
        ball_position = (randint(0, 19), randint(0, 19))
        paddle_position = (randint(0, 15), randint(0, 18))

        while True:
            if 0 < abs(ball_position[0] - hole_position[0]) < 2:
                if 0 < abs(ball_position[1] - hole_position[1]) < 2:
                    ball_position = (randint(0, 19), randint(0, 19))
                    continue

            if 0 < abs(ball_position[0] - paddle_position[0]) < 4:
                if 0 < abs(ball_position[1] - paddle_position[1]) < 2:
                    paddle_position = (randint(0, 15), randint(0, 19))
                    continue

            break

        seed = str(hole_position[0]).zfill(2) + '-' + str(hole_position[1]).zfill(2) + ';'
        seed += str(ball_position[0]).zfill(2) + '-' + str(ball_position[1]).zfill(2) + ';'
        seed += str(paddle_position[0]).zfill(2) + '-' + str(paddle_position[1]).zfill(2)

        return seed

    def __init__(self, seed='03-03;00-00;01-00'):
        self.running = True
        self._display_surface = None
        self.size = self.width, self.height = tuple((i*(Game.GAME_SCALE+1))-1 for i in GameField.FIELD_SIZE)
        self._pooled_event = None
        self._seed = seed
        self.tick_length = 1000 / Game.TICKS_PER_SECOND
        self.fitness = 0
        self.game_field = None

    def on_init(self, gui=True):
        if gui:
            pygame.init()
            self._display_surface = pygame.display.set_mode(self.size)

        self.running = True
        self.fitness = 0
        self.game_field = GameField(self._seed)
        return True

    def on_event(self, interactive, event):
        if interactive:
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self._pooled_event = 'u'
                elif event.key == pygame.K_DOWN:
                    self._pooled_event = 'd'
                elif event.key == pygame.K_LEFT:
                    self._pooled_event = 'l'
                elif event.key == pygame.K_RIGHT:
                    self._pooled_event = 'r'
                elif event.key == pygame.K_SPACE:
                    self._pooled_event = 's'
                else:
                    self._pooled_event = None

        else:
            self._pooled_event = event

    def on_loop(self):
        self.fitness -= 1
        self.game_field.update(self._pooled_event)
        self.game_field.update_ball()

        if self.game_field.check_win():
            self.running = False

        if self._pooled_event is not None:
            self._pooled_event = None

    def on_render(self):
        self._display_surface.fill((255, 255, 255))
        self.draw_grid()
        self.visualize_game_filed(self.game_field.get_game_field())
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def draw_grid(self):
        for i in range(GameField.FIELD_WIDTH-1):
            x = ((i+1) * (Game.GAME_SCALE+1))-1
            pygame.draw.line(self._display_surface, (232, 232, 232), (x, 0), (x, self.height), 1)
        for i in range(GameField.FIELD_HEIGHT-1):
            y = ((i+1) * (Game.GAME_SCALE+1))-1
            pygame.draw.line(self._display_surface, (232, 232, 232), (0, y), (self.width, y), 1)

    def visualize_game_filed(self, field):
        for x in range(GameField.FIELD_WIDTH):
            for y in range(GameField.FIELD_HEIGHT):
                val_x = (x * (Game.GAME_SCALE+1))
                val_y = (y * (Game.GAME_SCALE+1))

                if field[x][y] == ElementSymbol.HOLE:
                    self._display_surface.fill((0, 0, 0), pygame.Rect(val_x, val_y, Game.GAME_SCALE, Game.GAME_SCALE))

                if field[x][y] == ElementSymbol.BALL:
                    self._display_surface.fill((255, 0, 0), pygame.Rect(val_x, val_y, Game.GAME_SCALE, Game.GAME_SCALE))

                if field[x][y] == ElementSymbol.PADDLE:
                    self._display_surface.fill((0, 0, 255), pygame.Rect(val_x, val_y, Game.GAME_SCALE, Game.GAME_SCALE))

    def run(self, net=None, gui=True):
        combo = []
        tick = time.clock()

        if not self.on_init(gui):
            self.running = False

        while self.running:
            if net is not None and self.fitness < -100:
                break
            if gui:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if net is None:
                        self.on_event(True, event)
                if time.clock() - tick > self.tick_length / 1000:
                    tick = time.clock()
                    if net is not None:
                        output = net.activate(self.game_field.simple_serialized)
                        selected = int(5 * output[0])
                        move = ('u', 'd', 'r', 'l', 's', '-')[selected]
                        combo.append(move)
                        self.on_event(False, move)
                    self.on_loop()
                self.on_render()

            else:
                if net is not None:
                    output = net.activate(self.game_field.simple_serialized)
                    selected = int(5 * output[0])
                    move = ('u', 'd', 'r', 'l', 's', '-')[selected]
                    self.on_event(False, move)
                self.on_loop()

        if gui:
            print("Fitness: " + str(self.fitness))
            self.on_cleanup()

        return ''.join(combo)

    def simulate(self, moves):
        while self.running:
            if len(moves) > 0:
                self.on_event(False, moves.pop(0))
            else:
                self.on_event(False, '-')
            self.on_loop()
        return self.fitness
