import simplejson, socket, sys, pyglet
import settings
from racket import Racket
from ball import Ball

def connect():
    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((settings.SERVER_IP, settings.SERVER_PORT))
        me = str(conn.getsockname()[1])
        print "Client connected to %s:%s with id: %s" % (settings.SERVER_IP, settings.SERVER_PORT, me)
        return [me, conn]
    except socket.error:
        print "Couldn't connect to game server in: %s:%s" % (settings.SERVER_IP, settings.SERVER_PORT)
        sys.exit(1)

class MainWindow(pyglet.window.Window):
    keys = None
    running = False
    racket_left = None
    racket_right = None
    racket_me = None
    score = None
    master_client = False

    def __init__(self, *args, **kwargs):
        self.me, self.conn = connect()
        pyglet.window.Window.__init__(self, *args, **kwargs)
        self.load_sprites()
        self.keys = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keys)

    def run(self):
        if not self.running:
            pyglet.clock.schedule_interval(self.ball.moving, .005)
            self.running = True

    def pause(self):
        if self.running:
            pyglet.clock.unschedule(self.ball.moving)
            self.running = False

    def load_sprites(self):
        self.score = pyglet.text.Label('', font_size=15, x=settings.WINDOW_WIDTH/2, y=settings.WINDOW_HEIGHT - 15, anchor_x='center', anchor_y='center')
        self.racket_left = Racket(pyglet.resource.image(settings.RACKET_IMG)).center_anchor_y(settings.WINDOW_HEIGHT)
        self.racket_right = Racket(pyglet.resource.image(settings.RACKET_IMG)).center_anchor_y(settings.WINDOW_HEIGHT)
        self.ball = Ball(pyglet.resource.image(settings.BALL_IMG)).center_anchor_y(settings.WINDOW_HEIGHT).center_anchor_x(settings.WINDOW_WIDTH)
        self.racket_right.x = settings.WINDOW_WIDTH - self.racket_right.IMG.width
        self.racket_me = self.racket_left

    def define_players(self, server_response):
        if self.me == sorted(server_response.keys())[0]: #the first client connection
            self.master_client = True
            self.racket_me = self.racket_left
            self.racket_vs = self.racket_right
            self.score.text = 'Im master'
        else:
            self.racket_me = self.racket_right
            self.racket_vs = self.racket_left
            self.score.text = 'Im slave'

    def parse_keys(self):
        if self.keys[pyglet.window.key.UP] and self.racket_me.y < settings.WINDOW_HEIGHT:
            self.racket_me.move(0, settings.MOVE_SPEED)
            
        if self.keys[pyglet.window.key.DOWN] and self.racket_me.y > 0:
            self.racket_me.move(0, -settings.MOVE_SPEED)

    def on_draw(self):
        self.clear()

        if self.master_client:
            player = self.ball.check_collision([self.racket_left, self.racket_right])
            if player:
                self.ball.hit_racket()
                player.increase_score()
            if self.ball.check_collision_laterals(settings.WINDOW_HEIGHT):
                self.ball.hit_lateral()

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
        self.conn.send(simplejson.dumps(data))
        data = simplejson.loads(self.conn.recv(2000))
        self.define_players(data)

        if self.master_client:
            if len(data.keys()) == 2:
                self.run()
            else:
                self.pause()

        self.parse_keys()
        for playerid in data.keys():
            try:
                if playerid != self.me:
                    self.racket_vs.y = data[playerid]['racket']['y']
                    if not self.master_client:
                        self.ball.x = data[playerid]['ball']['x']
                        self.ball.y = data[playerid]['ball']['y']
            except:
                pass

        self.ball.draw()
        self.score.draw()
        self.racket_left.draw()
        self.racket_right.draw()

