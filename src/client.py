#!/usr/bin/env python
#author Jonas Sciangula Street
import pyglet
import math
import socket
import simplejson

WINDOW_WIDTH = 320
WINDOW_HEIGHT = 200
MOVE_SPEED = 8

BALL_IMG = 'assets/ball.png'
RACKET_IMG = 'assets/racket.png'
resolution = (WINDOW_WIDTH, WINDOW_HEIGHT)
keys = pyglet.window.key.KeyStateHandler()

pyglet.options['debug_gl'] = True
pyglet.options['debug_gl_trace'] = True
pyglet.options['debug_gl'] = True


class SprObj(pyglet.sprite.Sprite):

    ROTATION = 0
    SPEED = 0
    IMG = None

    def __init__(self, img, x=0, y=0, blend_src=770, blend_dest=771, batch=None, group=None, usage='dynamic'):
        self.IMG = img
        pyglet.sprite.Sprite.__init__(self, img, x, y, blend_src, blend_dest, batch, group, usage)

    def move(self, x, y):
        self.set_position(self.x + x, self.y + y)

    @property
    def left(self):
        return self.x

    @property
    def right(self):
        return self.x + self.width
    
    @property
    def top(self):
        return self.y + self.height

    @property
    def bottom(self):
        return self.y

    def center_anchor_y(self, window_height):
        self.y = window_height / 2 - self.height // 2
        return self

    def center_anchor_x(self, window_width):
        self.x = window_width / 2 - self.width // 2
        return self

    def check_collision(self, others_list):
        for sprite in others_list:
            if (self.bottom <= sprite.top and self.top >= sprite.bottom and
                self.right >= sprite.left and self.left <= sprite.right):
                print "Collision detected"
                return sprite

class Ball(SprObj):

    MOVING_RIGHT = True
    MOVE_STEPS = 5
    MOVE_EFFECT = 0

    def invert_moviment(self):
        self.MOVING_RIGHT = not self.MOVING_RIGHT

    def moving(self, clock):
        if self.MOVING_RIGHT:
            self.move(self.MOVE_STEPS, self.MOVE_EFFECT)
        else:
            self.move(-self.MOVE_STEPS, self.MOVE_EFFECT)


class Racket(SprObj):

    SCORE = 0
    def increase_score(self):
        self.SCORE += 1

    def get_hit_effect(self):
        if self.y:
            return self.y * -1



class MainWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        pyglet.window.Window.__init__(self, *args, **kwargs)
        self.push_handlers(keys)

        self.racket_img = pyglet.resource.image(RACKET_IMG)
        self.ball_img = pyglet.resource.image(BALL_IMG)

        self.racket = Racket(self.racket_img).center_anchor_y(WINDOW_HEIGHT)

        self.racket_opponent = Racket(self.racket_img).center_anchor_y(WINDOW_HEIGHT)
        self.racket_opponent.x = WINDOW_WIDTH - self.racket_img.width

        self.ball = Ball(self.ball_img).center_anchor_y(WINDOW_HEIGHT).center_anchor_x(WINDOW_WIDTH)

        self.score = pyglet.text.Label('', font_size=15, x=WINDOW_WIDTH/2, y=WINDOW_HEIGHT - 15, anchor_x='center', anchor_y='center')

        pyglet.clock.schedule_interval(self.ball.moving, .005) 


    def on_draw(self):
        self.clear()


        player = self.ball.check_collision([self.racket, self.racket_opponent])
        if player:
            self.ball.invert_moviment()
            player.increase_score()

        if keys[pyglet.window.key.UP] and self.racket.y < WINDOW_HEIGHT:
            self.racket.move(0, MOVE_SPEED)
            
        if keys[pyglet.window.key.DOWN] and self.racket.y > 0:
            self.racket.move(0, -MOVE_SPEED)


        if keys[pyglet.window.key.NUM_7] and self.racket_opponent.y < WINDOW_HEIGHT:
            self.racket_opponent.move(0, MOVE_SPEED)
            
        if keys[pyglet.window.key.NUM_1] and self.racket_opponent.y > 0:
            self.racket_opponent.move(0, -MOVE_SPEED)

        self.score.text = 'Me: %d  -   Opponent: %d' % (self.racket.SCORE, self.racket_opponent.SCORE)

        self.score.draw()
        self.racket.draw()
        self.racket_opponent.draw()
        data = {
            "id1": {
                "y": self.racket.y
            },
            "id2": {
                "y": self.racket_opponent.y
            }
        }
        data = simplejson.dumps(data)
        print data
        self.ball.draw()


if __name__ == "__main__":
    MainWindow(width=resolution[0], height=resolution[1])
    pyglet.app.run()
