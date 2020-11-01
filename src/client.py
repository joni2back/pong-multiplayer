#!/usr/bin/env python
# Copyright 2014 Jonas Sciangula Street

# Do not generate bytecodes in developer mode
import math, sys, socket
sys.dont_write_bytecode = True


from lib import mainwindow
from lib import settings
import pyglet


if __name__ == "__main__":
    mainwindow.MainWindow(width=settings.WINDOW_WIDTH, height=settings.WINDOW_HEIGHT)
    pyglet.app.run()
