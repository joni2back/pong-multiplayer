import socket, sys
import pyglet, simplejson
from pyglet import clock
from . import settings
from .racket import Racket
from .ball import Ball

def connect():
    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((settings.SERVER_IP, settings.SERVER_PORT))
        me = str(conn.getsockname()[1])
        print(f"Client connected to {settings.SERVER_IP}:{settings.SERVER_PORT} with id: {me}")
        return [me, conn]
    except socket.error:
        print("Couldn't connect to game server in: {settings.SERVER_IP}:{settings.SERVER_PORT}")
        sys.exit(1)

class Game(pyglet.window.Window):
    running = False
    racket_left = None
    racket_right = None
    racket_me = None
    score = None
    primary_client = False
    multiplayer_mode = False

    def __init__(self, multiplayer_mode = False):
        self.load_sprites()
        self.multiplayer_mode = multiplayer_mode
        if self.multiplayer_mode:
            self.me, self.conn = connect()

    def draw(self):
        self.debug_text.text = \
            f"FPS: {clock.get_fps()}, SleepTime: {clock.get_sleep_time(True)}"
        if self.multiplayer_mode:
            self.draw_multiplayer()
        else:
            self.draw_singleplayer()

    def run(self):
        if not self.running:
            clock.schedule_interval(self.ball.moving, .005)
            self.running = True

    def pause(self):
        if self.running:
            clock.unschedule(self.ball.moving)
            self.running = False

    def load_sprites(self):
        self.debug_text = pyglet.text.Label("FPS: ?, SleepTime: ?", font_size=10, x=0, y=settings.WINDOW_HEIGHT, anchor_x='left', anchor_y='top')
        self.score = pyglet.text.Label('', font_size=15, x=settings.WINDOW_WIDTH/2, y=settings.WINDOW_HEIGHT - 15, anchor_x='center', anchor_y='center')
        self.racket_left = Racket(pyglet.resource.image(settings.RACKET_IMG)).center_anchor_y(settings.WINDOW_HEIGHT)
        self.racket_right = Racket(pyglet.resource.image(settings.RACKET_IMG)).center_anchor_y(settings.WINDOW_HEIGHT)
        self.ball = Ball(pyglet.resource.image(settings.BALL_IMG)).center_anchor_y(settings.WINDOW_HEIGHT).center_anchor_x(settings.WINDOW_WIDTH)
        self.racket_right.x = settings.WINDOW_WIDTH - self.racket_right.width
        self.racket_me = self.racket_left

    def define_players(self, server_response):
        if self.me == sorted(server_response.keys())[0]: # the first client connection
            self.primary_client = True
            self.racket_me = self.racket_left
            self.racket_vs = self.racket_right
            self.score.text = 'I\'m primary'
        else:
            self.racket_me = self.racket_right
            self.racket_vs = self.racket_left
            self.score.text = 'I\'m secondary'

    def on_collision(self):
        player = self.ball.check_collision([self.racket_left, self.racket_right])
        if player:
            self.ball.hit_racket()
            player.increase_score()
            self.ball.prevent_stick(player)
        if self.ball.check_collision_laterals(settings.WINDOW_HEIGHT):
            self.ball.hit_lateral()

    def update_server_data(self):
        data = {
            "ball": {
                "x": self.ball.x,
                "y": self.ball.y,
            },
            "racket": {
                "x": self.racket_me.x,
                "y": self.racket_me.y,
            }
        }
        self.conn.send(simplejson.dumps(data).encode('utf-8'))
        return simplejson.loads(self.conn.recv(2000).decode('utf-8'))

    def update_multiplayer_positions(self, data):
        for playerid in data.keys():
            try:
                if playerid != self.me:
                    self.racket_vs.y = data[playerid]['racket']['y']
                    if not self.primary_client:
                        self.ball.x = data[playerid]['ball']['x']
                        self.ball.y = data[playerid]['ball']['y']
            except:
                pass

    def draw_multiplayer(self):
        data = self.update_server_data()
        self.define_players(data)

        if self.primary_client:
            if len(data.keys()) == 2:
                self.run()
            else:
                self.pause()

        if self.primary_client:
            self.on_collision()

        self.update_multiplayer_positions(data)

    def draw_singleplayer(self):
        self.run()
        self.on_collision()
