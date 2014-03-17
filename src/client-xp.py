#!/usr/bin/env python
import pyglet
import math
import socket
import simplejson

resolution = (800, 600)
keys = pyglet.window.key.KeyStateHandler()
image = pyglet.image.load('ship.png')
image.anchor_x = image.width // 2
image.anchor_y = image.height // 2

def forward():
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(('192.168.1.43', 50090))
    _id = str(conn.getsockname()[1])
    print "Connected with _id: " + _id
    return [_id, conn]

def create_ship(_id=False):
    ship = pyglet.sprite.Sprite(image)
    ship.x = resolution[0] / 2
    ship.y = resolution[1] / 2
    if _id:
        ship.opacity = 64
        ship._id = _id
    return ship

class MainWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        pyglet.window.Window.__init__(self, *args, **kwargs)
        self.push_handlers(keys)
        self.ship = create_ship()
        self.me, self.conn = forward()
        self.players = []
        self.players_id = []

    def on_draw(self):
        self.clear()
        self.ship.draw()
        x, y = self.ship.position
        a = self.ship.rotation
        data = simplejson.dumps([x, y, a])
        self.conn.send(data)
        data = simplejson.loads(self.conn.recv(2000))

        for shipid in data.keys():
            if shipid != self.me and shipid not in self.players_id:
                self.players_id.append(shipid)
                self.players.append(create_ship(shipid))

        for player in self.players:
            if player._id in data:
                try:
                    player.x, player.y, player.rotation = data[player._id]
                except:
                    pass
            else:
                player.x, player.y, player.rotation = [0, 0, 0]
            player.draw()

        if keys[pyglet.window.key.LEFT]:
            self.ship.rotation -= 2

        if keys[pyglet.window.key.RIGHT]:
            self.ship.rotation += 2

        if keys[pyglet.window.key.UP]:
            diff = math.cos(math.radians(self.ship.rotation))
            self.ship.y += 6 * diff
            increase = math.sin(math.radians(self.ship.rotation))
            self.ship.x += 6 * increase


if __name__ == "__main__":
    MainWindow(width=resolution[0], height=resolution[1])
    pyglet.app.run()
