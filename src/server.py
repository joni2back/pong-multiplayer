#!/usr/bin/env python
import socket, select, sys, time, simplejson
sys.dont_write_bytecode = True
from lib import settings

buffer_size = 2000
delay = 0.01
rackets = {}

class GameServer:

    def __init__(self, host, port):
        self.input_list = []
        self.channel = {}

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(0)

    def main_loop(self):
        self.input_list.append(self.server)
        while 1:
            # TODO: disconnect new clients if the number is > 2
            time.sleep(delay)
            inputr, outputr, exceptr = select.select(self.input_list, [], [])
            for self.s in inputr:
                if self.s == self.server:
                    self.on_accept()
                    break
                else:
                    self.data = self.s.recv(buffer_size)
                if len(self.data) == 0:
                    self.on_close()
                else:
                    self.on_recv()

    def on_accept(self):
        clientsock, clientaddr = self.server.accept()
        print(f"{clientaddr} has connected")
        rackets[clientaddr[1]] = {}
        self.input_list.append(clientsock)

    def on_close(self):
        clientaddr = self.s.getpeername()
        print(f"{clientaddr} has disconnected")
        del(rackets[clientaddr[1]])
        self.input_list.remove(self.s)

    def on_recv(self):
        player_id = self.s.getpeername()[1]
        rackets[player_id] = simplejson.loads(self.data.decode('utf-8'))
        self.s.send(simplejson.dumps(rackets).encode('utf-8'))

if __name__ == '__main__':
        server = GameServer(settings.SERVER_IP, settings.SERVER_PORT)
        print("Server listening...")
        try:
            server.main_loop()
        except KeyboardInterrupt:
            print("Ctrl C - Stopping server")
            sys.exit(1)
