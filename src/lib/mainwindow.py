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

    def parse_keys(self):
        racket = self.game.racket_me
        if self.keys[pyglet.window.key.UP] and racket.y < settings.WINDOW_HEIGHT - racket.height:
            racket.move(0, settings.MOVE_SPEED)

        if self.keys[pyglet.window.key.DOWN] and racket.y > 0:
            racket.move(0, -settings.MOVE_SPEED)

    def on_draw(self):
        self.clear()
        self.parse_keys()

        self.game.draw()

        self.game.debug_text.draw()
        self.game.ball.draw()
        self.game.score.draw()
        self.game.racket_left.draw()
        self.game.racket_right.draw()
