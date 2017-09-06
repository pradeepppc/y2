from Person import *
from Bomb import *

class Bomberman(Person):
    name = 'hero'
    life = 3
    score = 0
    level = 0
    def __init__(self):
        Person.__init__(self)



    def put_bomb(self):
        b = Bomb()
        tup = self.get_position()
        tp = b.create_bomb(tup[0], tup[1])
        return tp
    def inc_brick_score(self):
        self.score += 20

    def get_life(self):
        return self.life

    def inc_level(self):
        self.level += 1

    def get_level(self):
        return self.level

    def inc_score(self):
        self.score += 100

    def set_score(self, x):
        self.score = x

    def get_score(self):
        return self.score

    def Got_killed(self):
        self.life -= 1


