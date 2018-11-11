import numpy as np

# right, left, down, up
NB = [(0, 1), (0, -1), (1, 0), (-1, 0)]


class Agent(object):
    def __init__(self, init_place_sampler, game):
        self.init_place_sampler = init_place_sampler
        self.i, self.j = 0, 0
        self.game = game
        self.gathered = 0

        self.reset()

    def reset(self):
        self.i, self.j = self.init_place_sampler()
        self.gathered = 0

    def move(self, direct=None):
        if direct is None:
            n_dir = np.random.randint(low=0, high=3+1)
        elif isinstance(direct, int):
            n_dir = direct
        elif isinstance(direct, str):
            n_dir = {'right': 0,
                     'left': 1,
                     'down': 2,
                     'up': 3}[direct]
        else:
            raise ValueError("`direct` could be None, str or int.")

        di, dj = NB[n_dir]

        if not self.game.is_oob(self.i + di, self.j + dj):
            self.i += di
            self.j += dj
        elif self.game.collide == 'sym':
            self.i -= di
            self.j -= dj
        elif self.game.collide == 'rand':
            self.move()

        self.gathered += self.game.gather(self.i, self.j)

    def get_observations(self):
        return [(self.i + di, self.j + dj) for (di, dj) in NB]
