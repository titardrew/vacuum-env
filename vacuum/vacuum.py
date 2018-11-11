import gym
import numpy as np
from core import Game
from gym import spaces
from time import sleep
from tqdm import tqdm
from vis import TerminalVisualizer, WindowVisualizer


class VacuumEnv(gym.Env):
    def __init__(self, size=8, max_episodes=100, gen_proba=0.5, collide='sym'):
        self.viewer = None
        self.done = None
        self.game = Game(max_episodes, gen_proba, size, collide)
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(0, 1, shape=(4,), dtype=np.uint8)

    def step(self, action=None):
        obs = self.game.step(action)
        self.done = self.game.finished()
        reward = -self.game.garbage_count if self.done else 0
        info = {'garbage_count': self.game.garbage_count,
                'gathered': self.game.agent.gathered, 
                'episodes_left': self.game.episodes_left}
        return np.array(obs), reward, self.done, info

    def reset(self):
        obs = self.game.reset()
        self.done = False
        return np.array(obs)

    def render(self, mode='window', size='small'):
        if self.viewer is None:
            if mode == 'window':
                self.viewer = WindowVisualizer(self.game, size)
            elif mode == 'terminal':
                self.viewer = TerminalVisualizer(self.game)

        self.viewer.render()

    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None
