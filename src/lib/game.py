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
    server_data = None
    running = False
    sleep_idle = True
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
            clock.schedule(self.update_server_data)

    def draw(self):
        sleep_time = clock.get_sleep_time(self.sleep_idle)
        self.debug_text.text = \
            f"FPS: {round(clock.get_fps(), 2)}"
        if self.multiplayer_mode:
            self.draw_multiplayer()
        else:
            self.draw_singleplayer()

    def run(self):
        if not self.running:
            if self.primary_client:
                clock.schedule_interval(self.ball.moving, .005)
            self.running = True

    def pause(self):
        if self.running:
            if self.primary_client:
                clock.unschedule(self.ball.moving)
            self.running = False

    def load_sprites(self):
        self.debug_text = pyglet.text.Label('Debug!', font_size=10, x=0, y=settings.WINDOW_HEIGHT, anchor_x='left', anchor_y='top')
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
            if not self.running:
                self.score.text = 'I\'m primary'
        else:
            self.racket_me = self.racket_right
            self.racket_vs = self.racket_left
            if not self.running:
                self.score.text = 'I\'m secondary'

    def on_collision(self):
        player = self.ball.check_collision([self.racket_left, self.racket_right])
        if player:
            self.ball.hit_racket(player is self.racket_left)
            player.increase_score()
            self.ball.prevent_stick(player)
        if self.ball.check_collision_laterals(settings.WINDOW_HEIGHT):
            self.ball.hit_lateral()

    def update_server_data(self, dt):
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
        if self.primary_client:
            data['score'] = [self.racket_left.SCORE, self.racket_right.SCORE]
        self.conn.send(simplejson.dumps(data).encode('utf-8'))
        self.server_data = simplejson.loads(self.conn.recv(2000).decode('utf-8'))
        return self.server_data

    def update_multiplayer_positions(self, data):
        for playerid in data.keys():
            if playerid != self.me:
                player_data = data[playerid]
                if 'racket' in player_data:
                    self.racket_vs.x = player_data['racket']['x']
                    self.racket_vs.y = player_data['racket']['y']
                if not self.primary_client and 'ball' in player_data:
                    self.ball.x = player_data['ball']['x']
                    self.ball.y = player_data['ball']['y']
                if 'score' in player_data:
                    self.racket_left.SCORE = player_data['score'][0]
                    self.racket_right.SCORE = player_data['score'][1]

    def draw_multiplayer(self):
        self.define_players(self.server_data)

        if len(self.server_data.keys()) == 2:
            self.run()
        else:
            self.pause()

        if self.primary_client:
            self.on_collision()

        if self.running:
            self.score.text = f"{self.racket_left.SCORE} : {self.racket_right.SCORE}"

        self.update_multiplayer_positions(self.server_data)

    def draw_singleplayer(self):
        self.run()
        self.on_collision()
