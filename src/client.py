#!/usr/bin/env python
#author Jonas Sciangula Street
import pyglet
import math
import socket
import simplejson

WINDOW_WIDTH = 720
WINDOW_HEIGHT = 480
MOVE_SPEED = 15

BALL_IMG = 'assets/ball.png'
RACKET_IMG = 'assets/racket.png'
resolution = (WINDOW_WIDTH, WINDOW_HEIGHT)
keys = pyglet.window.key.KeyStateHandler()


class SprObj(pyglet.sprite.Sprite):

    ROTATION = 0
    SPEED = 0
    IMG = None

    def __init__(self, img, x=0, y=0, blend_src=770, blend_dest=771, batch=None, group=None, usage='dynamic'):
        self.IMG = img
        #self.center_anchor()
        pyglet.sprite.Sprite.__init__(self, img, x, y, blend_src, blend_dest, batch, group, usage)

    def center_anchor(self):
        self.IMG.anchor_x = self.IMG.width // 2
        self.IMG.anchor_y = self.IMG.height // 2
        return self

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

    def check_collision(self, others_list):
        for sprite in others_list:
            if (self.bottom <= sprite.top and
                    self.top >= sprite.bottom and
                    self.right >= sprite.left and
                    self.left <= sprite.right):
                print "Collision detected"
                return sprite

class Ball(SprObj):

    MOVING_RIGHT = True
    MOVE_STEPS = 15
    MOVE_EFFECT = 0
    
    def pong(self, racket_hit_effect):
        self.MOVING_RIGHT = not self.MOVING_RIGHT
        self.MOVE_EFFECT = racket_hit_effect

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
        self.racket = Racket(pyglet.resource.image(RACKET_IMG))
        self.racket.y = WINDOW_HEIGHT / 2

        self.racket_opponent = Racket(pyglet.resource.image(RACKET_IMG))
        self.racket_opponent.x = WINDOW_WIDTH - 9
        self.racket_opponent.y = WINDOW_HEIGHT / 2
                

        self.ball = Ball(pyglet.resource.image(BALL_IMG))
        
        self.ball.y = WINDOW_HEIGHT / 2
        self.ball.x = WINDOW_WIDTH / 2

        self.score = pyglet.text.Label('', font_size=20, x=WINDOW_WIDTH/2, y=WINDOW_HEIGHT - 15, anchor_x='center', anchor_y='center')


        pyglet.clock.schedule_interval(self.ball.moving, .015) 


    def on_draw(self):
        self.clear()


        collision = self.ball.check_collision([self.racket, self.racket_opponent])
        if collision:
            collision.increase_score()
            if self.ball.MOVING_RIGHT:
                self.ball.x -= 3
            else:
                self.ball.x += 3
            self.ball.pong(collision.get_hit_effect())

        #bot
        self.racket_opponent.y = self.ball.y
        
        if keys[pyglet.window.key.UP] and self.racket.y < WINDOW_HEIGHT:
            self.racket.move(0, MOVE_SPEED)
            
        if keys[pyglet.window.key.DOWN] and self.racket.y > 0:
            self.racket.move(0, -MOVE_SPEED)


        if keys[pyglet.window.key.NUM_7] and self.racket_opponent.y < WINDOW_HEIGHT:
            self.racket_opponent.move(0, MOVE_SPEED)
            
        if keys[pyglet.window.key.NUM_1] and self.racket_opponent.y > 0:
            self.racket_opponent.move(0, -MOVE_SPEED)

        self.score.text = 'Me: %d, Computer: %d' % (self.racket.SCORE, self.racket_opponent.SCORE)

        self.score.draw()
        self.racket.draw()
        self.racket_opponent.draw()
        #data = simplejson.dumps(self.racket)
        self.ball.draw()


if __name__ == "__main__":
    MainWindow(width=resolution[0], height=resolution[1])
    pyglet.app.run()
