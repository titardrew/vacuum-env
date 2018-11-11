import sys
import os

SYMB = {0: ' ', 1: '*'} 


class TerminalVisualizer(object):
    def __init__(self, game):
        self.game = game

    def render(self):
        os.system('clear')
        sys.stdout.flush()

        map_to_vis = self.game.map.copy()

        for i, row in enumerate(self.game.map):
            out = ''
            for j, s in enumerate(row):
                if i == self.game.agent.i and j == self.game.agent.j:
                    out += 'A'
                else:
                    out += SYMB[s]
            sys.stdout.write(out + '\n')

    def close(self):
        os.system('clear')
        sys.stdout.write('Game over!')
