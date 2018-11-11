import numpy as np

from .sampler import get_uniform_sampler
from .agent import Agent

SPACE = 0
GARBAGE = 1
WALL = -1  # used as return code


class Game(object):
    """Game object that contains game logic.

    Usage:
        > g = Game(...)
        > obs = g.reset()
        > while not g.finished():
        >     act = your_bot(obs)
        >     obs = g.step(act)
        > garb_left, gathered = g.get_summary()
    """

    def __init__(self, max_episodes=100, gen_proba=0.5, dim=5, collide='sym'):
        """
        Arguments:
            max_episodes: Time length of game.
            gen_proba: Probability of new garbage appearance.
            dim: Map dimension. Map will be (dim x dim) size.
            collide: Collision behaviour. If 'sym' then agent will move
                in the opposite direction. If 'rand' then agent will move
                in random available direction.
        """

        assert dim > 1

        self.dim = dim
        self.agent = Agent(get_uniform_sampler(dim), self)
        self.map = None
        self.garbage_count = 0
        self.max_episodes = max_episodes
        self.episodes_left = 0
        self.p = gen_proba
        self.collide = collide

    def reset(self):
        """Restart the game.

        Returns: Initial observations of agent. See step() for details.
        """

        self.agent.reset()
        self.garbage_count = 0
        self.episodes_left = self.max_episodes
        self.map = [[SPACE for _ in range(self.dim)] for _ in range(self.dim)]

        return self._get_obs()

    def is_oob(self, i, j):
        return not (0 <= i < self.dim and 0 <= j < self.dim)

    def gather(self, i, j):
        if self.map[i][j] == GARBAGE:
            self.map[i][j] = SPACE
            self.garbage_count -= 1
            return 1
        else:
            return 0

    def finished(self):
        return not self.episodes_left > 0

    def get_summary(self):
        """Get game session results.

        Returns: Count of garbage that left on map,
                 Count of garbage that was gathered during the game.
        """

        return self.garbage_count, self.agent.gathered

    def step(self, action=None):
        """Perform action, update environment and get observations.

        Arguments:
            action: Action for agent to perform.
                Could be int (0 - left, 1 - right, 2 - down, 3 - up),
                str ('left', 'right', 'down', 'up') or None (move in
                random direction). Default: None.

        Returns: np.ndarray of shape (4,)
                 e.g [W00]
                     [WA1]
                     [W10],
                 where A-agent, W-wall, 0-space, 1-garbage.
                 In this case array([-1, 1, 1, 0]) will be returned.
        """

        if self.finished():
            raise ValueError("The game is finished.")
        # Agent acts first.
        self.agent.move(action)

        # With proba `p` new garbage is generated
        if self.p >= np.random.random_sample():
            self._generate_garbage()

        # Decrement episodes number
        self.episodes_left -= 1

        # Return LRUD cells' info
        return self._get_obs()

    def _get_obs(self):
        nb = self.agent.get_observations()
        obs = np.zeros(4)
        for ind, (i, j) in enumerate(nb):
            obs[ind] = WALL if self.is_oob(i, j) else self.map[i][j]

        return obs

    def _generate_garbage(self):
        if self.garbage_count < self.dim**2 - 1:  # -1 for agent
            free = [(i, j) for i in range(self.dim) \
                    for j in range(self.dim)  \
                    if self.map[i][j] == SPACE \
                    and (self.agent.i != i \
                    or self.agent.j != j)]
            i, j = free[np.random.randint(low=0, high=len(free))]
            self.map[i][j] = GARBAGE
            self.garbage_count += 1
