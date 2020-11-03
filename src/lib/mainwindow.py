import simplejson, socket, sys, pyglet
from . import settings
from . import game

class MainWindow(pyglet.window.Window):
    keys = None
    game = None

    def __init__(self, *args, **kwargs):
        pyglet.window.Window.__init__(self, *args, **kwargs)
        self.game = game.Game(multiplayer_mode=True)
        self.keys = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keys)

    def move_racket(self, dx, dy):
        racket = self.game.racket_me
        racket.move(0, dy, y_bounds=(0, settings.WINDOW_HEIGHT - racket.height))

    def parse_keys(self):
        dy = (settings.MOVE_SPEED if self.keys[pyglet.window.key.UP] else 0) \
            + (-settings.MOVE_SPEED if self.keys[pyglet.window.key.DOWN] else 0)
        self.move_racket(0, dy)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.move_racket(scroll_x * settings.MOVE_SPEED, scroll_y * settings.MOVE_SPEED)

    def on_draw(self):
        self.clear()
        self.parse_keys()

        self.game.draw()

        self.game.debug_text.draw()
        self.game.ball.draw()
        self.game.score.draw()
        self.game.racket_left.draw()
        self.game.racket_right.draw()
