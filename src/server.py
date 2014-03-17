#!/usr/bin/python
import socket
import select
import time
import sys
import simplejson

buffer_size = 2000
delay = 0
rackets = {}

class TheServer:

    def __init__(self, host, port):
        self.input_list = []
        self.channel = {}

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(200)

    def main_loop(self):
        self.input_list.append(self.server)
        while 1:
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
        print clientaddr, "has connected"
        rackets[clientaddr[1]] = {}
        self.input_list.append(clientsock)

    def on_close(self):
        clientaddr = self.s.getpeername()
        print " %s has disconnected" % clientaddr[0]
        del(rackets[clientaddr[1]])
        #remove objects from input_list
        self.input_list.remove(self.s)

    def on_recv(self):
        _id = self.s.getpeername()[1]
        rackets[_id] = simplejson.loads(self.data)
        self.s.send(simplejson.dumps(ships))

if __name__ == '__main__':
        server = TheServer('0.0.0.0', 50090)
        try:
            server.main_loop()
        except KeyboardInterrupt:
            print "Ctrl C - Stopping server"
            sys.exit(1)