import sprobj

class Ball(sprobj.SprObj):

    MOVING_RIGHT = True
    MOVING_TOP = True
    HORIZONTAL_MOVIMENT = 3
    VERTICAL_MOVIMENT = 0.8

    def hit_racket(self):
        self.MOVING_RIGHT = not self.MOVING_RIGHT

    def hit_lateral(self):
        self.MOVING_TOP = not self.MOVING_TOP

    def moving(self, clock):
        if self.MOVING_RIGHT:
            self.move(self.HORIZONTAL_MOVIMENT, 0)
        else:
            self.move(-self.HORIZONTAL_MOVIMENT, 0)

        if self.MOVING_TOP:
            self.move(0, self.VERTICAL_MOVIMENT)
        else:
            self.move(0, -self.VERTICAL_MOVIMENT)