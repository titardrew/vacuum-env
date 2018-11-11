import pyglet
from pyglet.gl import *

map_col = {2: (200, 0, 0),
           1: (0, 200, 0),
           0: (250, 250, 250)}

wh = {'small': (200, 200),
      'medium': (400, 400),
      'large': (800, 800),
      'huge': (1200, 1200)}


class WindowVisualizer(pyglet.window.Window):
    def __init__(self, game, size='small'):

        width, height = wh[size]
        pyglet.window.Window.__init__(self, width=width, height=height,
                               fullscreen=False)

        self.cell_size = width // game.dim
        self.screen_width = width
        self.screen_height = height
        self.columns = width // self.cell_size
        self.rows = height // self.cell_size
        self.cells_vertex_list = []
        self.game = game
        self.grid_batch = pyglet.graphics.Batch()

        self._initialize()
        self._draw_grid()


    def _initialize(self):
        gl.glClearColor(0, 0, 0, 1)
        _map = self.game.map
        for row in range(self.game.dim):
            self.cells_vertex_list.append([])
            for col in range(self.game.dim):
                cell = self.cell_position(col, row)
                self.cells_vertex_list[row].append(cell)

    def translate(self, pixel_x, pixel_y):
        """Translate pixel coordinates (pixel_x,pixel_y) into grid coords"""
        x = pixel_x * self.columns // self.screen_width
        y = pixel_y * self.rows // self.screen_height
        return x, y

    def cell_position(self, col, row):
        x1, y1 = col * self.cell_size, row * self.cell_size
        x2, y2 = col * self.cell_size + self.cell_size, \
            row * self.cell_size + self.cell_size
        return (x1, y1, x2, y2)

    def _draw_grid(self):
        # Horizontal lines
        for i in range(self.rows):
            self.grid_batch.add(2, gl.GL_LINES, None, ('v2i',
                                                       (0,
                                                        i * self.cell_size,
                                                        self.screen_width,
                                                        i * self.cell_size)))
        # Vertical lines
        for j in range(self.columns + 1):
            self.grid_batch.add(2, gl.GL_LINES, None, ('v2i',
                                                       (j * self.cell_size,
                                                        0,
                                                        j * self.cell_size,
                                                        self.screen_height)))

    def render(self):
        self.clear()
        self.switch_to()
        self.dispatch_events()
        self.draw()
        gl.glColor4f(0.03, 0.03, 0.03, 1.0)
        self.grid_batch.draw()
        self.flip()

    def draw(self):
        _map = self.game.map
        gl.glBegin(gl.GL_QUADS)
        for row in range(self.game.dim):
            for col in range(self.game.dim):
                if row == self.game.agent.i \
                        and col == self.game.agent.j:
                    r, g, b = map_col[2]
                else:
                    r, g, b = map_col[_map[row][col]]
                gl.glColor4f(r, g, b, 1.0)
                x1, y1, x2, y2 = self.cells_vertex_list[row][col]
                gl.glVertex2f(x1, y1)
                gl.glVertex2f(x1, y2)
                gl.glVertex2f(x2, y2)
                gl.glVertex2f(x2, y1)
        gl.glEnd()

        gathered = self.game.agent.gathered
        garb = self.game.garbage_count
        left = self.game.episodes_left

        label = pyglet.text.Label('Gath: %s, Garb_cur: %s, Epis_left: %s'
                                  % (gathered, garb, left),
                                  font_size=8,
                                  color=(0, 0, 0, 255),
                                  x=self.cell_size // 3, y=10,
                                  anchor_x='left', anchor_y='center')
        label.draw()
