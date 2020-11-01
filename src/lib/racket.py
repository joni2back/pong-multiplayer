from . import sprobj

class Racket(sprobj.SprObj):

    SCORE = 0

    def increase_score(self):
        self.SCORE += 1

    def get_hit_effect(self):
        if self.y:
            return self.y * -1
