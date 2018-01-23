import pygame
import time
from src.game_field import GameField, ElementSymbol


class Game:
    GAME_SCALE = 20
    TICKS_PER_SECOND = 10

    def __init__(self, seed='03-03;17-05;08-10'):
        self._running = True
        self._display_surface = None
        self.size = self.width, self.height = tuple((i*(Game.GAME_SCALE+1))-1 for i in GameField.FIELD_SIZE)
        self.game_field = GameField(seed)
        self.current_frame_game_field = self.game_field.get_game_field()
        self._pooled_event = None
        self.tick_length = 1000 / Game.TICKS_PER_SECOND
        self.fitness = 0

    def on_init(self):
        pygame.init()
        self._display_surface = pygame.display.set_mode(self.size)
        self._running = True
        return True

    def on_event(self, interactive, event):
        if interactive:
            if event.type == pygame.QUIT:
                self._running = False

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
        self.fitness += 1
        self.game_field.update(self._pooled_event)
        self.game_field.update_ball()

        if self.game_field.check_win():
            print("player won")
            print("Fitness: " + str(self.fitness))
            self._running = False

        if self._pooled_event is not None:
            self._pooled_event = None

    def on_render(self):
        print('render')
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

    def run(self, moves=None):
        tick = time.clock()

        if not self.on_init():
            self._running = False

        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                if moves is None:
                    self.on_event(True, event)
            if time.clock() - tick > self.tick_length / 1000:
                if moves is not None:
                    if len(moves) > 0:
                        self.on_event(False, moves.pop(0))
                    else:
                        self.on_event(False, '-')
                self.on_loop()
                tick = time.clock()
            self.on_render()

        self.on_cleanup()
