from enum import Enum, IntEnum

class ElementSymbol(Enum):
    HOLE = 1
    BALL = 2
    PADDLE = 3
    TRACK = 4
    NONE = 0


class GameField:
    FIELD_SIZE = FIELD_WIDTH, FIELD_HEIGHT = 20, 20

    def __init__(self):
        self._game_field = [[0 for x in range(GameField.FIELD_WIDTH)] for y in range(GameField.FIELD_HEIGHT)]

        self._hole_position = None
        self._ball_position = None
        self._paddle_position = None
        self._paddle_horizontal = True
        self._ball_direction = (-1, 1)  # [0]: -1 - left, 1 - right; [1]: -1 - up, 1 - down

        self.place_elements('03-03;17-05;08-10')

    def place_elements(self, seed = ''):
        if len(seed) == 17:
            positions = seed.split(';')
            self._hole_position = tuple([int(pos) for pos in positions[0].split('-')])
            self._ball_position = tuple([int(pos) for pos in positions[1].split('-')])
            self._paddle_position = tuple([int(pos) for pos in positions[2].split('-')])

        elif len(seed) != 0:
            raise ValueError('Something with seed is messed up')

        self._game_field[self._hole_position[0]][self._hole_position[1]] = ElementSymbol.HOLE
        self._game_field[self._hole_position[0]][self._hole_position[1]+1] = ElementSymbol.HOLE
        self._game_field[self._hole_position[0]+1][self._hole_position[1]] = ElementSymbol.HOLE
        self._game_field[self._hole_position[0]+1][self._hole_position[1]+1] = ElementSymbol.HOLE

        self._game_field[self._ball_position[0]][self._ball_position[1]] = ElementSymbol.BALL

        self._game_field[self._paddle_position[0]][self._paddle_position[1]] = ElementSymbol.PADDLE
        self._game_field[self._paddle_position[0]+(1*int(self._paddle_horizontal))][self._paddle_position[1]+(1*int(not self._paddle_horizontal))] = ElementSymbol.PADDLE
        self._game_field[self._paddle_position[0]+(2*int(self._paddle_horizontal))][self._paddle_position[1]+(2*int(not self._paddle_horizontal))] = ElementSymbol.PADDLE
        self._game_field[self._paddle_position[0]+(3*int(self._paddle_horizontal))][self._paddle_position[1]+(3*int(not self._paddle_horizontal))] = ElementSymbol.PADDLE

    def update(self, key):
        self._game_field[self._paddle_position[0]][self._paddle_position[1]] = ElementSymbol.NONE
        self._game_field[self._paddle_position[0]+(1*int(self._paddle_horizontal))][self._paddle_position[1]+(1*int(not self._paddle_horizontal))] = ElementSymbol.NONE
        self._game_field[self._paddle_position[0]+(2*int(self._paddle_horizontal))][self._paddle_position[1]+(2*int(not self._paddle_horizontal))] = ElementSymbol.NONE
        self._game_field[self._paddle_position[0]+(3*int(self._paddle_horizontal))][self._paddle_position[1]+(3*int(not self._paddle_horizontal))] = ElementSymbol.NONE

        if key == 'u':
            if self._paddle_position[1] > 0:
                self._paddle_position = (self._paddle_position[0], self._paddle_position[1] - 1)

        if key == 'd':
            if self._paddle_position[1] < GameField.FIELD_HEIGHT-(int(not self._paddle_horizontal) * 3)-1:
                self._paddle_position = (self._paddle_position[0], self._paddle_position[1] + 1)

        if key == 'l':
            if self._paddle_position[0] > 0:
                self._paddle_position = (self._paddle_position[0] - 1, self._paddle_position[1])

        if key == 'r':
            if self._paddle_position[0] < GameField.FIELD_WIDTH - (int(self._paddle_horizontal) * 3)-1:
                self._paddle_position = (self._paddle_position[0] + 1, self._paddle_position[1])

        if key == 's':
            if self._paddle_horizontal:
                if self._paddle_position[1] > GameField.FIELD_HEIGHT - 4:
                    self._paddle_position = (self._paddle_position[0], GameField.FIELD_HEIGHT - 4)

            if not self._paddle_horizontal:
                if self._paddle_position[0] > GameField.FIELD_WIDTH - 4:
                    self._paddle_position = (GameField.FIELD_WIDTH - 4, self._paddle_position[1])

            self._paddle_horizontal = not self._paddle_horizontal

        self.place_elements()

    def get_game_field(self):
        return self._game_field

    def update_ball(self):
        self._game_field[self._ball_position[0]][self._ball_position[1]] = ElementSymbol.NONE

        # bounce left <-> right
        if 0 > self._ball_position[0] + self._ball_direction[0] or self._ball_position[0] + self._ball_direction[0] >= GameField.FIELD_WIDTH:
            self._ball_direction = (self._ball_direction[0] * -1, self._ball_direction[1])

        # bounce up <-> down
        if 0 > self._ball_position[1] + self._ball_direction[1] or self._ball_position[1] + self._ball_direction[1] >= GameField.FIELD_WIDTH:
            self._ball_direction = (self._ball_direction[0], self._ball_direction[1] * -1)

        if self._game_field[self._ball_position[0]+self._ball_direction[0]][self._ball_position[1]] == ElementSymbol.PADDLE:
            self._ball_direction = (self._ball_direction[0] * -1, self._ball_direction[1])

        if self._game_field[self._ball_position[0]][self._ball_position[1]+self._ball_direction[1]] == ElementSymbol.PADDLE:
            self._ball_direction = (self._ball_direction[0], self._ball_direction[1] * -1)

        self._ball_position = (self._ball_position[0] + self._ball_direction[0], self._ball_position[1] + self._ball_direction[1])

        self._game_field[self._ball_position[0]][self._ball_position[1]] = ElementSymbol.BALL

    def check_win(self):
        if  0 <= self._ball_position[0] - self._hole_position[0] <= 1 and 0 <= self._ball_position[1] - self._hole_position[1] <= 1:
            return True
        return False
