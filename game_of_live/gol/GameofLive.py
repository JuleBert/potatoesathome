import imageio
import numpy as np


class GameOfLife(object):
    def __init__(self, width_height, square_size):
        self.square_size = square_size
        self.width_height = width_height
        self.field_width = int(width_height/square_size)
        self.state = [[0 for _ in range(self.field_width)] for _ in range(self.field_width)]
        self.images = []

    def create_gif(self, figures, steps, filename):
        for figure in figures:
            self.draw_figure(figure[0], figure[1])
        self.step(steps)
        self.print_me(filename)

    def draw_figure(self, figure, position):
        if figure == 'block':
            self.create_block(position[0],position[1])
        elif figure == 'beehive':
            self.create_beehive(position[0],position[1])
        elif figure == 'loaf':
            self.create_loaf(position[0],position[1])
        elif figure == 'boat':
            self.create_boat(position[0],position[1])
        elif figure == 'tub':
            self.create_tub(position[0],position[1])
        elif figure == 'big_square':
            self.create_big_square(position[0],position[1])
        elif figure == 'double_tub':
            self.create_double_tub(position[0],position[1])
        elif figure == 'blinker':
            self.create_blinker(position[0],position[1])
        elif figure == 'toad':
            self.create_toad(position[0],position[1])
        elif figure == 'beacon':
            self.create_beacon(position[0],position[1])
        elif figure == 'tripol':
            self.create_tripol(position[0],position[1])
        elif figure == 'pentadecathlon':
            self.create_pentadecathlon(position[0],position[1])
        elif figure == 'pulsar':
            self.create_pulsar(position[0],position[1])
        elif figure == 'glider':
            self.create_glider(position[0],position[1])
        elif figure == 'lwss':
            self.create_lwss(position[0],position[1])
        elif figure == 'mwss':
            self.create_mwss(position[0],position[1])
        elif figure == 'hwss':
            self.create_hwss(position[0],position[1])
        elif figure == 'giant':
            self.create_giant(position[0],position[1])
        elif figure == 'r_pentomino':
            self.create_r_pentomino(position[0],position[1])
        elif figure == 'die_hard':
            self.create_die_hard(position[0],position[1])
        elif figure == 'acorn':
            self.create_acorn(position[0],position[1])
        elif figure == 'surprise':
            self.create_surprise(position[0],position[1])
        elif figure == 'gosper_glider_gun':
            self.create_gosper_glider_gun(position[0],position[1])
        elif figure == 'block_laying_engine_1':
            self.create_block_laying_engine_1(position[0],position[1])
        elif figure == 'block_laying_engine_2':
            self.create_block_laying_engine_2(position[0],position[1])
        elif figure == 'block_laying_engine_3':
            self.create_block_laying_engine_3(position[0],position[1])

    def draw_grid(self, im):
        x_max = len(im[0])
        y_max = len(im)
        for x in range(x_max):
            for y in range(0, y_max, self.square_size):
                im[y][x] = 0
        for y in range(y_max):
            for x in range(0, x_max, self.square_size):
                im[y][x] = 0

    def fill_square(self, im, position):
        check_position(position)
        if (position[0] == 0) or (position[0] == self.field_width) or (position[1] == 0) or (position[1] == self.field_width):
            pass
        for x in range(position[1]*self.square_size, (position[1] + 1 ) * self.square_size):
            for y in range(position[0]*self.square_size, (position[0] + 1 ) * self.square_size):
                im[y][x] = 0

    def fill_gray_square(self, im, position):
        for x in range(position[1]*self.square_size, (position[1] + 1 ) * self.square_size):
            for y in range(position[0]*self.square_size, (position[1] + 1 ) * self.square_size):
                im[y][x] = 200

    def gray_border(self, im):
        for x in range(self.field_width):
            self.fill_gray_square(im, [x, 0])
        for x in range(self.field_width):
            self.fill_gray_square(im, [x, self.field_width - 1])
        for y in range(self.field_width):
            self.fill_gray_square(im, [0, y])
        for y in range(self.field_width):
            self.fill_gray_square(im, [self.field_width - 1, y])

    def paint_field(self, border=False, grid=False):
        im = np.ones([self.width_height, self.width_height])
        im = im * 255
        if border:
            self.gray_border(im)
        if grid:
            self.draw_grid(im)
        for i in range(len(self.state)):
            for j in range(len(self.state[i])):
                if self.state[j][i] == 1:
                    self.fill_square(im, [i,j])
        return im

    def step(self, step_number, print_jpg = False):
        self.images.append(self.paint_field())
        if step_number > 0:
            for _ in range(step_number):
                # return_state = self.state
                return_state = [[y for y in x] for x in self.state]
                for i in range(1, len(self.state) - 1):
                    for j in range(1, len(self.state[i]) - 1):
                        # a1 = self.state[j-1][i-1]
                        # a2 = self.state[j-1][i]
                        # a3 = self.state[j-1][i+1]
                        # a4 = self.state[j][i-1]
                        # a5 = self.state[j][i+1]
                        # a6 = self.state[j+1][i-1]
                        # a7 = self.state[j+1][i]
                        # a8 = self.state[j+1][i+1]
                        neighbor_sum = self.state[j-1][i-1] + \
                                       self.state[j-1][i] + \
                                       self.state[j-1][i+1] + \
                                       self.state[j][i-1] + \
                                       self.state[j][i+1] + \
                                       self.state[j+1][i-1] + \
                                       self.state[j+1][i] + \
                                       self.state[j+1][i+1]
                        if self.state[j][i] == 1:
                            if neighbor_sum < 2:
                                return_state[j][i] = 0
                            if neighbor_sum > 3:
                                return_state[j][i] = 0
                        else:
                            if neighbor_sum == 3:
                                return_state[j][i] = 1
                self.state = return_state
                my_var = self.paint_field()
                self.images.append(my_var)
                if print_jpg:
                    imageio.imwrite('step' + str(_) + '.jpg', my_var)

    def print_me(self, file_name):
        # Generate GIF
        imageio.mimsave(file_name, self.images)

    # still lifes
    def create_block(self, x, y):
        check_position([x, y])
        self.state[x][y] = 1
        self.state[x+1][y] = 1
        self.state[x][y+1] = 1
        self.state[x+1][y+1] = 1

    def create_beehive(self, x, y):
        check_position([x, y])
        self.state[x+1][y] = 1
        self.state[x][y+1] = 1
        self.state[x+2][y+1] = 1
        self.state[x][y+2] = 1
        self.state[x + 2][y + 2] = 1
        self.state[x+1][y+3] = 1

    def create_loaf(self, x, y):
        check_position([x, y])
        self.state[x + 1][y] = 1
        self.state[x + 2][y] = 1
        self.state[x][y + 1] = 1
        self.state[x + 3][y + 1] = 1
        self.state[x + 1][y + 2] = 1
        self.state[x + 3][y + 2] = 1
        self.state[x + 2][y + 3] = 1

    def create_boat(self, x, y):
        check_position([x, y])
        self.state[x][y] = 1
        self.state[x+1][y] = 1
        self.state[x+2][y+1] = 1
        self.state[x][y + 1] = 1
        self.state[x + 1][y + 2] = 1

    def create_tub(self, x, y):
        check_position([x, y])
        self.state[x][y + 1] = 1
        self.state[x + 1][y] = 1
        self.state[x + 1][y + 2] = 1
        self.state[x + 2][y + 1] = 1

    def create_big_square(self, x, y):
        check_position([x, y])
        self.state[x + 1][y] = 1
        self.state[x + 2][y] = 1
        self.state[x][y + 1] = 1
        self.state[x + 3][y + 1] = 1
        self.state[x][y + 2] = 1
        self.state[x + 3][y + 2] = 1
        self.state[x][y + 3] = 1
        self.state[x + 3][y + 3] = 1

    def create_double_tub(self, x, y):
        check_position([x, y])
        self.state[x][y + 2] = 1
        self.state[x + 1][y + 1] = 1
        self.state[x + 1][y + 3] = 1
        self.state[x + 2][y] = 1
        self.state[x + 2][y + 2] = 1
        self.state[x + 3][y + 1] = 1

    # Oscillators
    def create_blinker(self, x, y):
        check_position([x, y])
        self.state[x][y] = 1
        self.state[x][y+1] = 1
        self.state[x][y+2] = 1

    def create_toad(self, x, y):
        check_position([x, y])
        self.state[x+1][y] = 1
        self.state[x+2][y] = 1
        self.state[x+3][y] = 1
        self.state[x][y+1] = 1
        self.state[x+1][y + 1] = 1
        self.state[x+2][y + 1] = 1

    def create_beacon(self, x, y):
        check_position([x, y])
        self.state[x][y] = 1
        self.state[x+1][y] = 1
        self.state[x][y+1] = 1
        self.state[x + 3][y + 2] = 1
        self.state[x+2][y+3] = 1
        self.state[x+3][y + 3] = 1

    def create_tripol(self, x, y):
        check_position([x, y])
        self.state[x][y] = 1
        self.state[x+1][y] = 1
        self.state[x][y+1] = 1
        self.state[x+2][y+1] = 1
        self.state[x+2][y+3] = 1
        self.state[x+4][y+3] = 1
        self.state[x+3][y+4] = 1
        self.state[x+4][y+4] = 1

    def create_pentadecathlon(self, x, y):
        check_position([x, y])
        self.state[x+1][y] = 1
        self.state[x + 1][y + 1] = 1
        self.state[x][y + 2] = 1
        self.state[x + 3][y + 2] = 1
        self.state[x + 1][y + 3] = 1
        self.state[x + 1][y + 4] = 1
        self.state[x + 1][y + 5] = 1
        self.state[x + 1][y + 6] = 1
        self.state[x][y + 7] = 1
        self.state[x + 3][y + 7] = 1
        self.state[x + 1][y + 8] = 1
        self.state[x + 1][y + 9] = 1

    def create_pulsar(self, x, y):
        check_position([x, y])
        # 1. Senkrechte
        self.state[x][y + 2] = 1
        self.state[x][y + 3] = 1
        self.state[x][y + 4] = 1
        self.state[x][y + 8] = 1
        self.state[x][y + 9] = 1
        self.state[x][y + 10] = 1
        # 2. Senkrechte
        self.state[x + 5][y + 2] = 1
        self.state[x + 5][y + 3] = 1
        self.state[x + 5][y + 4] = 1
        self.state[x + 5][y + 8] = 1
        self.state[x + 5][y + 9] = 1
        self.state[x + 5][y + 10] = 1
        # 3.Senkrechte
        self.state[x + 7][y + 2] = 1
        self.state[x + 7][y + 3] = 1
        self.state[x + 7][y + 4] = 1
        self.state[x + 7][y + 8] = 1
        self.state[x + 7][y + 9] = 1
        self.state[x + 7][y + 10] = 1
        # 4. Senkrechte
        self.state[x + 12][y + 2] = 1
        self.state[x + 12][y + 3] = 1
        self.state[x + 12][y + 4] = 1
        self.state[x + 12][y + 8] = 1
        self.state[x + 12][y + 9] = 1
        self.state[x + 12][y + 10] = 1
        # 1. Waagerechte
        self.state[x + 2][y] = 1
        self.state[x + 3][y] = 1
        self.state[x + 4][y] = 1
        self.state[x + 8][y] = 1
        self.state[x + 9][y] = 1
        self.state[x + 10][y] = 1
        # 2. Waagerechte
        self.state[x + 2][y + 5] = 1
        self.state[x + 3][y + 5] = 1
        self.state[x + 4][y + 5] = 1
        self.state[x + 8][y + 5] = 1
        self.state[x + 9][y + 5] = 1
        self.state[x + 10][y + 5] = 1
        # 3. Waagerechte
        self.state[x + 2][y + 7] = 1
        self.state[x + 3][y + 7] = 1
        self.state[x + 4][y + 7] = 1
        self.state[x + 8][y + 7] = 1
        self.state[x + 9][y + 7] = 1
        self.state[x + 10][y + 7] = 1
        # 4. Waagerechte
        self.state[x + 2][y + 12] = 1
        self.state[x + 3][y + 12] = 1
        self.state[x + 4][y + 12] = 1
        self.state[x + 8][y + 12] = 1
        self.state[x + 9][y + 12] = 1
        self.state[x + 10][y + 12] = 1

    # Spaceships
    def create_glider(self, x, y):
        check_position([x, y])
        self.state[x+1][y] = 1
        self.state[x+2][y+1] = 1
        self.state[x][y+2] = 1
        self.state[x+1][y+2] = 1
        self.state[x+2][y+2] = 1

    def create_lwss(self, x, y):
        check_position([x, y])
        self.state[x][y + 1] = 1
        self.state[x][y + 3] = 1
        self.state[x + 1][y] = 1
        self.state[x + 2][y] = 1
        self.state[x + 3][y] = 1
        self.state[x + 3][y + 3] = 1
        self.state[x + 4][y] = 1
        self.state[x + 4][y + 1] = 1
        self.state[x + 4][y + 2] = 1

    def create_mwss(self, x, y):
        check_position([x, y])
        self.state[x][y + 1] = 1
        self.state[x][y + 3] = 1
        self.state[x + 1][y] = 1
        self.state[x + 2][y] = 1
        self.state[x + 3][y] = 1
        self.state[x + 3][y + 4] = 1
        self.state[x + 4][y] = 1
        self.state[x + 5][y] = 1
        self.state[x + 5][y + 3] = 1
        self.state[x + 6][y] = 1
        self.state[x + 6][y + 1] = 1
        self.state[x + 6][y + 2] = 1

    def create_hwss(self, x, y):
        check_position([x, y])
        self.state[x][y + 1] = 1
        self.state[x][y + 3] = 1
        self.state[x + 1][y] = 1
        self.state[x + 2][y] = 1
        self.state[x + 2][y + 4] = 1
        self.state[x + 3][y] = 1
        self.state[x + 3][y + 4] = 1
        self.state[x + 4][y] = 1
        self.state[x + 5][y] = 1
        self.state[x + 5][y + 3] = 1
        self.state[x + 6][y] = 1
        self.state[x + 6][y + 1] = 1
        self.state[x + 6][y + 2] = 1

    # others
    def create_giant(self, x, y):
        check_position([x, y])
        self.state[x][y] = 1
        self.state[x+1][y] = 1
        self.state[x+2][y] = 1
        self.state[x][y + 1] = 1
        self.state[x+2][y + 1] = 1
        self.state[x][y + 2] = 1
        self.state[x+2][y + 2] = 1
        self.state[x][y + 4] = 1
        self.state[x+2][y + 4] = 1
        self.state[x][y + 5] = 1
        self.state[x+2][y + 5] = 1
        self.state[x][y + 6] = 1
        self.state[x+1][y + 6] = 1
        self.state[x+2][y + 6] = 1

    def create_r_pentomino(self, x, y):
        check_position([x, y])
        self.state[x + 1][y] = 1
        self.state[x + 2][y] = 1
        self.state[x][y + 1] = 1
        self.state[x + 1][y + 1] = 1
        self.state[x + 1][y + 2] = 1

    def create_die_hard(self, x, y):
        check_position([x, y])
        self.state[x + 6][y] = 1
        self.state[x][y + 1] = 1
        self.state[x + 1][y + 1] = 1
        self.state[x + 1][y + 2] = 1
        self.state[x + 5][y + 2] = 1
        self.state[x + 6][y + 2] = 1
        self.state[x + 7][y + 2] = 1

    def create_acorn(self, x, y):
        check_position([x, y])
        self.state[x + 1][y] = 1
        self.state[x + 3][y + 1] = 1
        self.state[x][y + 2] = 1
        self.state[x + 1][y + 2] = 1
        self.state[x + 4][y + 2] = 1
        self.state[x + 5][y + 2] = 1
        self.state[x + 6][y + 2] = 1

    def create_surprise(self, x, y):
        check_position([x, y])
        self.state[x][y + 4] = 1
        self.state[x + 1][y + 4] = 1
        self.state[x][y + 5] = 1
        self.state[x + 1][y + 5] = 1
        self.state[x + 10][y + 4] = 1
        self.state[x + 10][y + 5] = 1
        self.state[x + 10][y + 6] = 1
        self.state[x + 11][y + 3] = 1
        self.state[x + 11][y + 7] = 1
        self.state[x + 12][y + 2] = 1
        self.state[x + 12][y + 8] = 1
        self.state[x + 13][y + 2] = 1
        self.state[x + 13][y + 8] = 1
        self.state[x + 14][y + 5] = 1

    def create_gosper_glider_gun(self, x, y):
        check_position([x, y])
        self.state[x][y + 4] = 1
        self.state[x + 1][y + 4] = 1
        self.state[x][y + 5] = 1
        self.state[x + 1][y + 5] = 1
        self.state[x + 10][y + 4] = 1
        self.state[x + 10][y + 5] = 1
        self.state[x + 10][y + 6] = 1
        self.state[x + 11][y + 3] = 1
        self.state[x + 11][y + 7] = 1
        self.state[x + 12][y + 2] = 1
        self.state[x + 12][y + 8] = 1
        self.state[x + 13][y + 2] = 1
        self.state[x + 13][y + 8] = 1
        self.state[x + 14][y + 5] = 1
        self.state[x + 15][y + 3] = 1
        self.state[x + 15][y + 7] = 1
        self.state[x + 16][y + 4] = 1
        self.state[x + 16][y + 5] = 1
        self.state[x + 16][y + 6] = 1
        self.state[x + 17][y + 5] = 1
        self.state[x + 20][y + 2] = 1
        self.state[x + 20][y + 3] = 1
        self.state[x + 20][y + 4] = 1
        self.state[x + 21][y + 2] = 1
        self.state[x + 22][y + 3] = 1
        self.state[x + 23][y + 4] = 1
        self.state[x + 24][y + 1] = 1
        self.state[x + 24][y + 5] = 1
        self.state[x + 26][y] = 1
        self.state[x + 26][y + 1] = 1
        self.state[x + 26][y + 5] = 1
        self.state[x + 26][y + 6] = 1
        self.state[x + 36][y + 2] = 1
        self.state[x + 36][y + 3] = 1
        self.state[x + 37][y + 2] = 1
        self.state[x + 37][y + 3] = 1

    def create_block_laying_engine_1(self, x, y):
        check_position([x, y])
        self.state[x][y + 6] = 1
        self.state[x + 2][y + 5] = 1
        self.state[x + 2][y + 6] = 1
        self.state[x + 4][y + 1] = 1
        self.state[x + 4][y + 2] = 1
        self.state[x + 4][y + 3] = 1
        self.state[x + 5][y] = 1
        self.state[x + 5][y + 1] = 1
        self.state[x + 5][y + 2] = 1
        self.state[x + 6][y + 1] = 1

    def create_block_laying_engine_2(self, x, y):
        check_position([x, y])
        self.state[x][y] = 1
        self.state[x][y + 1] = 1
        self.state[x][y + 4] = 1
        self.state[x + 1][y] = 1
        self.state[x + 1][y + 3] = 1
        self.state[x + 2][y] = 1
        self.state[x + 2][y + 3] = 1
        self.state[x + 2][y + 4] = 1
        self.state[x + 3][y + 2] = 1
        self.state[x + 4][y] = 1
        self.state[x + 4][y + 2] = 1
        self.state[x + 4][y + 3] = 1
        self.state[x + 4][y + 4] = 1

    def create_block_laying_engine_3(self, x, y):
        check_position([x, y])
        self.state[x][y] = 1
        self.state[x + 1][y] = 1
        self.state[x + 2][y] = 1
        self.state[x + 3][y] = 1
        self.state[x + 4][y] = 1
        self.state[x + 5][y] = 1
        self.state[x + 6][y] = 1
        self.state[x + 7][y] = 1
        self.state[x + 9][y] = 1
        self.state[x + 10][y] = 1
        self.state[x + 11][y] = 1
        self.state[x + 12][y] = 1
        self.state[x + 13][y] = 1
        self.state[x + 17][y] = 1
        self.state[x + 18][y] = 1
        self.state[x + 19][y] = 1
        self.state[x + 26][y] = 1
        self.state[x + 27][y] = 1
        self.state[x + 28][y] = 1
        self.state[x + 29][y] = 1
        self.state[x + 30][y] = 1
        self.state[x + 31][y] = 1
        self.state[x + 32][y] = 1
        self.state[x + 34][y] = 1
        self.state[x + 35][y] = 1
        self.state[x + 36][y] = 1
        self.state[x + 37][y] = 1
        self.state[x + 38][y] = 1


def check_position(position):
    if (len(position) != 2) or (type(position[0]) != int) or (type(position[1]) != int):
        raise ValueError('Falsche Position')
