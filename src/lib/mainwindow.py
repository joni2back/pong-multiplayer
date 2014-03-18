import simplejson, socket
import pyglet
import settings
from racket import Racket
from ball import Ball



def forward():
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(('192.168.1.43', 50090))
    _id = str(conn.getsockname()[1])
    print "Connected with _id: " + _id
    return [_id, conn]


class MainWindow(pyglet.window.Window):
    keys = None

    def __init__(self, *args, **kwargs):
        pyglet.window.Window.__init__(self, *args, **kwargs)
        self.keys = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keys)

        self.racket_img = pyglet.resource.image(settings.RACKET_IMG)
        self.ball_img = pyglet.resource.image(settings.BALL_IMG)

        self.racket = Racket(self.racket_img).center_anchor_y(settings.WINDOW_HEIGHT)

        self.racket_opponent = Racket(self.racket_img).center_anchor_y(settings.WINDOW_HEIGHT)
        self.racket_opponent.x = settings.WINDOW_WIDTH - self.racket_img.width

        self.ball = Ball(self.ball_img).center_anchor_y(settings.WINDOW_HEIGHT).center_anchor_x(settings.WINDOW_WIDTH)
        self.score = pyglet.text.Label('', font_size=15, x=settings.WINDOW_WIDTH/2, y=settings.WINDOW_HEIGHT - 15, anchor_x='center', anchor_y='center')

        self.me, self.conn = forward()

        pyglet.clock.schedule_interval(self.ball.moving, .005) 


    def on_draw(self):
        self.clear()

        player = self.ball.check_collision([self.racket, self.racket_opponent])
        if player:
            self.ball.hit_racket()
            player.increase_score()

        if self.keys[pyglet.window.key.UP] and self.racket.y < settings.WINDOW_HEIGHT:
            self.racket.move(0, settings.MOVE_SPEED)
            
        if self.keys[pyglet.window.key.DOWN] and self.racket.y > 0:
            self.racket.move(0, -settings.MOVE_SPEED)


        if self.keys[pyglet.window.key.NUM_7] and self.racket_opponent.y < settings.WINDOW_HEIGHT:
            self.racket_opponent.move(0, settings.MOVE_SPEED)
            
        if self.keys[pyglet.window.key.NUM_1] and self.racket_opponent.y > 0:
            self.racket_opponent.move(0, -settings.MOVE_SPEED)

        self.score.text = 'Me: %d  -   Opponent: %d' % (self.racket.SCORE, self.racket_opponent.SCORE)

        self.score.draw()
        self.racket.draw()
        
        self.ball.draw()

        data = simplejson.dumps({
            "racket": {
                "x": self.racket.x,
                "y": self.racket.y,
            },
            "ball": {
                "x": self.ball.x,
                "y": self.ball.y,
            }
        })
        self.conn.send(data)
        data = simplejson.loads(self.conn.recv(2000))

        for playerid in data.keys():
            if playerid != self.me:# and playerid not in self.players_id:
                try:
                    self.racket_opponent.y = data[playerid]['racket']['y']
                except:
                    pass
            self.racket_opponent.draw()

